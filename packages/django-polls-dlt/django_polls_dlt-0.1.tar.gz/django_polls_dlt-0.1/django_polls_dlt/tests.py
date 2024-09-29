"""
测试建议：
    为每个模型和视图都建立单独的 TestClass
    每个测试方法只测试一个功能
    给每个测试方法其一个自描述功能的名字
"""

import datetime
import logging

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Create your tests here.

class QuestionTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False if questions whose pub_date is in the future.
        :return:
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


# Creating test database for alias 'default'...
# ...
# Destroying test database for alias 'default'...
# Django 会创建一个特殊的数据库供测试使用；
# 当一个测试用例开始时，Django 会开启一个事务，
#   在测试用例执行期间，所有对数据库的修改操作，都在这个事务内部进行；
#   当测试用例结束后，无论成功还是失败，Django 都会回滚（rollback）这个事务；
# 通过这种方式，每个测试用例执行的时候看到的数据库都是初始状态，从而互不影响；
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        logging.debug("test_no_questions")
        # TestCase 自带的 client 可以模拟请求获得 view 视图的返回
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["latest_question_list"], [])
        self.assertContains(response, "No polls are available.")

    def test_past_question(self):
        """
        Questions whose pub_date is in the past should be displayed.
        """
        logging.debug("test_past_question")
        question = create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])

    def test_future_question(self):
        """
        Questions whose pub_date is in the future should not be displayed.
        """
        logging.debug("test_future_question")
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_and_past_question(self):
        logging.debug("test_future_and_past_question")
        question = create_question(question_text="Past question", days=-30)
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])

    def test_two_past_questions(self):
        question1 = create_question("Past question 1", days=-30)
        question2 = create_question("Past question 2", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["latest_question_list"], [question2, question1])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text="Future question", days=30)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question("Past question", days=-30)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["question"], past_question)
        self.assertContains(response, past_question.question_text)
