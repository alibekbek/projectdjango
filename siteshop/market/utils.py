from django.db.models import Sum
from django.db.models.functions import ExtractYear, ExtractMonth
from itertools import groupby
from operator import itemgetter

from market.models import SellingInfo


def top_selling_items_pm():
    # Получаем продажи за каждый месяц для каждого товара
    sales_per_month = (
        SellingInfo.objects
        .annotate(year=ExtractYear('date'), month=ExtractMonth('date'))
        .values('year', 'month', 'item__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('year', 'month', '-total_sold')
    )

    # Группируем результаты по году и месяцу
    grouped_sales = groupby(sales_per_month, key=itemgetter('year', 'month'))

    # Создаем список для хранения топ-3 продаваемых товаров за каждый месяц
    top_items_pm = []

    # Для каждого месяца находим топ-3 товаров
    for (year, month), sales_group in grouped_sales:
        top_items = []
        for idx, sale in enumerate(sales_group):
            if idx >= 3:  # Ограничиваемся топ-3
                break
            top_items.append(sale)
        top_items_pm.append({'year': year, 'month': month, 'top_items': top_items})

    return top_items_pm
