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


def api_getclassinfo(request):
    ret_getdict = {'code': 400, 'msg': "查询失败"}
    return JsonResponse(ret_getdict)


def api_changeclassinfo(request):
    ret_getdict = {'code': 400, 'msg': "查询失败"}
    return JsonResponse(ret_getdict)


def api_deleteclass(request):
    ret_getdict = {'code': 400, 'msg': "查询失败"}
    return JsonResponse(ret_getdict)


def api_arrangeclass(request):
    if request.method == 'POST':
        try:
            res = {'code': 100, 'msg': '排课成功'}
            ga = GeneticOptimize()
            courses = ga.evolution(Course.objects.all(), )
            res['ans'] = {}
            print(res)
            for course in courses:
                res['ans'][course.course_id] = {
                    'time': str(course.course_time),
                    'classroom': str(course.course_classroom.classroom_id),
                }
            print(res)
            return JsonResponse(res)
        except Exception as ex:
            print(ex)
            ret_getdict = {'code': 400, 'msg': "排课失败"}
            return JsonResponse(ret_getdict)
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
            ret_getdict = {'code': 200, 'msg': "查看成功", 'classrooms': classrooms}
            return JsonResponse(ret_getdict)
        except Exception as ex:
            print(ex)
            ret_getdict = {'code': 400, 'msg': "查看失败"}
            return JsonResponse(ret_getdict)
    else:
        ret_getdict = {'code': 400, 'msg': "查看失败"}
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
            classroom_id = request.POST.get('id')
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
    ret_getdict = {'code': 400, 'msg': "查询失败"}
    return JsonResponse(ret_getdict)


def api_manualchangeclasstable(request):
    ret_getdict = {'code': 400, 'msg': "查询失败"}
    return JsonResponse(ret_getdict)
