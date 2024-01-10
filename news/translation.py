from modeltranslation.translator import register, TranslationOptions
from .models import Newa, Category

@register(Newa)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
