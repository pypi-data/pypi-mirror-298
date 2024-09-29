from django.contrib import admin

from .models import Question, Choice


# Register your models here.
# admin.site.register(Choice)

#
# class ChoiceInline(admin.StackedInline):
# 通过 TabularInline 替代 StackInline，关联对象以一种表格式的方式展示，显得更加紧凑；
class ChoiceInline(admin.TabularInline):
    """
    声明 Choice 对象要在 Question 后台页面编辑
    """
    model = Choice
    # 在关联的外键对象编辑中、默认提供 3 个空白的 Choice 选项供你编辑
    extra = 3


# 通过 admin.site.register() 注册的模型，Django 能够构建一个默认的表单用于展示；
# admin.site.register(Question)

# 自定义的模型表单的外观和工作方式，你可以在注册模型时将这些设置告诉 Django；
class QuestionAdmin(admin.ModelAdmin):
    # 尝试通过重排列表单上的字段来看看 admin.ModelAdmin 是怎么工作的;
    # 表单字段重排在模型拥有多个字段的时候就显得比较直观了；
    # fields = ["pub_date", "question_text"]

    # 在模型拥有字段比较多的时候，还可以将表单分为几个字段集;
    # fieldsets 和 fields 是互斥的，不能同时设置；
    #   <class 'polls.admin.QuestionAdmin'>: (admin.E005) Both 'fieldsets' and 'fields' are specified.
    #   <class 'polls.admin.QuestionAdmin'>: (admin.E012) There are duplicate field(s) in 'fieldsets[1][1]'.
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]

    # 声明 Choice 对象要在 Question 后台页面编辑
    inlines = [ChoiceInline]

    # 默认情况下，Django 对象显示每个对象的 str()，但有时如果能显示单个字段会更有帮助；
    # list_diaply 选项就是为此而设计的，它是对象的更改列表页上以列形式显示的字段名称和列表；
    # list_display = ["question_text", "pub_date"]
    # 同时，list_display 的列表页还能以列的形式显示对象某个函数的返回值；
    # was_published_recently 这一列在管理后台列表页是默认没有排序功能的，
    #   可以通过 @admin.display 装饰器在 was_published_recently() 上进行注解使其获得排序功能；
    list_display = ["question_text", "pub_date", "was_published_recently"]

    # 给列表页添加过滤器，Django 会根据字段的常用类型自动推断要提供那个过滤器；
    list_filter = ["pub_date"]

    # 搜索功能，可以添加多个字段，后台使用 LIKE 来模糊查询，推荐搜索字段只设置一个，便于数据库操作；
    search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)
