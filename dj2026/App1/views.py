from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from .models import BookShelf, Category, Book
from .forms import UserLoginForm, UserRegistrationForm

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login/')
def home(request):
    books = Book.objects.filter(is_active=True).select_related('category')
    user_hobbies = request.user.reading_hobbies.split(',') if request.user.reading_hobbies else []
    recommended_books = Book.objects.filter(
        Q(category__name__in=user_hobbies) |
        Q(title__icontains=user_hobbies[0]) if user_hobbies else Q()
    ).select_related('category')[:6]
    context = {
        'books': books,
        'recommended_books': recommended_books,
        'recent_books': Book.objects.filter(is_active=True).select_related('category')[:8]
    }
    return render(request, 'home.html', context)

def category_list(request):
    """
    分类浏览页面 - 显示所有分类和书籍
    """
    all_categories = Category.objects.all()
    books = Book.objects.all()
    print("categories页面接收到的GET参数:", dict(request.GET))
    # 1. 处理分类筛选（使用模板中的分类值）
    category_filter = request.GET.get('category')
    if category_filter and category_filter != 'all':
        print(f"应用分类筛选: {category_filter}")
        category_mapping = {
            'poetry': '诗歌',
            'novel': '小说',
            'classic': '经典名著',
            'modern': '现代文学',
            # 热门榜单映射
            'douban': '豆瓣高分榜',
            'college': '大学生必读书单',
            'healing': '治愈系名著',
            'classic_rank': '经典传世榜',
            'masterpiece': '名家代表作榜',
        }
        if category_filter in category_mapping:
            category_name = category_mapping[category_filter]
            books = books.filter(category__name=category_name)
        else:
            try:
                books = books.filter(category_id=int(category_filter))
            except (ValueError, TypeError):
                print(f"无效的分类筛选值: {category_filter}")
    # 2. 处理难度筛选
    difficulty_filter = request.GET.get('difficulty')
    if difficulty_filter and difficulty_filter != 'all':
        print(f"应用难度筛选: {difficulty_filter}")
        difficulty_mapping = {
            'beginner': '入门级',
            'intermediate': '进阶级',
            'advanced': '高级',
        }
        if difficulty_filter in difficulty_mapping:
            books = books.filter(difficulty_level=difficulty_mapping[difficulty_filter])
    # 3. 处理受众筛选
    audience_filter = request.GET.get('audience')
    if audience_filter and audience_filter != 'all':
        print(f"应用受众筛选: {audience_filter}")
        audience_mapping = {
            'male': '男生偏好',
            'female': '女生偏好',
        }
        if audience_filter in audience_mapping:
            books = books.filter(target_audience=audience_mapping[audience_filter])
    # 4. 处理热门榜单多选
    rank_filter = request.GET.get('rank')
    if rank_filter:
        print(f"应用热门榜单筛选: {rank_filter}")
        rank_list = rank_filter.split(',')
        rank_mapping = {
            'douban': '豆瓣高分榜',
            'college': '大学生必读书单',
            'healing': '治愈系名著',
            'classic': '经典传世榜',
            'masterpiece': '名家代表作榜',
        }
        q_objects = Q()
        for rank in rank_list:
            if rank in rank_mapping:
                q_objects |= Q(category__name=rank_mapping[rank])

        if q_objects:
            books = books.filter(q_objects)
    # 5. 为每个图书计算字数（保持原有的功能）
    for book in books:
        book.word_count = (book.pages if book.pages else 300) * 500
    print(f"categories页面返回的书籍数量: {books.count()}")
    context = {
        'categories': all_categories,
        'books': books,
        'all_categories': all_categories,
    }
    return render(request, 'categories.html', context)

def book_list(request, category_id=None):
    all_categories = Category.objects.all()
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        books = Book.objects.filter(category=category)
    else:
        category = None
        books = Book.objects.all()
    search_query = request.GET.get('q')
    if search_query:
        print(f"应用搜索筛选: {search_query}")
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(publisher__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    sort_by = request.GET.get('sort_by')
    if sort_by:
        if sort_by == 'score':
            books = books.order_by('-score')
        elif sort_by == 'likes':
            books = books.order_by('-likes')
        elif sort_by == 'price_low':
            books = books.order_by('price')
        elif sort_by == 'price_high':
            books = books.order_by('-price')
    else:
        books = books.order_by('-created_at')

    print(f"最终返回的书籍数量: {books.count()}")

    context = {
        'books': books,
        'category': category,
        'all_categories': all_categories,
    }
    return render(request, 'book_list.html', context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id, is_active=True)
    return render(request, 'book_detail.html', {'book': book})

@login_required
def like_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.likes += 1
    book.save()
    return redirect('book_detail', book_id=book_id)

@login_required
def my_bookshelf(request):
    """
    我的书架页面 - 显示用户收藏的书籍
    """
    # 检查是否有添加图书的参数
    add_book_id = request.GET.get('add_book')
    if add_book_id:
        try:
            book = Book.objects.get(id=add_book_id)
            # 检查是否已经在书架中
            existing = BookShelf.objects.filter(user=request.user, book=book).first()
            if not existing:
                BookShelf.objects.create(
                    user=request.user,
                    book=book,
                    status='planned',  # 默认状态为"想读"
                    progress=0,
                    added_date=timezone.now()
                )
                messages.success(request, f'已成功将《{book.title}》添加到书架')
            else:
                messages.info(request, f'《{book.title}》已经在您的书架中了')
        except Book.DoesNotExist:
            messages.error(request, '图书不存在')
    # 获取用户的所有书架记录
    user_bookshelves = BookShelf.objects.filter(user=request.user).select_related('book')
    # 按状态分类统计
    reading_count = user_bookshelves.filter(status='reading').count()
    completed_count = user_bookshelves.filter(status='completed').count()
    planned_count = user_bookshelves.filter(status='planned').count()
    # 获取筛选参数
    status_filter = request.GET.get('status')
    sort_by = request.GET.get('sort_by', 'recent')
    # 应用状态筛选
    if status_filter and status_filter != 'all':
        user_bookshelves = user_bookshelves.filter(status=status_filter)
    # 应用排序
    if sort_by == 'title':
        user_bookshelves = user_bookshelves.order_by('book__title')
    elif sort_by == 'progress':
        user_bookshelves = user_bookshelves.order_by('-progress')
    elif sort_by == 'rating':
        user_bookshelves = user_bookshelves.order_by('-rating')
    else:  # recent
        user_bookshelves = user_bookshelves.order_by('-added_date')
    context = {
        'bookshelves': user_bookshelves,
        'reading_count': reading_count,
        'completed_count': completed_count,
        'planned_count': planned_count,
    }
    return render(request, 'my_book.html', context)


@login_required
def add_to_bookshelf(request, book_id):
    """
    添加书籍到书架
    """
    book = get_object_or_404(Book, id=book_id)
    # 检查是否已经在书架中
    existing_entry = BookShelf.objects.filter(user=request.user, book=book).first()
    if existing_entry:
        messages.info(request, f'《{book.title}》已经在您的书架中了')
    else:
        # 创建新的书架记录
        BookShelf.objects.create(
            user=request.user,
            book=book,
            status='planned',  # 默认状态为"想读"
            progress=0,
            rating=None
        )
        messages.success(request, f'已成功将《{book.title}》添加到书架')
    return redirect('book_detail', book_id=book_id)


@login_required
def update_bookshelf_progress(request, bookshelf_id):
    """
    更新书架中书籍的阅读进度
    """
    if request.method == 'POST':
        bookshelf_item = get_object_or_404(BookShelf, id=bookshelf_id, user=request.user)

        try:
            progress = int(request.POST.get('progress', 0))
            if 0 <= progress <= 100:
                bookshelf_item.progress = progress

                # 如果进度达到100%，自动标记为"已读完"
                if progress >= 100:
                    bookshelf_item.status = 'completed'
                    bookshelf_item.progress = 100
                    bookshelf_item.completed_date = timezone.now()
                elif progress > 0:
                    bookshelf_item.status = 'reading'
                bookshelf_item.last_read = timezone.now()
                bookshelf_item.save()
                return JsonResponse({'success': True, 'progress': progress, 'status': bookshelf_item.status})
            else:
                return JsonResponse({'success': False, 'error': '进度值必须在0-100之间'})
        except ValueError:
            return JsonResponse({'success': False, 'error': '无效的进度值'})
    return JsonResponse({'success': False, 'error': '无效的请求方法'})

@login_required
def update_bookshelf_status(request, bookshelf_id):
    """
    更新书架中书籍的阅读状态
    """
    if request.method == 'POST':
        bookshelf_item = get_object_or_404(BookShelf, id=bookshelf_id, user=request.user)

        new_status = request.POST.get('status')
        if new_status in ['planned', 'reading', 'completed']:
            bookshelf_item.status = new_status
            # 如果是"已读完"，自动设置进度为100%
            if new_status == 'completed':
                bookshelf_item.progress = 100
                bookshelf_item.completed_date = timezone.now()
            bookshelf_item.save()
            return JsonResponse({'success': True, 'status': new_status})
    return JsonResponse({'success': False, 'error': '无效的请求'})

@login_required
def remove_from_bookshelf(request, bookshelf_id):
    """
    从书架中移除书籍
    """
    if request.method == 'POST':
        bookshelf_item = get_object_or_404(BookShelf, id=bookshelf_id, user=request.user)
        book_title = bookshelf_item.book.title
        bookshelf_item.delete()
        return JsonResponse({'success': True, 'message': f'已从书架中移除《{book_title}》'})
    return JsonResponse({'success': False, 'error': '无效的请求方法'})

@login_required
def rate_book_in_bookshelf(request, bookshelf_id):
    """
    为书架中的书籍评分
    """
    if request.method == 'POST':
        bookshelf_item = get_object_or_404(BookShelf, id=bookshelf_id, user=request.user)
        try:
            rating = float(request.POST.get('rating', 0))
            if 0 <= rating <= 10:
                bookshelf_item.rating = rating
                bookshelf_item.save()
                # 同时更新书籍的总评分（可选）
                book = bookshelf_item.book
                book.update_average_rating()  # 假设Book模型有这个方法
                return JsonResponse({'success': True, 'rating': rating})
            else:
                return JsonResponse({'success': False, 'error': '评分必须在0-10之间'})
        except ValueError:
            return JsonResponse({'success': False, 'error': '无效的评分值'})
    return JsonResponse({'success': False, 'error': '无效的请求方法'})