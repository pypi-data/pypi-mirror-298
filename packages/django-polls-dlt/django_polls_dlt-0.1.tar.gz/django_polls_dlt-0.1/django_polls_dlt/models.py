import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone


# Create your models here.

class Question(models.Model):
    # 每个 Field 类实例变量的名字(question_text,pub_date)，也是字段名；
    #   所以请使用对机器友好的格式，你将会在 Python 代码里使用它们， 而数据库会将它们作为列名；
    # 定义 Field 类实例有时需要参数，
    #   这些参数的用处不仅用来定义数据库结构，
    #   也用于数据格式验证；
    question_text = models.CharField(max_length=200)
    # 这里的 "date published" 是 verbose_name，
    #   即对人类阅读友好的名字， Django 会将其作为文档的一部分；
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    # was_published_recently 函数值夜可以添加到 Question 后台管理列表页，
    # 这一列在管理后台列表页是默认没有排序功能的，
    #  可以通过 @admin.display 装饰器在 was_published_recently() 上进行注解使其获得排序功能；
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    # 使用 ForeignKey 定义一个一对多的关系 relationship；
    #   一个 Choice 属于一个 Question, 一个 Question 可以有多个 Choice;
    # CASCADE 是级联的意思，
    #   表示当关联的对象 Question 删除时，
    #   与之相关联的当前对象（包含这个外界的对象，即 Choice）也会被自动删除；
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


"""
如何定义一对一关系？ One to One
    class User(models.Model):
        pass
    class Profile(models.Model):
        user = models.models.OneToOneField(User, on_delete=models.CASCADE)
        
如何定义多对多关系？Many to Many
    class Student(models.Model):
        pass
    class Course(models.Model):
        students = models.ManyToManyField(Student)

"""
