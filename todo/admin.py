from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin

from .models import TODOList, TODOAction


class TODOActionInlineAdmin(SortableInlineAdminMixin, admin.StackedInline):
    model = TODOAction
    extra = 1

    prepopulated_fields = {'slug': ('title',)}
    exclude = ('order',)


@admin.register(TODOList)
class TODOListAdmin(SortableAdminMixin, admin.ModelAdmin):
    inlines = [TODOActionInlineAdmin]
    prepopulated_fields = {'slug': ('title',)}
