from taleoftiles.models import Tag, Publication, Icon
from modeltranslation.translator import register, TranslationOptions

@register(Tag)
class TagTranslation(TranslationOptions):
    fields = ('name', 'summary')

# @register(Publication)
# class TagTranslation(TranslationOptions):
#     fields = ('title', 'content')


# @register(Icon)
# class IconTranslation(TranslationOptions):
#     fields = ('name', 'description')