from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tag, Scope


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'published_at']
    list_filter = ['published_at', ]


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_tags_count = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                main_tags_count += 1
        if main_tags_count > 1:
            raise ValidationError('Основных разделов не может быть более одного!')
        elif main_tags_count == 0:
            raise ValidationError('Должен быть хотя бы 1 основной раздел!')
        return super().clean()


class RelationshipInline(admin.TabularInline):
    model = Scope
    extra = 2
    formset = RelationshipInlineFormset


@admin.register(Tag)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',]
    list_filter = ['name',]
    inlines = [RelationshipInline]
