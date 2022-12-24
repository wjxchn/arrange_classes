import re
import openpyxl
import pymysql
re_singular_credit = re.compile(r'第(.*?)单周')
re_even_credit = re.compile(r'第(.*?)双周')
re_credit = re.compile(r'第(.*?)周')

re_day = re.compile(r'星期')

re_sections = re.compile(r'第(.*?)节')

#对于教室 考虑两个模式  一个是字母+数字  一个是(汉字)+数字

classroom = '主312'
re_class1 = re.compile(r'\(.\)\d+$')
re_class2 = re.compile(r'\（.\）\d+$')
re_class3 = re.compile(r'^..?\d+$')
# res = re_class3.match(classroom)
# print(res)

# conn = pymysql.connect(host='127.0.0.1', user='root',password='123456', database='classes_arrangement',charset='utf8')
# cursor = conn.cursor()

# sql = "insert ignore into db_course  " \
#       "(course_code, course_hour, course_max_capacity, course_name,course_type) values(1,16,120,'数学','必修' );"
# cursor.execute(sql)
# sql = "SELECT * from db_course;"
# cursor.execute(sql)
# datas = cursor.fetchall()
#
# for data in datas:
#     print(data)
def extract_hour(text, sections):
    '''
    根据课程的时间返回其课时数
    text 对应excel的 上课时间
    sections 对应 excel中的节次
    '''
    #先判断奇偶数
    weeks = 0
    res = re_singular_credit.findall(text)
    flag = 0 #0表示正常 1表示单双周
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
            weeks += 1
        else:
            num1, num2 = res_tmp.split('-')
            num1 = int(num1)
            num2 = int(num2)
            gap = num2-num1 +1
            if flag == 0:
                weeks += gap
            else:
                weeks += gap/2

    days = len(re_day.findall(text))
    # print(weeks)
    # print(days)

    sec_list = re_sections.findall(sections)[0]
    sec_list = sec_list.split(',')
    secs = len(sec_list)
    # print(secs)
    hour = weeks * days * secs
    return hour



def read_excel(filename):
    wb = openpyxl.load_workbook(f'{filename}')
    sheet = wb.worksheets[0]

    conn = pymysql.connect(host='127.0.0.1', user='root', password='macaronlin', database='classes_arrangement',
                           charset='utf8')
    cursor = conn.cursor()

    rows = sheet.rows
    cols = sheet.columns
    i = 0
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
            hour = extract_hour(time,sections)
        except ValueError:
            continue
        title = datas[6]


        class_capa = c_capacity + 20
        # 判断教室 从而判断是否录入此数据
        if address and(re_class1.match(address) or re_class2.match(address) or re_class3.match(address)):
            # print(address)
            c_id = insert_course(conn, cursor, c_code, c_name, c_capacity, hour, type)
            insert_teacher(conn, cursor, c_id, t_name, title)
            insert_classroom(conn,cursor,address,class_capa)

        # print(c_name,type,t_name,c_code,c_capacity,time,sections,address,hour)

        i += 1
        # if i==100:
        #     break
        # 插入课程表


    cursor.close()
    conn.close()
    # print(course_names)

def insert_classroom(coon, cursor, classroom,class_capa):
    '''
    插入db_classroom
    '''
    #首先检查此教室是否已经插入了
    sql = f"select * from db_classroom where classroom_name = '{classroom}';"
    cursor.execute(sql)
    datas = cursor.fetchall()
    if len(datas)==0:
        sql = f"insert ignore  into db_classroom (classroom_name,classroom_capacity) " \
              f"values('{classroom}',{class_capa});"
        cursor.execute(sql)
        coon.commit()
    else:
        if datas[0][2] < class_capa:
            sql = f"update db_classroom set classroom_capacity={class_capa} where classroom_name = '{classroom}';"
            cursor.execute(sql)
            coon.commit()


def insert_teacher(coon, cursor, c_id, t_name, titlt):
    '''
    往db_teacher中插入数据
    以及 db_course_course_teacher
    '''
    #首先获得课程id
    # sql =f"select course_id from db_course where course_code = '{c_code}';"
    # cursor.execute(sql)
    # c_id = cursor.fetchall()
    # c_id = c_id[0][0]
    # print('c_id:',c_id)

    #检查数据库中是否已有此老师
    sql = f"select teacher_id from db_teacher where teacher_name = '{t_name}';"
    cursor.execute(sql)
    datas = cursor.fetchall()
    # print('datas:',datas)
    if len(datas)==0:
        #说明此老师第一次出现
        sql = f"insert ignore  into db_teacher(teacher_name,teacher_profession_title) " \
              f"values('{t_name}','{titlt}');"
        cursor.execute(sql)
        coon.commit()
    #获得老师id
    sql = f"select teacher_id from db_teacher where teacher_name = '{t_name}';"
    cursor.execute(sql)
    t_id = cursor.fetchall()
    t_id = t_id[0][0]
    # print('t_id:',t_id)

    sql = f"select * from db_course_course_teacher ;"
    cursor.execute(sql)
    datas = cursor.fetchall()
    # print(datas)
    # #最后录入老师 课程的对应关系
    # print(f"我想插入{c_id},{t_id}")
    sql = f"insert into db_course_course_teacher(course_id, teacher_id)" \
          f"values({c_id}, {t_id});"
    cursor.execute(sql)
    coon.commit()



#往db_course中添加数据
def insert_course(coon, cursor, c_code, c_name, c_capacity, hour, type):
    sql = f"insert ignore into db_course  " \
          "(course_code, course_hour, course_max_capacity, course_name,course_type) " \
          f"values('{c_code}',{hour},{c_capacity},'{c_name}','{type}' );"
    cursor.execute(sql)
    # print(coon.insert_id())
    c_id = coon.insert_id()
    coon.commit()
    # sql = f"select "
    # sql = "SELECT course_name from db_course where course_id=0  "
    # cursor.execute(sql)
    # datas = cursor.fetchall()
    # print('datas:',datas)
    # print('len:',len(datas))
    # for data in datas:
    #     print(data[0])

    return c_id
    pass



if __name__ == '__main__':

    read_excel('全校课表(1).xlsx')

# print('-' in text)






