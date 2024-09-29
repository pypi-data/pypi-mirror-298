from django.urls import path

from . import views

# 定义 app_name，可用来在模板文件中指定 url 的命名空间，
# 即 app_name:path_name
app_name = 'polls'

urlpatterns = [
    # path(route, view, name, kwargs)
    # route: 是一个匹配 UR 来的准则,类似于正则表达式,
    #   Django 响应请求是会从 urlpatterns的第一项开始，按顺序依次匹配列表中的项；
    # view: 视图函数，Django 会传入一个 HttpRequest 对象作为第一个参数，
    #   被捕获的参数以关键字参数的形式传入；
    # name: 为你的 URL 取名以便你在 Django 的任意地方唯一的引用它，尤其是在模板中；
    # kwargs: 任意个关键字参数可作为一个字典传递给视图函数；
    # /polls/
    path('', views.index, name='index'),

    # /polls/5
    # 使用 <> 匹配到网址路径的值后将其作为一个关键字参数发送给视图
    #   detail(request=HttpRequest, question_id=val)
    #   <int:> int 部分是一种转换格式，用来确定匹配网址路径的是什么模式
    #       <:> 冒号(:)用来分隔转换形式和模式名
    # 在 Django 的 URL 配置中，路径末尾的斜杠 / 具有重要意义：
    #   Django 的 URL 解析机制
    #       Django 的 URL 解析器在匹配 URL 时是精确匹配的
    #       重定向行为：Django 会自动进行重定向确保 URL 的一致性，如果自动带上 /
    #   URL 规范和用户体验
    #   实际应用中的考虑
    #       SEO 优化更喜欢一致和规范的 URL 结构
    #       链接的稳定性
    # Django 的 URL 配置使用斜杠结尾是一种良好的实践，
    #   可以提供 URL 的可读性、一致性和可维护性
    #   同时也符合 WEB 开发的标准和用户的期望
    path('<int:question_id>/', views.detail, name='detail'),

    # polls/5/vote
    path('<int:question_id>/vote/', views.vote, name='vote'),

    # polls/5/results
    path('<int:question_id>/results/', views.results, name='results'),

    # 使用通用视图版本的 URLConf
    # IndexView, DetailView, ResultsView 都是通用视图
    path("v2/", views.IndexView.as_view(), name="indexV2"),
    path("v2/<int:pk>/", views.DetailView.as_view(), name="detailV2"),
    path("v2/<int:question_id>/vote/", views.voteV2, name="voteV2"),
    path("v2/<int:pk>/results/", views.ResultsView.as_view(), name="resultsV2"),
]
