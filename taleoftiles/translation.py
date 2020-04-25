from taleoftiles.models import Tag
from modeltranslation.translator import register, TranslationOptions

@register(Tag)
class TagTranslation(TranslationOptions):
    fields = ('name', 'summary')



