from django.db import models


class CategoryFeature(models.Model):
    """
    Характеристика конкретной категории
    """
    category = models.ForeignKey('mainapp.Category', verbose_name='Категория', on_delete=models.CASCADE)
    feature_name = models.CharField(max_length=100, verbose_name='Наименование характеристики') # предположим наименование характеристики будет Брэнд
    feature_filter_name= models.CharField(max_length=50, verbose_name='Имя для фильтра') # Тогда имя для фильтра будет brand.
    # Когда будет поиск товара, то для отправки Query-параметра будет использоватся feature_filter_name.
    unit = models.CharField(max_length=50, verbose_name='Единица измерения', null=True, blank=True)

    #Класс для проверки уникальности характеристик для разных товаров
    class Meta:
        unique_together = ('category', 'feature_name', 'feature_filter_name')

    def __str__(self):
        return f"{self.category.name} | {self.feature_name}"


class FeatureValidator(models.Model):
    """
    Валидатор значений для конкретной характеристики принадлежащей конкретной характеристики.
    Что бы из выпадающего списка выбирать конкретное значение характеристики.
    """

    category = models.ForeignKey(
        'mainapp.Category',
        verbose_name='Категория',
        on_delete=models.CASCADE,
    )

    feature_key = models.ForeignKey(
        CategoryFeature,
        verbose_name='Ключ характеристики',
        on_delete=models.CASCADE,
    )

    valid_feature_value = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Валидное значение',
    )

    def __str__(self):
        return f'Категория "{self.category.name}" | ' \
               f'Характеристики - "{self.feature_key.feature_name}" | ' \
               f'Значение -  "{self.valid_feature_value}" | ' \



class ProductFeatures(models.Model):
    """
    Характеристики товара
    """

    product = models.ForeignKey('mainapp.Product', verbose_name='Товар', on_delete=models.CASCADE)
    feature = models.ForeignKey(CategoryFeature, verbose_name='Характеристики', on_delete=models.CASCADE)
    value = models.CharField(max_length=255, verbose_name='Значение')

    def __str__(self):
        return f'Товар - "{self.product.title}" |' \
               f'Характеристика - "{self.feature.feature_name}" |'\
               f'Значение - {self.value} '