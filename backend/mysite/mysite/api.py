import os
import time
import json
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import hashers
from db.models import Author, User, Student, Teacher, Admin, Time, Course, Course_constraint, Classroom, Course_table
from mysite.genetic import GeneticOptimize


def api_test(request):
    if request.method == 'POST':
        username_str = request.POST.get('username')
        print(username_str)
        test = Author.objects.filter(name=username_str)
        if test.exists():
            ret_getdict = {'code': 200, 'msg': "查询成功"}
            return JsonResponse(ret_getdict)
        else:
            ret_getdict = {'code': 400, 'msg': "查询失败"}
            return JsonResponse(ret_getdict)
    else:
        ret_getdict = {'code': 400, 'msg': "查询失败"}
        return JsonResponse(ret_getdict)


# 用户登录
def api_login(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            user = User.objects.filter(user_name=username)
            if not user.exists():
                ret_getdict = {'code': 400, 'msg': "用户不存在"}
                return JsonResponse(ret_getdict)
            password = request.POST.get('password')
            if hashers.check_password(password, user[0].user_password):
                ret_getdict = {'code': 200, 'msg': "登录成功", 'id': user[0].user_id}
                return JsonResponse(ret_getdict)
            else:
                ret_getdict = {'code': 400, 'msg': "密码错误"}
                return JsonResponse(ret_getdict)
        except Exception as ex:
            print(ex)
            ret_getdict = {'code': 400, 'msg': "登录失败"}
            return JsonResponse(ret_getdict)
    else:
        ret_getdict = {'code': 400, 'msg': "登录失败"}
        return JsonResponse(ret_getdict)


# 用户注册
def api_register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            user = User.objects.filter(user_name=username)
            if user.exists():
                ret_getdict = {'code': 400, 'msg': "该用户已注册"}
                return JsonResponse(ret_getdict)
            password = request.POST.get('password')
            type = int(request.POST.get('type'))
            user = User(
                user_type=type,
                user_name=username,
                user_password=hashers.make_password(password)
            )
            user.save()
            print(user.user_id)
            if type == 0:
                student = Student(
                    user_id=user.user_id,
                    student_name=request.POST.get('name'),
                    student_sex=request.POST.get('sex'),
                    student_major=request.POST.get('major'),
                    student_class=request.POST.get('class')
                )
                student.save()
            elif type == 1:
                teacher = Teacher(
                    user_id=user.user_id,
                    teacher_name=request.POST.get('name'),
                    teacher_sex=request.POST.get('sex'),
                    teacher_profession_title=request.POST.get('title'),
                )
                teacher.save()
            else:
                admin = Admin(
                    user_id=user.user_id
                )
                admin.save()
            ret_getdict = {'code': 200, 'msg': "注册成功"}
            return JsonResponse(ret_getdict)
        except Exception as ex:
            print(ex)
            ret_getdict = {'code': 400, 'msg': "注册失败"}
            return JsonResponse(ret_getdict)

    else:
        ret_getdict = {'code': 400, 'msg': "注册失败"}
        return JsonResponse(ret_getdict)


# 获取全部用户列表
def api_getuser(request):
    if request.method == 'GET':
        try:
            user_set = User.objects.all()
            users = []
            for user in user_set:
                obj = {}
                obj['id'] = user.user_id
                obj['type'] = user.user_type
                obj['name'] = user.user_name
                users.append(obj)
            ret_getdict = {'code': 200, 'msg': "获取全部用户信息成功", 'users': users}
            return JsonResponse(ret_getdict)
        except Exception as ex:
            print(ex)
            ret_getdict = {'code': 400, 'msg': "获取全部用户信息失败"}
            return JsonResponse(ret_getdict)
    else:
        ret_getdict = {'code': 400, 'msg': "获取全部用户信息失败"}
        return JsonResponse(ret_getdict)


# 获取用户详细信息
def api_getuserinfo(request):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('id')
            user_set = User.objects.filter(user_id=user_id)
            if user_set.exists():
                if user_set[0].user_type == 0:
                    student_set = Student.objects.filter(user_id=user_id)
                    user = {
                        'id': user_id,
                        'type': '学生',
                        'username': user_set[0].user_name,
                        'name': student_set[0].student_name,
                        'sex': student_set[0].student_sex,
                        'major': student_set[0].student_major,
                        'class': student_set[0].student_class
                    }
                elif user_set[0].user_type == 1:
                    teacher_set = Teacher.objects.filter(user_id=user_id)
                    user = {
                        'id': user_id,
                        'type': '教师',
                        'username': user_set[0].user_name,
                        'name': teacher_set[0].teacher_name,
                        'sex': teacher_set[0].teacher_sex,
                        'title': teacher_set[0].teacher_profession_title
                    }
                else:
                    user = {
                        'id': user_id,
                        'type': '管理员',
                        'username': user_set[0].user_name,
                    }
                ret_getdict = {'code': 200, 'msg': "查看成功", 'user': user}
                return JsonResponse(ret_getdict)
            else:
                ret_getdict = {'code': 400, 'msg': "查看失败"}
                return JsonResponse(ret_getdict)
        except Exception as ex:
            print(ex)
            ret_getdict = {'code': 400, 'msg': "查看失败"}
            return JsonResponse(ret_getdict)
    else:
        ret_getdict = {'code': 400, 'msg': "查看失败"}
        return JsonResponse(ret_getdict)


# 修改用户详细信息
def api_changeuserinfo(request):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('id')
            user = User.objects.get(user_id=user_id)
            if user is not None:
                user_type = user.user_type
                user.user_name = request.POST.get('username')
                if user_type == 0:
                    student = Student.objects.get(user_id=user_id)
                    student.student_name = request.POST.get('name')
                    student.student_sex = request.POST.get('sex')
                    student.student_major = request.POST.get('major')
                    student.student_class = request.POST.get('class')
                    student.save()
                elif user_type == 1:
                    teacher = Teacher.objects.get(user_id=user_id)
                    teacher.teacher_name = request.POST.get('name')
                    teacher.teacher_sex = request.POST.get('sex')
                    teacher.teacher_profession_title = request.POST.get('title')
                    teacher.save()
                user.save()
                ret_getdict = {'code': 200, 'msg': "修改成功"}
                return JsonResponse(ret_getdict)
            else:
                ret_getdict = {'code': 400, 'msg': "修改失败"}
                return JsonResponse(ret_getdict)
        except Exception as ex:
            print(ex)
            ret_getdict = {'code': 400, 'msg': "修改失败"}
            return JsonResponse(ret_getdict)
    else:
        ret_getdict = {'code': 400, 'msg': "修改失败"}
        return JsonResponse(ret_getdict)


def api_addclass(request):
    if request.method == 'POST':
        classroom_name = request.POST.get('name')
        classroom_capacity = request.POST.get('capacity')
        classroom_place = request.POST.get('place')
        classroom = Classroom(
            classroom_name=classroom_name,
            classroom_capacity=classroom_capacity,
            classroom_place=classroom_place
        )
        classroom.save()
        ret_getdict = {'code': 200, 'msg': "添加成功"}
        return JsonResponse(ret_getdict)
    else:
        ret_getdict = {'code': 200, 'msg': "添加失败"}
        return JsonResponse(ret_getdict)


# 获取全部课程列表
def api_getclass(request):
    if request.method == 'GET':
        try:
            course_set = Course.objects.all()
            course_list = []
            for course in course_set:
                course_list.append({
                    'id': course.course_id,
                    'code': course.course_code,
                    'name': course.course_name,
                    'capacity': course.course_max_capacity,
                    'introduction': course.course_introduction,
                    'hour': course.course_hour,
                    'type': course.course_type,
                    'score': course.course_score,
                })
            ret_getdict = {'code': 200, 'msg': "获取全部课程信息成功", 'classrooms': course_list}
            return JsonResponse(ret_getdict)
        except Exception as ex:
            print(ex)
            ret_getdict = {'code': 400, 'msg': "获取全部课程信息失败"}
            return JsonResponse(ret_getdict)
    else:
        ret_getdict = {'code': 400, 'msg': "获取全部课程信息失败失败"}
        return JsonResponse(ret_getdict)


def api_changeclassinfo(request):
    ret_getdict = {'code': 400, 'msg': "查询失败"}
    return JsonResponse(ret_getdict)


def api_deleteclass(request):
    ret_getdict = {'code': 400, 'msg': "查询失败"}
    return JsonResponse(ret_getdict)


def api_arrangeclass(request):
    if request.method == 'POST':
        res = {'code': 100, 'msg': '排课成功'}
        ga = GeneticOptimize(popsize=32, elite=16, mutprob=0.2, maxiter=500)
        courses = ga.evolution(Course.objects.all(), Classroom.objects.all())
        res['ans'] = {
            course.course_id: {
                'teacher': str(course.course_teacher),
                'time': str(course.course_time),
                'classroom': str(course.course_classroom.classroom_id),
            } for course in courses
        }
        return JsonResponse(res)
    else:
        ret_getdict = {'code': 400, 'msg': "排课失败"}
        return JsonResponse(ret_getdict)


# 添加教室
def api_addclassroom(request):
    if request.method == 'POST':
        try:
            classroom_name = request.POST.get('name')
            classroom_capacity = request.POST.get('capacity')
            classroom_place = request.POST.get('place')
            classroom = Classroom(
                classroom_name=classroom_name,
                classroom_capacity=classroom_capacity,
                classroom_place=classroom_place
            )
            classroom.save()
            ret_getdict = {'code': 200, 'msg': "添加成功"}
            return JsonResponse(ret_getdict)
        except Exception as ex:
            print(ex)
            ret_getdict = {'code': 400, 'msg': "添加失败"}
            return JsonResponse(ret_getdict)
    else:
        ret_getdict = {'code': 400, 'msg': "添加失败"}
        return JsonResponse(ret_getdict)


# 查看所有教室
def api_getclassroom(request):
    if request.method == 'GET':
        try:
            classroom_set = Classroom.objects.all()
            classrooms = []
            for classroom in classroom_set:
                classrooms.append({
                    'id': classroom.classroom_id,
                    'name': classroom.classroom_name,
                    'capacity': classroom.classroom_capacity,
                    'place': classroom.classroom_place
                })
            ret_getdict = {'code': 200, 'msg': "获取全部教室信息成功", 'classrooms': classrooms}
            return JsonResponse(ret_getdict)
        except Exception as ex:
            print(ex)
            ret_getdict = {'code': 400, 'msg': "获取全部教室信息失败"}
            return JsonResponse(ret_getdict)
    else:
        ret_getdict = {'code': 400, 'msg': "获取全部教室信息失败失败"}
        return JsonResponse(ret_getdict)


# 查看某一教室具体信息
def api_getclassroominfo(request):
    if request.method == 'POST':
        try:
            classroom_id = request.POST.get('id')
            classroom_set = Classroom.objects.filter(classroom_id=classroom_id)
            if classroom_set.exists():
                classroom = {
                    'id': classroom_set[0].classroom_id,
                    'name': classroom_set[0].classroom_name,
                    'capacity': classroom_set[0].classroom_capacity,
                    'place': classroom_set[0].classroom_place
                }
                ret_getdict = {'code': 200, 'msg': "查看成功", 'classroom': classroom}
                return JsonResponse(ret_getdict)
            else:
                ret_getdict = {'code': 400, 'msg': "查看失败"}
                return JsonResponse(ret_getdict)
        except Exception as ex:
            print(ex)
            ret_getdict = {'code': 400, 'msg': "查看失败"}
            return JsonResponse(ret_getdict)
    else:
        ret_getdict = {'code': 400, 'msg': "查看失败"}
        return JsonResponse(ret_getdict)


# 修改某一教室信息
def api_modifyclassroominfo(request):
    if request.method == 'POST':
        try:
            classroom_id = request.POST.get('id')
            classroom_name = request.POST.get('name')
            classroom_capacity = request.POST.get('capacity')
            classroom_place = request.POST.get('place')
            classroom = Classroom.objects.get(classroom_id=classroom_id)
            if classroom is not None:
                classroom.classroom_name = classroom_name
                classroom.classroom_capacity = classroom_capacity
                classroom.classroom_place = classroom_place
                classroom.save()
                ret_getdict = {'code': 200, 'msg': "修改成功"}
                return JsonResponse(ret_getdict)
            else:
                ret_getdict = {'code': 400, 'msg': "修改失败"}
                return JsonResponse(ret_getdict)
        except Exception as ex:
            print(ex)
            ret_getdict = {'code': 400, 'msg': "修改失败"}
            return JsonResponse(ret_getdict)
    else:
        ret_getdict = {'code': 400, 'msg': "修改失败"}
        return JsonResponse(ret_getdict)


# 删除教室
def api_deleteclassroom(request):
    if request.method == 'POST':
        try:
            classroom_id = request.POST.get('data[id]')
            print(request.POST)
            classroom = Classroom.objects.get(classroom_id=classroom_id)
            if classroom is not None:
                classroom.delete()
                ret_getdict = {'code': 200, 'msg': "删除成功"}
                return JsonResponse(ret_getdict)
            else:
                ret_getdict = {'code': 400, 'msg': "删除失败"}
                return JsonResponse(ret_getdict)
        except Exception as ex:
            print(ex)
            ret_getdict = {'code': 400, 'msg': "删除失败"}
            return JsonResponse(ret_getdict)
    else:
        ret_getdict = {'code': 400, 'msg': "删除失败"}
        return JsonResponse(ret_getdict)


def api_getarrangeclasshistory(request):
    ret_getdict = {'code': 400, 'msg': "查询失败"}
    return JsonResponse(ret_getdict)


def api_selectcourse(request):
    ret_getdict = {'code': 400, 'msg': "查询失败"}
    return JsonResponse(ret_getdict)


def api_autochangeclasstable(request):
    if request.method == 'POST':
        # try:
        q_result_file_name = request.POST.get('result_file_name')
        with open(os.path.join('results', q_result_file_name), encoding='utf-8') as f:
            result = json.loads(f.read())

            course_ids = request.POST.get('course_id')
            update_classroom_id = request.POST.get('update_classroom_id')
            course_ids = course_ids[1:-1].split(', ') if course_ids != None else []
            courses1, courses2 = [], []
            for course_id in result.keys():
                course = MyCourse(Course.objects.get(course_id=course_id))
                if (not course_id in course_ids) and (result[course_id]['classroom'] != update_classroom_id):
                    course.course_classroom = MyClassroom(Classroom.objects.get(classroom_id=result[course_id]['classroom']))
                    course.course_time = [MyTime(semester='1', week=week, day=day, class_num=class_num) for week, day, class_num in [list(map(int, time.split('-')[-3:])) for time in result[course_id]['time'][1:-1].split(', ')]]
                    course.course_teacher = list(map(int, result[course_id]['teacher'][1:-1].split('-')))
                    courses1.append(course)
                else:
                    courses2.append(course)

            if len(courses2) == 0:
                res = {'code': 100, 'msg': '排课成功，但是课表不会改变'}
                return JsonResponse(res)
            
            ga = GeneticOptimize(popsize=4, elite=2, mutprob=0.2, maxiter=50)
            courses = ga._evolution(courses2, courses1, Classroom.objects.all())
            courses.extend(courses1)
            res = {'code': 200, 'msg': '排课成功'}
            res['ans'] = {}
            for course in courses:
                res['ans'][course.course_id] = {
                    'teacher': str(course.course_teacher),
                    'time': str(course.course_time),
                    'classroom': str(course.course_classroom.classroom_id),
                } 
                if res['ans'][course.course_id]['teacher'] != result[str(course.course_id)]['teacher']:
                    res['ans'][course.course_id]['pre_teacher'] = result[str(course.course_id)]['teacher']
                if res['ans'][course.course_id]['time'] != result[str(course.course_id)]['time']:
                    res['ans'][course.course_id]['pre_time'] = result[str(course.course_id)]['time']
                if res['ans'][course.course_id]['classroom'] != result[str(course.course_id)]['classroom']:
                    res['ans'][course.course_id]['pre_classroom'] = result[str(course.course_id)]['classroom']
            return JsonResponse(res)
        # except Exception as ex:
        #     print(ex)
        #     ret_getdict = {'code': 300, 'msg': "自动调整失败"}
        #     return JsonResponse(ret_getdict)
    else:
        ret_getdict = {'code': 400, 'msg': "自动调整失败"}


def api_manualchangeclasstable(request):
    if request.method == 'POST':
        try:
            q_result_file_name = request.POST.get('result_file_name')
            course_id = request.POST.get('course_id')
            st_week, ed_week = request.POST.get('st_week'), request.POST.get('ed_week')
            mode = request.POST.get('mode')
            
            with open(os.path.join('results', q_result_file_name), encoding='utf-8') as f:
                result = json.loads(f.read())
                if mode == 'update':
                    result[course_id]['time'] = []
                else:
                    result[course_id]['time'] = result[course_id]['time'][1:-1].split(', ')
                for week in range(int(st_week), int(ed_week) + 1):
                    for day in range(1, 8):
                        for class_num in range(1, 15):
                            if request.POST.get('%d-%d' % (day, class_num)) == '1':
                                if mode == 'add' or mode == 'update':
                                    result[course_id]['time'].append(MyTime(semester='2021-1', week=week, day=day, class_num=class_num))
                                elif mode == 'del':
                                    result[course_id]['time'].remove(str(MyTime(semester='2021-1', week=week, day=day, class_num=class_num)))
                result[course_id]['time'] = ', '.join([str(x) for x in result[course_id]['time']])
                ret_getdict = {'code': 200, 'msg': "计算成功", 'result': result}
                with open(os.path.join('results', '%s.json' % time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))), 'w', encoding='utf8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                return JsonResponse(ret_getdict)
        except Exception as ex:
            print(ex)
            ret_getdict = {'code': 300, 'msg': "手动调整失败"}
            return JsonResponse(ret_getdict)
    else:
        ret_getdict = {'code': 400, 'msg': "手动调整失败"}
    
    return JsonResponse(ret_getdict)


# 按照教室查看课表
def api_getcoursetablebyclassroom(request):
    if request.method == 'POST':
        try:
            mp = {1: 'monday', 2: 'tuesday', 3: 'wednesday', 4: 'thursday', 5: 'friday', 6: 'saturday', 7: 'sunday'}
            res = {str(i): {mp[j]: [] for j in range(1, 8)} for i in range(1, 15)}

            q_result_file_name = request.POST.get('result_file_name')
            q_classroom_id = request.POST.get('classroom_id')
            with open(os.path.join('results', q_result_file_name), encoding='utf-8') as f:
                result = json.loads(f.read())
                for course_id in result.keys():
                    classroom_id = result[course_id]['classroom']
                    teacher_id = list(map(int, result[course_id]['teacher'][1:-1].split(', ')))
                    times = [x.split('-')[-3:] for x in result[course_id]['time'][1:-1].split(', ')]
                    if q_classroom_id == classroom_id:
                        for week, day, class_num in times:
                            res[class_num][mp[int(day)]].append([int(week), course_id, teacher_id])

            for class_num in res.keys():
                for day in res[class_num].keys():
                    if len(res[class_num][day]) > 0:
                        res[class_num][day] = sorted(res[class_num][day], key=lambda x: x[0])
                        _tmp = []
                        for week, course_id, teacher_id in res[class_num][day]:
                            if len(_tmp) > 0 and course_id == _tmp[-1][1] and teacher_id == _tmp[-1][2]:
                                _tmp[-1][0].append(week)
                            else:
                                _tmp.append([[week], course_id, teacher_id])
                        res[class_num][day] = [' '.join([
                            '[{}-{}]'.format(week[0], week[-1]) if len(week) > 1 else '[{}]'.format(week[0]),
                            '{}'.format(Course.objects.get(course_id=course_id).course_name),
                            ', '.join(
                                ['{}'.format(Teacher.objects.get(teacher_id=id).teacher_name) for id in teacher_id]),
                        ]) for week, course_id, teacher_id in _tmp]

            # print(res)
            ret_getdict = {'code': 200, 'msg': "查询成功", 'res': res}
            return JsonResponse(ret_getdict)
        except Exception as ex:
            print(ex)
            ret_getdict = {'code': 300, 'msg': "查询失败"}
            return JsonResponse(ret_getdict)
    else:
        ret_getdict = {'code': 400, 'msg': "查询失败"}
        return JsonResponse(ret_getdict)


# 按照教师查看课表
def api_getcoursetablebyteacher(request):
    if request.method == 'POST':
        try:
            mp = {1: 'monday', 2: 'tuesday', 3: 'wednesday', 4: 'thursday', 5: 'friday', 6: 'saturday', 7: 'sunday'}
            res = {str(i): {mp[j]: [] for j in range(1, 8)} for i in range(1, 15)}

            q_result_file_name = request.POST.get('result_file_name')
            q_teacher_id = int(request.POST.get('teacher_id'))
            with open(os.path.join('results', q_result_file_name), encoding='utf-8') as f:
                result = json.loads(f.read())
                for course_id in result.keys():
                    classroom_id = result[course_id]['classroom']
                    teachers_id = list(map(int, result[course_id]['teacher'][1:-1].split(', ')))
                    print(teachers_id)
                    times = [x.split('-')[-3:] for x in result[course_id]['time'][1:-1].split(', ')]
                    if q_teacher_id in teachers_id:
                        for week, day, class_num in times:
                            res[class_num][mp[int(day)]].append([int(week), course_id, teachers_id, classroom_id])

            for class_num in res.keys():
                for day in res[class_num].keys():
                    if len(res[class_num][day]) > 0:
                        res[class_num][day] = sorted(res[class_num][day], key=lambda x: x[0])
                        _tmp = []
                        for week, course_id, teachers_id, classroom_id in res[class_num][day]:
                            if len(_tmp) > 0 and course_id == _tmp[-1][1] and teachers_id == _tmp[-1][
                                2] and classroom_id == _tmp[-1][3]:
                                _tmp[-1][0].append(week)
                            else:
                                _tmp.append([[week], course_id, teachers_id, classroom_id])
                        res[class_num][day] = [' '.join([
                            '[{}-{}]'.format(week[0], week[-1]) if len(week) > 1 else '[{}]'.format(week[0]),
                            '{}'.format(Course.objects.get(course_id=course_id).course_name),
                            ', '.join(
                                ['{}'.format(Teacher.objects.get(teacher_id=id).teacher_name) for id in teachers_id]),
                            '{}'.format(Classroom.objects.get(classroom_id=classroom_id).classroom_name),
                        ]) for week, course_id, teachers_id, classroom_id in _tmp]

            # print(res)
            ret_getdict = {'code': 200, 'msg': "查询成功", 'res': res}
            return JsonResponse(ret_getdict)
        except Exception as ex:
            print(ex)
            ret_getdict = {'code': 300, 'msg': "查询失败"}
            return JsonResponse(ret_getdict)
    else:
        ret_getdict = {'code': 400, 'msg': "查询失败"}
        return JsonResponse(ret_getdict)


# 按照学生查看课表
def api_getcoursetablebystudent(request):
    if request.method == 'POST':
        try:
            mp = {1: 'monday', 2: 'tuesday', 3: 'wednesday', 4: 'thursday', 5: 'friday', 6: 'saturday', 7: 'sunday'}
            res = {str(i): {mp[j]: [] for j in range(1, 8)} for i in range(1, 15)}

            q_result_file_name = request.POST.get('result_file_name')
            student_id = request.POST.get('student_id')
            course_set = Course.objects.filter(course_student=Student.objects.get(student_id=student_id))
            # print(course_set)
            course_id_list = []
            for course in course_set:
                course_id_list.append(course.course_id)
            # print(course_id_list)
            with open(os.path.join('results', q_result_file_name), encoding='utf-8') as f:
                result = json.loads(f.read())
                for course_id in result.keys():
                    if int(course_id) in course_id_list:
                        classroom_id = result[course_id]['classroom']
                        teachers_id = list(map(int, result[course_id]['teacher'][1:-1].split(', ')))
                        print(teachers_id)
                        times = [x.split('-')[-3:] for x in result[course_id]['time'][1:-1].split(', ')]
                        for week, day, class_num in times:
                            res[class_num][mp[int(day)]].append([int(week), course_id, teachers_id, classroom_id])
                            if week == '6' and day == '2' and class_num == '14':
                                print(course_id)
            # print(res)
            for class_num in res.keys():
                for day in res[class_num].keys():
                    if len(res[class_num][day]) > 0:
                        res[class_num][day] = sorted(res[class_num][day], key=lambda x: x[0])
                        _tmp = []
                        for week, course_id, teachers_id, classroom_id in res[class_num][day]:
                            if len(_tmp) > 0 and course_id == _tmp[-1][1] and teachers_id == _tmp[-1][
                                2] and classroom_id == _tmp[-1][3]:
                                _tmp[-1][0].append(week)
                            else:
                                _tmp.append([[week], course_id, teachers_id, classroom_id])
                        res[class_num][day] = [' '.join([
                            '[{}-{}]'.format(week[0], week[-1]) if len(week) > 1 else '[{}]'.format(week[0]),
                            '{}'.format(Course.objects.get(course_id=course_id).course_name),
                            ', '.join(
                                ['{}'.format(Teacher.objects.get(teacher_id=id).teacher_name) for id in teachers_id]),
                            '{}'.format(Classroom.objects.get(classroom_id=classroom_id).classroom_name),
                        ]) for week, course_id, teachers_id, classroom_id in _tmp]

            # print(res)
            ret_getdict = {'code': 200, 'msg': "查询成功", 'res': res}
            return JsonResponse(ret_getdict)
        except Exception as ex:
            print(ex)
            ret_getdict = {'code': 300, 'msg': "查询失败"}
            return JsonResponse(ret_getdict)
        else:
            ret_getdict = {'code': 400, 'msg': "查询失败"}
            return JsonResponse(ret_getdict)


# 查看所有老师
def api_getteacher(request):
    if request.method == 'GET':
        try:
            teacher_set = Teacher.objects.all()
            teacher_list = []
            for teacher in teacher_set:
                teacher_list.append({
                    'teacher_id': teacher.teacher_id,
                    'user_id': teacher.user_id,
                    'name': teacher.teacher_name,
                    'sex': teacher.teacher_sex,
                    'profession_title': teacher.teacher_profession_title
                })
            ret_getdict = {'code': 200, 'msg': "获取全部教师信息成功", 'teachers': teacher_list}
            return JsonResponse(ret_getdict)
        except Exception as ex:
            print(ex)
            ret_getdict = {'code': 400, 'msg': "获取全部教师信息失败"}
            return JsonResponse(ret_getdict)
    else:
        ret_getdict = {'code': 400, 'msg': "获取全部教师信息失败失败"}
        return JsonResponse(ret_getdict)


# 查看所有学生
def api_getstudent(request):
    if request.method == 'GET':
        try:
            student_set = Student.objects.all()
            student_list = []
            for student in student_set:
                student_list.append({
                    'student_id': student.student_id,
                    'user_id': student.user_id,
                    'name': student.student_name,
                    'sex': student.student_sex,
                    'major': student.student_major,
                    'class': student.student_class
                })
            ret_getdict = {'code': 200, 'msg': "获取全部学生信息成功", 'students': student_list}
            return JsonResponse(ret_getdict)
        except Exception as ex:
            print(ex)
            ret_getdict = {'code': 400, 'msg': "获取全部学生信息失败"}
            return JsonResponse(ret_getdict)
    else:
        ret_getdict = {'code': 400, 'msg': "获取全部学生信息失败失败"}
        return JsonResponse(ret_getdict)

def api_getresultlist(request):
    file_list = os.listdir("./results")
    ret_getdict = {'code': 200, 'msg': "查询排课结果列表成功", 'result_list': file_list}
    return JsonResponse(ret_getdict)

from mysite.genetic import MyCourse, MyClassroom, MyTime
from algorithm.score import schedule_score
def api_json2score(request):
    if request.method == 'POST':
        try:
            q_result_file_name = request.POST.get('result_file_name')
            print(q_result_file_name)
            with open(os.path.join('results', q_result_file_name), encoding='utf-8') as f:
                result = json.loads(f.read())
                courses = []
                for course_id in result.keys():
                    course = MyCourse(Course.objects.get(course_id=course_id))
                    course.course_classroom = MyClassroom(Classroom.objects.get(classroom_id=result[course_id]['classroom']))
                    course.course_time = [MyTime(semester='1', week=week, day=day, class_num=class_num) for week, day, class_num in [list(map(int, time.split('-')[-3:])) for time in result[course_id]['time'][1:-1].split(', ')]]
                    course.course_teacher = list(map(int, result[course_id]['teacher'][1:-1].split('-')))
                    courses.append(course)

            _, score, hard, soft = schedule_score([courses], 1)
            ret_getdict = {'code': 200, 'msg': "计算成功", 'score': score, 'hard': hard, 'soft': soft}
            return JsonResponse(ret_getdict)
        except Exception as ex:
            print(ex)
            ret_getdict = {'code': 400, 'msg': "计算失败"}
            return JsonResponse(ret_getdict)
    else:
        ret_getdict = {'code': 400, 'msg': "计算失败"}
        return JsonResponse(ret_getdict)
