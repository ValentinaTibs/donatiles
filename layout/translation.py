from layout.models import ElementTag
from modeltranslation.translator import register, TranslationOptions

@register(ElementTag)
class ElementTagTranslationOptions(TranslationOptions):
    fields = ('name', 'summary', )
