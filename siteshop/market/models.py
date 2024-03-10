from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Customer.Status.PUBLISHED)


class Customer(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    comment = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT)
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')
    owner = models.OneToOneField('Owner', on_delete=models.SET_NULL, null=True, blank=True, related_name="owner")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Заказчики"
        verbose_name_plural = "Заказчики"
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = "Категория заказчика"
        verbose_name_plural = "Категории заказчиков"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Owner(models.Model):
    name = models.CharField(max_length=100)
    iin = models.BigIntegerField(null=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255)
    item_type = models.ForeignKey('ItemType', on_delete=models.SET_NULL, null=True, blank=True, related_name="item_type")
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def get_absolute_url(self):
        return reverse('item', kwargs={'item_slug': self.slug})


class ItemType(models.Model):
    typename = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"

    def __str__(self):
        return self.typename


class Price(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    shipper = models.ForeignKey('Shipper', on_delete=models.CASCADE, related_name="company", blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="prices")

    class Meta:
        verbose_name = "Цена"
        verbose_name_plural = "Цены на товары"
        unique_together = ['shipper', 'item']

    def __str__(self):
        return f"{self.item.name} - {self.shipper.name} - {self.value}"


class Shipper(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SellingInfo(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Получаем цену для данного товара и данного поставщика
        price_object = Price.objects.get(item=self.item, shipper=self.shipper)
        self.price = price_object.value
        super().save(*args, **kwargs)

    def total_price(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Покупки"

    def __str__(self):
        return f"{self.customer.name} - {self.item.name} - {self.shipper.name}"

