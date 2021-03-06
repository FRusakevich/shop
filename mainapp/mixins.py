from django.views.generic.detail import SingleObjectMixin
from .models import Category, UnderWear, HomeWear


class CategoryDetailMixins(SingleObjectMixin):

    CATEGORY_SLUG2PRODUCT_MODEL = {
        'underwear': UnderWear,
        'homewear': HomeWear
    }

    def get_context_data(self, **kwargs):
        if isinstance(self.get_object(), Category):
            model = self.CATEGORY_SLUG2PRODUCT_MODEL[self.get_object().slug]
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.get_categories_for_left_sidebar()
            context['category_products'] = model.objects.all()
            return context
        else:
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.get_categories_for_left_sidebar()
            return context
