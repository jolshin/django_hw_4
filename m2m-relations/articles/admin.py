from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        count_main_tag = 0
        tags = []
        for form in self.forms:
            
            is_main = form.cleaned_data.get('is_main')
            if is_main == True:
                count_main_tag += 1
            
            tag = form.cleaned_data.get('tag')
            if tag in tags:
                raise ValidationError('Повторяющийся тэг')
            elif tag != None:
                tags.append(tag)

        if count_main_tag != 1:
            raise ValidationError('Выберите 1 основной тэг')
        

        
        return super().clean()  # вызываем базовый код переопределяемого метода

class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 2

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline, ]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    pass
