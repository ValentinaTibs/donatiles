from taleoftiles.models import Tag, Publication, Icon
from layout.models import MailTemplate
from modeltranslation.translator import register, TranslationOptions

@register(Tag)
class TagTranslation(TranslationOptions):
    fields = ('name', 'summary')

@register(Publication)
class PubTranslation(TranslationOptions):
    fields = ('title',	'content',)

@register(MailTemplate)
class MailTranslation(TranslationOptions):
    fields = ('subj','content',)



# @register(Icon)
# class IconTranslation(TranslationOptions):
#     fields = ('name', 'description')