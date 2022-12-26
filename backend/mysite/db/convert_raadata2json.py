'''
将真实的排课数据转换为json格式
'''
import json
import re
import openpyxl
import pymysql
from input_data2mysql import extract_hour as time_ensure
re_class1 = re.compile(r'\(.\)\d+$')
re_class2 = re.compile(r'\（.\）\d+$')
re_class3 = re.compile(r'^..?\d+$')
re_singular_credit = re.compile(r'第(.*?)单周')
re_even_credit = re.compile(r'第(.*?)双周')
re_credit = re.compile(r'第(.*?)周')

re_day = re.compile(r'星期(\d)$')

re_sections = re.compile(r'第(.*?)节')
# "1": {
#     "teacher": "[1]",
#     "time": "[2021-1-9-7-3, 2021-1-9-7-4, 2021-1-10-7-3, 2021-1-10-7-4, 2021-1-11-7-3, 2021-1-11-7-4, 2021-1-12-7-3, 2021-1-12-7-4, 2021-1-13-7-3, 2021-1-13-7-4, 2021-1-14-7-3, 2021-1-14-7-4, 2021-1-15-7-3, 2021-1-15-7-4, 2021-1-16-7-3, 2021-1-16-7-4]",
#     "classroom": "110"
# },
# week-day-section
text = "第1-16单周 星期4"
sec = "第8,9节"
def extract_hour(text, sections):
    '''
    根据课程的时间处理成对应的json格式
    text 对应excel的 上课时间
    sections 对应 excel中的节次
    '''
    times = []
    #先判断奇偶数
    weeks = []
    day = -1
    secs = []
    res = re_singular_credit.findall(text)
    flag = 0 #0表示正常 1表示单 2表示双
    if len(res)!=0:
        flag = 1
    elif len(re_even_credit.findall(text))!=0:
        res = re_even_credit.findall(text)
        flag = 1
    else:
        res = re_credit.findall(text)
    res = res[0].split(',')
    for res_tmp in res:
        if '-' not in res_tmp:
            num = int(res_tmp)
            # print(num)
            weeks.append(num)
        else:
            num1, num2 = res_tmp.split('-')
            num1 = int(num1)
            num2 = int(num2)
            for i in range(num1,num2+1):
                if flag==0:
                    weeks.append(i)
                if flag==1 and i%2==1:
                    weeks.append(i)
                if flag==2 and i%2==0:
                    weeks.append(i)
    day = str(re_day.findall(text)[0])
    # print(weeks)
    # print("weeks:",weeks)
    # print("day:", day)

    sec_list = re_sections.findall(sections)[0]
    sec_list = sec_list.split(',')
    for sec in sec_list:
        if '第' in sec:
            sec = sec.replace('第','')
        secs.append(int(sec))
    for week in weeks:
        for sec in secs:
            str_tmp = f'2021-1-{week}-{day}-{sec}'
            times.append(str_tmp)
    # print("secs：", secs)
    # print(times)
    return times


def read_excel(filename):
    res_dict = {}
    wb = openpyxl.load_workbook(f'{filename}')
    sheet = wb.worksheets[0]

    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', database='classes_arrangement',
                           charset='utf8')
    cursor = conn.cursor()

    rows = sheet.rows
    cols = sheet.columns
    c_id = 1
    for row in rows:
        datas = [x.value for x in row]
        # print(datas)
        # print(len(datas))
        c_name = datas[0]
        if c_name == '课程名称':
            continue
        type = datas[4]
        t_name = datas[5]
        c_code = str(datas[8])
        c_capacity = int(datas[9])
        time = datas[10]
        sections = datas[11]
        address = datas[12]
        try:
            time_ensure(time,sections)
        except ValueError:
            continue
        times = extract_hour(time,sections)
        title = datas[6]


        class_capa = c_capacity + 20
        # 判断教室 从而判断是否录入此数据
        if address and(re_class1.match(address) or re_class2.match(address) or re_class3.match(address)):
            # print(address)
            #查询教师id和教室id
            sql = f"select teacher_id from db_teacher where teacher_name = '{t_name}';"
            cursor.execute(sql)
            datas = cursor.fetchall()
            t_id = datas[0][0]

            sql = f"select classroom_id from db_classroom where classroom_name = '{address}';"
            cursor.execute(sql)
            datas = cursor.fetchall()
            classroom_id = datas[0][0]

            res_dict[f'{str(c_id)}'] = {'teacher': f'[{t_id}]',
                                        'time': '['+', '.join(times)+']',
                                        'classroom':str(classroom_id)}
            c_id+=1

    print("课程数量：",c_id-1)
    cursor.close()
    conn.close()
    res_datas = json.dumps(res_dict,indent=1)
    with open('raw_data.json',mode='w',encoding='utf-8') as f:
        f.write(res_datas)
if __name__ == '__main__':
    read_excel('全校课表(1).xlsx')