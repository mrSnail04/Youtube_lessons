# импорты для ограничений по разрешению изображения
# import sys
# from PIL import Image
# from django.core.files.uploadedfile import InMemoryUploadedFile
# from io import BytesIO

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse

User = get_user_model()


# Create your models here.
# 1 product
# 2 Category
# 3 cartProduct
# 4 Cart
# 5 Order


# 6 Customer
def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass


# класс позволяющий выводить на главную страницу последнюю добавленную технику
class LatestProductsManager:
    # функция достающая весь список товаров, который надо отобразить
    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        # Позволяет сортировать, какую группу техники выводить первой
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            # вызываем родительский класс у переданной модели
            # берём последние 5 штук.
            products.extend(model_products)  # расширяем наш список товаров

        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            # проверяем ли есть эта модель в найших аргументах.
            if ct_model.exists():
                if with_respect_to in args:
                    # Возвращаем отсортированый список продуктов. Обращаясь к их моделям через атрибут meta.
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:
    objects = LatestProductsManager()


class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Ноутбуки': 'notebook__count',
        'Смартфоны': 'smartphone__count',
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('notebook', 'smartphone')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    # MIN_RESOLUTION = (400, 400)
    # MAX_RESOLUTION = (800, 800)
    # MAX_IMAGE_SIZE = 3145728

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория',
                                 on_delete=models.CASCADE)  # Связь с категориями и обязательный on_delet, что бы удалять. разрывать все связи
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     # Вариант №1 предупреждение, что изображение слишком большое или слишком маленькое
    #     image = self.image
    #     img = Image.open(image)
    #     min_height, min_width = self.MIN_RESOLUTION
    #     max_height, max_width = self.MAX_RESOLUTION
    #     if img.height < min_height or img.width < min_width:
    #         raise MinResolutionErrorException('Разрешение изображение меньше минимального!')
    #     if img.height > max_height or img.width > max_width:
    #         raise MaxResolutionErrorException('Разрешение изображение больше минимального!')
    #
    #     # Вариант №2. Обрезаем изображение до 200*200, если загружается изображение больше, чем 800*800
    #     # image = self.image
    #     # img = Image.open(image)
    #     # new_img = img.convert('RGB')
    #     # # обрезаем изображение
    #     # resized_new_img = new_img.resize((200, 200), Image.ANTIALIAS)
    #     # # Преобразуем изображение в байты
    #     # filestream = BytesIO()
    #     # # Сохраняем изображение в filestream
    #     # resized_new_img.save(filestream, 'JPEG', quality=90)
    #     # # переводим ползунок при чтении объекта на 1
    #     # filestream.seek(0)
    #     # name = '{}.{}'.format(*self.image.name.split('.'))
    #     # print(self.image.name, name)
    #     # self.image = InMemoryUploadedFile(
    #     #     filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
    #     # )
    #     super().save(*args, **kwargs)


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)  # Кол-во товара
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.content_object.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.CharField(max_length=255, verbose_name='Адрес')

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


class Notebook(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    processor_freq = models.CharField(max_length=255, verbose_name='Частота процессора')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    video = models.CharField(max_length=255, verbose_name='Видеокарта')
    time_without_charge = models.CharField(max_length=255, verbose_name='Время работы аккумулятора')

    def __str__(self):
        return "{}: {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Smartphone(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    resolution = models.CharField(max_length=255, verbose_name='Разрещение экрана')
    accum_volume = models.CharField(max_length=255, verbose_name='Объем батареи')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    sd = models.BooleanField(default=True, verbose_name='Наличие SD карты')
    sd_volume_max = models.CharField(max_length=255, null=True, blank=True, verbose_name='Максимальный объем SD карты')
    main_cam_mp = models.CharField(max_length=255, verbose_name='Главная камера')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Фронтальная камера')

    def __str__(self):
        return "{}: {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

    # @property
    # def sd(self):
    #     if self.sd:
    #         return 'Да'
    #     return 'Нет'
