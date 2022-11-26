from django.http import JsonResponse,HttpResponse
from db.models import Author, Publish, Book

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
    ret_getdict = {'code': 400, 'msg': "查询失败"}
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