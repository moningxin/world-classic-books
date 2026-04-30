# App1/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, verbose_name="手机号")
    reading_hobbies = models.TextField(blank=True, verbose_name="阅读兴趣")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="分类名称")
    description = models.TextField(blank=True, verbose_name="描述")

    class Meta:
        verbose_name = "图书分类"
        verbose_name_plural = "图书分类"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="书名")
    author = models.CharField(max_length=100, verbose_name="作者")
    publisher = models.CharField(max_length=100, verbose_name="出版社")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name='books', verbose_name="分类")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=39.9, verbose_name="价格")
    description = models.TextField(blank=True, verbose_name="描述")
    cover = models.ImageField(upload_to='book_covers/', blank=True, null=True, verbose_name="封面")
    likes = models.IntegerField(default=0, verbose_name="点赞数")
    is_active = models.BooleanField(default=True, verbose_name="是否上架")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    published_date = models.DateField(null=True, blank=True, verbose_name="出版日期")
    isbn = models.CharField(max_length=13, blank=True, verbose_name="ISBN")
    pages = models.IntegerField(null=True, blank=True, verbose_name="页数")
    # 原有字段
    tags = models.CharField(max_length=200, blank=True, verbose_name="标签")
    difficulty_level = models.CharField(max_length=20, choices=[
        ('入门级', '入门级'),
        ('进阶级', '进阶级'),
        ('专家级', '专家级')
    ], default='入门级', verbose_name="难度级别")
    target_audience = models.CharField(max_length=20, choices=[
        ('通用', '通用'),
        ('男生偏好', '男生偏好'),
        ('女生偏好', '女生偏好')
    ], default='通用', verbose_name="目标读者")
    score = models.DecimalField(max_digits=3, decimal_places=1, default=8.5, verbose_name="评分")

    # 新增字段（用于分类浏览页面）
    book_status = models.CharField(max_length=20, choices=[
        ('已完结', '已完结'),
        ('连载中', '连载中')
    ], default='已完结', verbose_name="图书状态")
    word_count = models.IntegerField(default=0, verbose_name="字数")
    last_update = models.DateTimeField(auto_now=True, verbose_name="最后更新")

    class Meta:
        verbose_name = "图书"
        verbose_name_plural = "图书"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_word_count_display(self):
        """获取字数的显示格式"""
        if self.word_count >= 10000:
            return f"{self.word_count / 10000:.1f}万字"
        else:
            return f"{self.word_count}字"

    def get_image_path(self):
        if hasattr(self, 'english_name') and self.english_name:
            safe_name = self.english_name.lower().replace(' ', '_').replace("'", "").replace('"', "")
            image_name = f"book_{safe_name}.jpg"
            image_path = os.path.join('images', image_name)
            static_path = os.path.join('static', image_path)
            if os.path.exists(static_path):
                return f'/static/{image_path}'

class BookShelf(models.Model):
    """
    用户书架模型
    """
    STATUS_CHOICES = [
        ('planned', '想读'),
        ('reading', '在读中'),
        ('completed', '已读完'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, verbose_name='书籍')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned', verbose_name='阅读状态')
    progress = models.IntegerField(default=0, verbose_name='阅读进度(%)')
    rating = models.FloatField(null=True, blank=True, verbose_name='个人评分')
    added_date = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    last_read = models.DateTimeField(auto_now=True, verbose_name='最后阅读时间')
    completed_date = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    notes = models.TextField(blank=True, verbose_name='读书笔记')

    class Meta:
        verbose_name = '用户书架'
        verbose_name_plural = '用户书架'
        unique_together = ['user', 'book']  # 每个用户对每本书只能有一条记录

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"