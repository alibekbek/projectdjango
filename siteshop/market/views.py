from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from .utils import top_selling_items_pm

from market.models import Customer, Category, TagPost, Item, SellingInfo

menu = [{'title': "Главная", 'url_name': 'home'},
        {'title': "Заказчики", 'url_name': 'home'},
        {'title': "Список товаров", 'url_name': 'items'},
        {'title': "Аналитика", 'url_name': 'analysis'},
        # {'title': "Войти", 'url_name': 'login'}
        ]


def index(request):
    posts = Customer.published.all().select_related('cat')
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'market/index.html', context=data)


def about(request):
    return render(request, 'market/about.html', {'title': 'О сайте', 'menu': menu})


def show_post(request, post_slug):
    post = get_object_or_404(Customer, slug=post_slug)
    data = {
        'name': post.name,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'market/post.html', data)


def addpage(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Customer.published.filter(cat_id=category.pk).select_related('cat')
    data = {
        'title': f'Рубрика {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': cat_slug,
    }
    return render(request, 'market/index.html', context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Customer.Status.PUBLISHED).select_related('cat')

    data = {
        'title': f"Тег: {tag.tag}",
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'market/index.html', context=data)


def items_view(request):
    items = Item.objects.all()
    data = {
        'title': 'Товары',
        'menu': menu,
        'items': items
    }
    return render(request, 'market/items.html', context=data)


def show_items(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)
    data = {
        'title': item.name,
        'menu': menu,
        'item': item,

    }
    return render(request, 'market/item.html', context=data)


def analysis(request):
    customer_spending_per_month = (
        SellingInfo.objects
        .annotate(year=ExtractYear('date'), month=ExtractMonth('date'))
        .values('customer__name', 'year', 'month')
        .annotate(total_spent=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField())))
        .order_by('customer__name', 'year', 'month')
    )

    shipper_earning_per_month = (
        SellingInfo.objects
        .values('shipper__name', 'date__year', 'date__month')
        .annotate(total_earned=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField())))
        .order_by('shipper__name', 'date__year', 'date__month')
    )

    top_items_pm = top_selling_items_pm()

    data = {
        'name': 'Аналитика',
        'menu': menu,
        'customer_spending_per_month': customer_spending_per_month,
        'shipper_earning_per_month': shipper_earning_per_month,
        'top_items_pm': top_items_pm,

    }

    return render(request, 'market/analysis.html', data)


def page_not_found(request, exception):
    return HttpResponseNotFound("Страница не найдена")
