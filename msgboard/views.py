# -*- coding:utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from models import MyUser, Content
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage
from django_redis import get_redis_connection
from django.core.cache import cache
import logging
import logConfig
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
logger = logging.getLogger(logConfig.logger_name + '.messsageBoard')
PER_PAGE = 6


# Create your views here.
def msg_user_login(request):
    if request.session.get("is_login", None):
        return redirect('msgboard:getMsg')
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        message = '所有字段必须填写!'
        if username and password:
            try:
                user = list(MyUser.objects(username=username))
                if user is not None and user[0].password == password:
                    request.session['is_login'] = True
                    # request.session['user_id'] = user[0].id
                    request.session['username'] = username
                    # return render(request, 'user/index.html')
                    logger.info('用户已登录：%s', str(username))
                    return redirect('msgboard:getMsg')
                else:
                    logger.warning('密码错误：%s', str(username))
                    message = '密码不正确'
            except Exception as e:
                logger.warning('用户不存在：%s', str(username))
                message = '用户不存在!请先注册'
                print e, e.args
        return render(request, 'msgboard/login.html', {'message': message})
    return render(request, 'msgboard/login.html')


def msg_user_logout(request):
    if request.session.get('is_login', None):
        username = request.session.get('username')
        # 如果本来就未登录，也就没有登出一说
        request.session.flush()
        logger.info('用户%s已登出', str(username))
        return render(request, 'msgboard/login.html', {'alert': username + ' logout'})
    return HttpResponse('您还未登录')


def msg_user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username and password:
            if MyUser.objects(username=username):
                return render(request, 'msgboard/login.html', {'alert': '用户名已存在！'})
            user = MyUser(username=username, password=password)
            user.save()
            logger.info('用户%s注册成功', str(username))
            return render(request, 'msgboard/login.html', {'alert': '注册成功！'})
    return HttpResponse('error')


def msg_push(request):
    if request.method == 'POST':
        if request.session.get('is_login', None):
            username = request.session.get('username')
            user = MyUser.objects(username=username)[0]
            user.content_num = user.content_num + 1
            new_content = Content(text=request.POST.get('content'), user=user, time=timezone.now())
            user.save()
            new_content.save()
            content_top = list(MyUser.objects.order_by('-content_num'))
            cache.set('content_top', content_top[:10], 60)
            return redirect('msgboard:getMsg')
        else:
            return render(request, 'msgboard/login.html', {'alert': '请登陆后再进行留言'})


def msg_get(request):
    content_list = Content.objects.order_by('-time')
    paginator = Paginator(content_list, PER_PAGE)
    total_page = paginator.num_pages
    if request.is_ajax():
        page = int(request.GET.get('page'))
        try:
            contents = paginator.page(page)
            # 如果页数不是整数，返回第一页
        except PageNotAnInteger:
            contents = paginator.page(1)
            # 如果页数不存在/不合法，返回最后一页
        except InvalidPage:
            contents = paginator.page(paginator.num_pages)
        content_li = object_list_to_json(contents.object_list)
        # 分别为是否有上一页false/true，是否有下一页false/true，总共多少页，当前页面的数据
        result = {'has_pre_page': contents.has_previous(),
                  'has_next_page': contents.has_next(),
                  'total_page': total_page,
                  'contents_li': content_li,
                  }
        return JsonResponse(result)
    if request.method == 'GET':
        page_num = request.GET.get('page', None)
        if not page_num:
            contents = paginator.page(1)
        else:
            contents = paginator.page(page_num)
        contents_li = list(contents)
        content_top = cache.get('content_top')
        message = request.GET.get('message', None)
        if not content_top:
            content_top = list(MyUser.objects.order_by('-content_num'))

    if request.method == 'POST':
        contents = paginator.page(1)
        contents_li = list(contents)
        content_top = cache.get('content_top')
        message = request.GET.get('message', None)
    return render(request, 'msgboard/index.html', {'contents': contents_li, 'content_top': content_top,
                                                   'message': message, 'total_page': total_page,
                                                   'pageContent': contents})


def object_list_to_json(object_list):
    result = []
    for con in object_list:
        result.append(con.to_json())
    return result
