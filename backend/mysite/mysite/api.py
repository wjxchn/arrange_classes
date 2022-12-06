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
    ret_getdict = {'code': 400, 'msg': "查询失败"}
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
                    'classroom': str(course.course_classroom),
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

def api_addclassroom(request):
    ret_getdict = {'code': 400, 'msg': "查询失败"}
    return JsonResponse(ret_getdict)

def api_getclassroominfo(request):
    ret_getdict = {'code': 400, 'msg': "查询失败"}
    return JsonResponse(ret_getdict)

def api_modifyclassroominfo(request):
    ret_getdict = {'code': 400, 'msg': "查询失败"}
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