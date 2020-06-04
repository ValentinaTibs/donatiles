from taleoftiles.models import Tag, Publication
from layout.models import MailTemplate, Element
from modeltranslation.translator import register, TranslationOptions


@register(Element)
class ElementTranslationOptions(TranslationOptions):
    fields = ('content', )
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