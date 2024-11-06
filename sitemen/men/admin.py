from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Men, Category

class MarriedFilter(admin.SimpleListFilter):
    title = "Статус мужчины"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [
            ('married', "Женат"),
            ('single', "Не женат")
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(wife__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(wife__isnull=True)


@admin.register(Men)
class MenAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'wife', 'tags']
    prepopulated_fields = {'slug': ('title', )}
    filter_horizontal = ['tags']
    list_display = ('title', 'post_photo', 'time_create', 'photo', 'is_published', 'cat', 'author')
    list_display_links = ('title', )
    ordering = ['time_create', 'title']
    list_editable = ('is_published', )
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title']
    list_filter = [MarriedFilter, 'cat__name', 'is_published']
    save_on_top = True

    @admin.display(description="Фото", ordering='title')
    def post_photo(self, men: Men):
        if men.photo:
            return mark_safe(f"<img src='{men.photo.url}' width=50>")
        else:
            return "Без фото"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Men.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Men.Status.DRAFT)
        self.message_user(request, f"{count} записей снято с публикации!", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
