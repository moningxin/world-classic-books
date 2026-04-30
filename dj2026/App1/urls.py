from django.urls import path
from App1 import views

urlpatterns = [
    path('', views.home, name='home'),  # 首页
    path('login/', views.user_login, name='user_login'),  # 登录页
    path('register/', views.user_register, name='user_register'),  # 注册页
    path('logout/', views.user_logout, name='user_logout'),  # 退出登录
    path('categories/', views.category_list, name='category_list'),  # 分类页
    path('books/', views.book_list, name='book_list'),  # 所有图书
    path('books/category/<int:category_id>/', views.book_list, name='book_list_by_category'),  # 分类图书
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),  # 图书详情
    path('book/<int:book_id>/like/', views.like_book, name='like_book'),  # 点赞
    path('my-bookshelf/', views.my_bookshelf, name='my_bookshelf'),
    path('bookshelf/add/<int:book_id>/', views.add_to_bookshelf, name='add_to_bookshelf'),
    path('bookshelf/update-progress/<int:bookshelf_id>/', views.update_bookshelf_progress, name='update_bookshelf_progress'),
    path('bookshelf/update-status/<int:bookshelf_id>/', views.update_bookshelf_status, name='update_bookshelf_status'),
    path('bookshelf/remove/<int:bookshelf_id>/', views.remove_from_bookshelf, name='remove_from_bookshelf'),
    path('bookshelf/rate/<int:bookshelf_id>/', views.rate_book_in_bookshelf, name='rate_book_in_bookshelf'),
]