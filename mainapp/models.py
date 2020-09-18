from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


# mainpage
class LatestProductsManager:

    def get_products_for_main_page(self, *args, **kwargs):
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        return products


class LatestProducts:
    object = LatestProductsManager()


class CategoryManager(models.Manager):
    CATEGORY_NAME_COUNT_NAME = {
        'Домашняя одежда': 'homewear__count',
        'Нижнее бельё': 'underwear__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('underwear', 'homewear')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        print(data)

        return data


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категориия', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title


class UnderWear(Product):
    under_wear_type = models.CharField(max_length=50, verbose_name='Тип(низ/верх)')
    size = models.IntegerField(verbose_name='Размер')
    capacity = models.IntegerField(verbose_name='Объем')
    letter = models.CharField(max_length=5, verbose_name='Размерная буква')
    color = models.CharField(max_length=20, verbose_name='Цвет')

    def __str__(self):
        return f"{self.category.name} {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class HomeWear(Product):
    home_wear_type = models.CharField(max_length=50, verbose_name='Тип(пижама/шорты/майка)')
    size = models.IntegerField(verbose_name='Размер')
    growth = models.IntegerField(verbose_name='Рост')
    color = models.CharField(max_length=20, verbose_name='Цвет')

    def __str__(self):
        return f"{self.category.name} {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')




