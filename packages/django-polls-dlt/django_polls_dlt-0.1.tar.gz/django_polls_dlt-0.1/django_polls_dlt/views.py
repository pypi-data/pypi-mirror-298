from django.db.models import F
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


# Create your views here.
# Django 中视图的概念是「一类具有相同功能和模板的网页的集合」
# 在该投票应用中，我们需要下列几个视图
#   问题索引页：展示最近的几个投票问题
#   问题详情页：展示某个投票的问题和不带结果的选项列表
#   问题结果页：展示某个投票的结果
#   投票处理器：用于响应用户为某个问题的特定选项投票的操作

def index(request: HttpRequest) -> HttpResponse:
    latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    # template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    # return HttpResponse(template.render(context, request))
    # 上面的代码等同于下面这一行
    return render(request, "polls/index.html", context)


# 每个视图必须要做的两件事：
#   返回一个包含被请求页面内容的 HttpResponse 对象，
#   或者抛出一个异常比如 Http404；
def detail(request: HttpRequest, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question not found")

    # 尝试用 get() 函数获取一个对象，如果不存在就抛出Http404 也是一个普遍的流程，
    # 因此 Django 也提供了一个快捷函数；
    # 为什么使用辅助函数 get_object_or_404 而不是自己捕获 ObjectDoesNotExist 异常，
    # 为什么 models API 不直接抛出 ObjectDoesNotExist 而是抛出 Http404 呢？
    #   因为这样做会增加 model 和 view 的耦合性；
    #   指导 Django 设计的最重要的思想之一就是用保证松散耦合；
    #   一些受控制的耦合将会被包含在 django.shortcuts 模块中；
    question = get_object_or_404(Question, pk=question_id)
    if question.pub_date >= timezone.now():
        # future question can not be displayed.
        raise Http404()

    return render(request, "polls/detail.html", {
        "question": question,
    })


def vote(request: HttpRequest, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "Please select a choice.",
        })
    else:
        # django.db.models.F() 函数：用于在查询和更新操作中引用模型字段的值；
        # 它允许你在不将数据从数据库中取出到 Python 对象的情况下，直接在数据库层面进行更新操作；
        # 如果没有 F() 函数，当执行 selected_choice.votes = select_choice.votes + 1 这样的操作时，
        # Django 通常会先从数据库中获取 selected_choice 对象的当前 votes 值，将其加载到 Python 内存中，
        # 然后进行加 1 操作，最后将更新后的对象保存回数据库；这种方式在高并发场景下可能会出现数据不一致的问题；
        # 而使用 F() 函数，Django 会直接在数据库层面生成一个类似于 UPDATE table SET votes = votes + 1 WHERE ...
        # 的 SQL 语句，这样就避免了高并发场景下的数据一致性问题；高并发更新时的数据一致性被数据库层面用行锁给解决了；
        # 更广泛的应用场景：F() 函数还可用于其他算术运算（不同字段加减乘除等）
        #   F("field1") - F("field2")
        # F() 函数的命名一种合理的推测是它代表 Field 字段的意思；
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data.
        # This prevents data from being posted twice if a user hit the Back button.
        # reverse(viewname,args=(tuple,)) 根据视图名称和可选参数来生成相应的 URL，
        # 这种方式避免了URL硬编码、可动态生成 URL，提高了可读性和可理解性；
        # HttpResponseRedirect 只接受一个参数：重定向的 URL
        # reverse() 返回的是 url，比如 /polls/1/results, 而不是返回模板路径，需要注意区分；
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def results(request: HttpRequest, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if question.pub_date >= timezone.now():
        raise Http404()
    return render(request, "polls/results.html", {
        "question": question,
    })


# 使用通用视图：代码还是少点好
# detail() results() index() 视图都存在冗余问题，反映了网络开发中的一个常见情况：
# 根据 URL 中的参数从数据库中获取数据、载入模板然后返回渲染后的模板；
# 由于这种情况非常常见，Django 提供了一种快捷方式，叫做”通用视图“系统；
#   通用视图将常见的模式抽象到了一种程度，以至于他甚至都不需要自己编写 Python 模板；
#   例如，ListView 和 DetailView 通用视图分别抽象了”显示对象列表“和
#   ”显示特定类型对象的详细页面“的概念；

class IndexView(generic.ListView):
    template_name = "polls/v2/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five 5 published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    # 每个模型都需要知道它将要操作的模型，
    # 可以使用 model 属性来声明；
    model = Question
    # 默认情况下，generic.DetailView 会使用 app_name/model_name_detail.html 的模板
    # 可以使用 template_name 声明一个指定的模板
    template_name = "polls/v2/detail.html"

    # generic.DetailView 会在这个 queryset() 的基础上再去根据传入的 pk=question_id 去查找对应的 Question
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/v2/results.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


def voteV2(request: HttpRequest, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "Please select a choice.",
        })
    else:
        # django.db.models.F() 函数：用于在查询和更新操作中引用模型字段的值；
        # 它允许你在不将数据从数据库中取出到 Python 对象的情况下，直接在数据库层面进行更新操作；
        # 如果没有 F() 函数，当执行 selected_choice.votes = select_choice.votes + 1 这样的操作时，
        # Django 通常会先从数据库中获取 selected_choice 对象的当前 votes 值，将其加载到 Python 内存中，
        # 然后进行加 1 操作，最后将更新后的对象保存回数据库；这种方式在高并发场景下可能会出现数据不一致的问题；
        # 而使用 F() 函数，Django 会直接在数据库层面生成一个类似于 UPDATE table SET votes = votes + 1 WHERE ...
        # 的 SQL 语句，这样就避免了高并发场景下的数据一致性问题；高并发更新时的数据一致性被数据库层面用行锁给解决了；
        # 更广泛的应用场景：F() 函数还可用于其他算术运算（不同字段加减乘除等）
        #   F("field1") - F("field2")
        # F() 函数的命名一种合理的推测是它代表 Field 字段的意思；
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data.
        # This prevents data from being posted twice if a user hit the Back button.
        # reverse(viewname,args=(tuple,)) 根据视图名称和可选参数来生成相应的 URL，
        # 这种方式避免了URL硬编码、可动态生成 URL，提高了可读性和可理解性；
        # 所有的视图函数都应该采用这种方式；
        # HttpResponseRedirect 只接受一个参数：重定向的 URL
        return HttpResponseRedirect(reverse("polls:resultsV2", args=(question.id,)))
