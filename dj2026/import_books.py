# import_books.py - 修改后的版本
import os
import sys
import django
from datetime import date, datetime
import random

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj2026.settings')
django.setup()

from App1.models import Category, Book


def import_data():
    """导入图书数据 - 添加新字段"""

    print("开始导入图书数据...")

    # 创建所有分类（不变）
    categories_data = [
        ('诗歌', '诗歌体裁相关书籍'),
        ('入门级', '适合初学者的入门级名著'),
        ('进阶级', '需要一定阅读基础的进阶书籍'),
        ('男生偏好榜', '受男性读者欢迎的书籍'),
        ('女生偏好榜', '受女性读者欢迎的书籍'),
        ('豆瓣高分榜', '豆瓣评分高的经典书籍'),
        ('大学生必读书单', '大学生推荐阅读的书目'),
        ('治愈系名著', '温暖治愈心灵的书籍'),
        ('经典传世榜', '经典传世名著'),
        ('名家代表作榜', '名家代表作品'),
        ('冷门高分榜', '冷门但评分高的作品'),
    ]

    categories = {}
    for name, description in categories_data:
        category, created = Category.objects.get_or_create(
            name=name,
            defaults={'description': description}
        )
        categories[name] = category
        if created:
            print(f"✓ 创建分类: {name}")

    # 完整的图书数据，包含所有字段
    books_data = [
        # 第一个图片的数据
        {'title': '飞鸟集', 'author': '泰戈尔', 'publisher': '人民文学出版社', 'category': categories['诗歌'],
         'price': 32.5, 'description': '325首短诗，以自然万物喻人生哲理，语言清新优美，传递爱与希望。',
         'tags': '诗歌,哲理,治愈', 'difficulty_level': '入门级', 'target_audience': '通用', 'score': 8.7, 'likes': 325,
         'book_status': '已完结', 'word_count': 45000, 'last_update': datetime.now()},

        {'title': '小王子', 'author': '安托万·德·圣埃克苏佩里', 'publisher': '译林出版社',
         'category': categories['入门级'],
         'price': 28.0,
         'description': '小王子的星际旅行，遇见国王、商人等角色，探讨爱、孤独与成长，适合所有年龄段的入门名著。',
         'tags': '童话,哲理,入门', 'difficulty_level': '入门级', 'target_audience': '通用', 'score': 9.2,
         'likes': 1256, 'book_status': '已完结', 'word_count': 38000, 'last_update': datetime.now()},

        {'title': '卡拉马佐夫兄弟', 'author': '陀思妥耶夫斯基', 'publisher': '上海译文出版社',
         'category': categories['进阶级'],
         'price': 78.0, 'description': '卡拉马佐夫父子的矛盾与冲突，探讨人性、信仰与道德，思想深奥与文学性兼具。',
         'tags': '现实主义,哲学,进阶', 'difficulty_level': '进阶级', 'target_audience': '通用', 'score': 9.0,
         'likes': 856, 'book_status': '已完结', 'word_count': 850000, 'last_update': datetime.now()},

        {'title': '战争与和平', 'author': '列夫·托尔斯泰', 'publisher': '人民文学出版社',
         'category': categories['男生偏好榜'],
         'price': 89.9, 'description': '宏大的战争场面与细腻的人物刻画，展现男性对历史、责任与荣誉的思考。',
         'tags': '史诗,历史,战争', 'difficulty_level': '进阶级', 'target_audience': '男生偏好', 'score': 9.1,
         'likes': 1567, 'book_status': '已完结', 'word_count': 1200000, 'last_update': datetime.now()},

        {'title': '百年孤独', 'author': '加西亚·马尔克斯', 'publisher': '南海出版公司',
         'category': categories['男生偏好榜'],
         'price': 45.0, 'description': '复杂的家族脉络与魔幻情节，考验逻辑思维与想象力，深受男性读者喜爱。',
         'tags': '魔幻现实主义,史诗', 'difficulty_level': '进阶级', 'target_audience': '男生偏好', 'score': 9.3,
         'likes': 2876, 'book_status': '已完结', 'word_count': 280000, 'last_update': datetime.now()},

        {'title': '堂吉诃德', 'author': '塞万提斯', 'publisher': '人民文学出版社', 'category': categories['男生偏好榜'],
         'price': 52.0, 'description': '堂吉诃德的荒诞冒险，讽刺中世纪骑士制度，充满幽默与深刻的社会批判。',
         'tags': '讽刺,冒险,骑士文学', 'difficulty_level': '进阶级', 'target_audience': '男生偏好', 'score': 8.8,
         'likes': 1098, 'book_status': '已完结', 'word_count': 950000, 'last_update': datetime.now()},

        {'title': '飘', 'author': '玛格丽特·米切尔', 'publisher': '上海译文出版社',
         'category': categories['女生偏好榜'],
         'price': 65.0, 'description': '斯嘉丽在南北战争中的坚韧与成长，与瑞德的爱恨纠葛，展现女性的生命力。',
         'tags': '爱情,战争,女性成长', 'difficulty_level': '进阶级', 'target_audience': '女生偏好', 'score': 9.0,
         'likes': 1876, 'book_status': '已完结', 'word_count': 1032000, 'last_update': datetime.now()},

        {'title': '小妇人', 'author': '路易莎·梅·奥尔科特', 'publisher': '译林出版社',
         'category': categories['女生偏好榜'],
         'price': 38.0, 'description': '马奇家四姐妹的成长故事，传递爱、善良与独立的价值观，温暖治愈。',
         'tags': '家庭,成长,女性互助', 'difficulty_level': '入门级', 'target_audience': '女生偏好', 'score': 8.9,
         'likes': 1543, 'book_status': '已完结', 'word_count': 185000, 'last_update': datetime.now()},

        {'title': '茶花女', 'author': '小仲马', 'publisher': '人民文学出版社', 'category': categories['女生偏好榜'],
         'price': 32.0, 'description': '妓女玛格丽特与阿尔芒的纯洁爱情，揭露资产阶级的虚伪与冷漠，催人泪下。',
         'tags': '爱情,悲剧,人性', 'difficulty_level': '入门级', 'target_audience': '女生偏好', 'score': 8.7,
         'likes': 987, 'book_status': '已完结', 'word_count': 145000, 'last_update': datetime.now()},

        # 第二个图片的数据
        {'title': '局外人', 'author': '阿尔贝·加缪', 'publisher': '上海译文出版社',
         'category': categories['豆瓣高分榜'],
         'price': 35.0, 'description': '短小精悍却直击灵魂，探讨现代人的存在困境，引发无数读者共鸣。豆瓣评分9.0分。',
         'tags': '存在主义,9.0分,现代文学', 'difficulty_level': '进阶级', 'target_audience': '通用', 'score': 9.0,
         'likes': 1324, 'book_status': '已完结', 'word_count': 78000, 'last_update': datetime.now()},

        {'title': '哈姆雷特', 'author': '威廉·莎士比亚', 'publisher': '人民文学出版社',
         'category': categories['豆瓣高分榜'],
         'price': 38.0, 'description': '莎士比亚四大悲剧之首，语言精妙，哲学思考深刻，影响后世无数文学作品。豆瓣评分8.9分。',
         'tags': '戏剧,8.9分,悲剧', 'difficulty_level': '进阶级', 'target_audience': '通用', 'score': 8.9,
         'likes': 1098, 'book_status': '已完结', 'word_count': 92000, 'last_update': datetime.now()},

        {'title': '理想国', 'author': '柏拉图', 'publisher': '商务印书馆', 'category': categories['大学生必读书单'],
         'price': 48.0, 'description': '西方哲学的奠基之作，探讨正义、国家与理想生活，培养批判性思维。',
         'tags': '哲学,政治,经典', 'difficulty_level': '专家级', 'target_audience': '通用', 'score': 8.8, 'likes': 765,
         'book_status': '已完结', 'word_count': 320000, 'last_update': datetime.now()},

        {'title': '了不起的盖茨比', 'author': 'F·司各特·菲茨杰拉德', 'publisher': '人民文学出版社',
         'category': categories['大学生必读书单'],
         'price': 42.0, 'description': '盖茨比的爱情与悲剧，揭露20世纪美国梦的幻灭，文学手法精湛，是大学文学课程的必读书。',
         'tags': '现代主义,美国梦', 'difficulty_level': '进阶级', 'target_audience': '通用', 'score': 8.9,
         'likes': 987, 'book_status': '已完结', 'word_count': 68000, 'last_update': datetime.now()},

        {'title': '瓦尔登湖', 'author': '梭罗', 'publisher': '上海译文出版社', 'category': categories['治愈系名著'],
         'price': 45.0, 'description': '梭罗在瓦尔登湖畔的独居生活，倡导简单生活，安抚现代人的焦虑与浮躁。',
         'tags': '自然,治愈,哲理', 'difficulty_level': '进阶级', 'target_audience': '通用', 'score': 8.7, 'likes': 876,
         'book_status': '已完结', 'word_count': 215000, 'last_update': datetime.now()},

        # 其他数据
        {'title': '傲慢与偏见', 'author': '简·奥斯汀', 'publisher': '人民文学出版社',
         'category': categories['经典传世榜'],
         'price': 36.0, 'description': '伊丽莎白与达西的爱情故事，展现了英国乡村生活和社会阶层差异，经典爱情小说。',
         'tags': '爱情,社会讽刺,经典', 'difficulty_level': '入门级', 'target_audience': '女生偏好', 'score': 9.0,
         'likes': 1432, 'book_status': '已完结', 'word_count': 185000, 'last_update': datetime.now()},

        {'title': '巴黎圣母院', 'author': '雨果', 'publisher': '人民文学出版社', 'category': categories['名家代表作榜'],
         'price': 55.0, 'description': '雨果的代表作之一，讲述钟楼怪人卡西莫多的故事，充满浪漫主义色彩和人道主义精神。',
         'tags': '浪漫主义,人性,法国文学', 'difficulty_level': '进阶级', 'target_audience': '通用', 'score': 8.9,
         'likes': 1123, 'book_status': '已完结', 'word_count': 460000, 'last_update': datetime.now()},

        {'title': '红与黑', 'author': '司汤达', 'publisher': '人民文学出版社', 'category': categories['名家代表作榜'],
         'price': 42.0, 'description': '19世纪法国批判现实主义文学的代表作，讲述于连的个人奋斗与社会冲突。',
         'tags': '批判现实主义,法国文学', 'difficulty_level': '进阶级', 'target_audience': '通用', 'score': 8.8,
         'likes': 987, 'book_status': '已完结', 'word_count': 520000, 'last_update': datetime.now()},

        {'title': '呼啸山庄', 'author': '艾米莉·勃朗特', 'publisher': '人民文学出版社',
         'category': categories['冷门高分榜'],
         'price': 39.0, 'description': '希斯克利夫与凯瑟琳的悲剧爱情，充满哥特式氛围，被誉为英国文学中最伟大的小说之一。',
         'tags': '哥特,复仇,爱情', 'difficulty_level': '进阶级', 'target_audience': '通用', 'score': 8.9, 'likes': 876,
         'book_status': '已完结', 'word_count': 135000, 'last_update': datetime.now()},

        {'title': '变形记', 'author': '卡夫卡', 'publisher': '上海译文出版社', 'category': categories['冷门高分榜'],
         'price': 34.0, 'description': '卡夫卡的代表作，讲述格里高尔·萨姆沙变成甲虫的故事，反映现代人的异化与孤独。',
         'tags': '荒诞,隐喻,现代主义', 'difficulty_level': '进阶级', 'target_audience': '通用', 'score': 8.8,
         'likes': 765, 'book_status': '已完结', 'word_count': 25000, 'last_update': datetime.now()},
    ]

    # 导入图书数据
    imported_count = 0
    for book_data in books_data:
        try:
            # 检查是否已存在
            book, created = Book.objects.update_or_create(
                title=book_data['title'],
                author=book_data['author'],
                defaults=book_data
            )
            if created:
                imported_count += 1
                print(f"✓ 添加图书: 《{book_data['title']}》 - {book_data['author']}")
            else:
                print(f"✓ 更新图书: 《{book_data['title']}》 - {book_data['author']}")
        except Exception as e:
            print(f"✗ 操作失败《{book_data['title']}》: {e}")

    print(f"\n{'=' * 50}")
    print(f"✅ 数据导入完成！")
    print(f"📊 统计信息:")
    print(f"   共导入/更新图书: {imported_count} 本")
    print(f"   数据库总图书数: {Book.objects.count()} 本")
    print(f"   数据库总分类数: {Category.objects.count()} 个")
    print(f"{'=' * 50}")

    # 显示每个分类的图书数量
    print(f"\n📚 分类图书统计:")
    for category_name, category_obj in categories.items():
        count = Book.objects.filter(category=category_obj).count()
        if count > 0:
            print(f"   {category_name}: {count} 本")


if __name__ == '__main__':
    import_data()