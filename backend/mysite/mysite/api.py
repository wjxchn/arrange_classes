from django.http import JsonResponse, HttpResponse
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


def api_login(request):
    ret_getdict = {'code': 400, 'msg': "查询失败"}
    return JsonResponse(ret_getdict)


def api_register(request):
    ret_getdict = {'code': 400, 'msg': "查询失败"}
    return JsonResponse(ret_getdict)


def api_getuserinfo(request):
    ret_getdict = {'code': 400, 'msg': "查询失败"}
    return JsonResponse(ret_getdict)


def api_changeuserinfo(request):
    ret_getdict = {'code': 400, 'msg': "查询失败"}
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
