"""
polls: 一个简单的投票应用；

创建模型
    Django 里面写数据库驱动的 WEB 应用的第一步是定义模型，即数据库结构设计和附加其他元数据；
    一个模型就是单个数据的信息源；
    模型中包含了不可缺少的数据区域和存储数据的行为；
    Django 遵循 DRY 原则；目的就是先在某处定义好数据模型，然后自动从该位置推导一些事情；
    Django 的迁移代码是由模型文件自动生成的，它本质上是个历史记录，
    Django 可以用它来进行数据库的滚动更新，通过这种方式使其能够和当前的模型匹配；

在这个投票应用中，需要创建两个模型：
    Question 问题
        desc        问题描述
        publish_ts  发布时间
        choices
    Choice 选项
        desc        选项描述
        vote        当前得票数
        question_id

python manage.py makemigrations polls

    Migrations for 'polls':
    polls/migrations/0001_initial.py
        + Create model Question
        + Create model Choice

python manage.py sqlmigrate polls 0001

    # the output depends on your DB (sqlite3, mysql, or postgresql)
    # 最终的表名是由 appName_modelName 拼接而来
    # 主键 ID 会被自动创建
    # Django 会默认在外键字段名后追加字符串 _id，如 question_id
    # 外键关系由 ForeignKey 生成，不用关心 REFERENCES 部分，
    #   它只是告诉数据库，请在全部事务执行完之后再创建外键关系；

    BEGIN;
    --
    -- Create model Question
    --
    CREATE TABLE "polls_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "question_text" varchar(200) NOT NULL, "pub_date" datetime NOT NULL);
    --
    -- Create model Choice
    --
    CREATE TABLE "polls_choice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "choice_text" varchar(200) NOT NULL, "votes" integer NOT NULL, "question_id" bigint NOT NULL REFERENCES "polls_question" ("id") DEFERRABLE INITIALLY DEFERRED);
    CREATE INDEX "polls_choice_question_id_c5b4b260" ON "polls_choice" ("question_id");
    COMMIT;


# 可以执行这条语句来帮忙检查项目中的问题，在检查过程中不会对数据库进行任何操作
python manage.py check

# 再次执行 migrate 命令，它会选中所有还没有执行过的迁移，并应用在数据库上；
#   Django 会创建一个特殊的表 django_migrations 来跟踪执行过哪些迁移；

# 数据库迁移是非常强大的功能，
    它能让你在开发过程中持续的改变数据库结构而不需要重新删除或创建表；
    它专注于使数据库平滑升级而不会丢失数据；

# 改变模型需要这三步：
    - 编辑 models.py 文件，改变模型；
    - 运行 python manage.py makemigrations 为模型的改变生成迁移文件；
    - 运行 python manage.py migrate 来应用数据库迁移；

python manage.py migrate

# 进入 manage shell，这个命令会设置 DJANGO_SETTINGS_MODULE 环境变量，
# 它会让 Django 根据 django_site/settings.py 来设置 Python 包的导入路径;
# 可以在 manage shell 中探索数据库 API
    python manage.py shell

Django 管理页面
    为你的数据库表生成一行记录、修改和删除内容的后台是一项缺乏创造性和乏味的工作，
    因此，Django 全自动的地根据模型创建了后台的管理界面；
    Django 产生于一个公众页面和内容发布者完全分离的新闻类站点的开发过程中；
    站点管理人员使用管理系统来添加新闻、事件和资讯等，
    这些添加的内容诶显示在公众页面上；

    首先需要创建一个能登录管理页面的用户：
        python manage.py createsuperuser
    登录后会默认看到
        Authentication and Authorization
            Groups 和 Users
        它们是由 django.contrib.auth 提供的，这是 Django 开发的认证框架

如何让 PyCharm Professional 支持 Django 项目，比如解析一些 Django 里面的一些基类中的属性
    配置 Django 项目：在 PyCharm 的设置中，
    找到 “Languages & Frameworks”（语言和框架）->“Django” 选项。
    确保项目的settings.py文件路径正确设置，
    并且 “Enable Django Support”（启用 Django 支持）选项已勾选;

模板文件
    Django 项目的 TEMPLATES 配置项描述了 Django 项目如何载入和渲染模板；
    默认的设置文件使用了  DjangoTemplates backend，并将 APP_DIRS  设置为 True;
    这一选项将会让 DjangoTemplates 在每个 INSTALLED_APPS 文件夹中寻找 templates 子目录；
    这就是缺省配置；所以我们只需要在对应的app中创建templates目录放入模板文件即可；

    模板文件路径示例：polls/templates/polls/index.html
        在上面这个示例中，固然可以在 polls/templates 下面直接放置模板文件，
        但是如果不同的应用中有重名的模板文件，Django 就没有办法区分它们；
        而 templates/polls/index.html 中的 /polls/ 其实是模板文件的命名空间，
        通过这种方式，我们帮助 Django 来区分各自的模板，保证不会重名；

编写测试
    测试将节约你的时间；
    测试不仅能发现错误，而且能预防错误；
    测试有利于团队协作；
    测试使你的代码更有吸引力；

python manage.py test polls

"""
