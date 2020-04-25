from layout.models import Element
from modeltranslation.translator import register, TranslationOptions

@register(Element)
class ElementTranslationOptions(TranslationOptions):
    fields = ('content', )

