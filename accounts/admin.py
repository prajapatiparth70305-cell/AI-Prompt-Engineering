from django.contrib import admin

from .models import PromptHistory, PromptTemplate


@admin.register(PromptHistory)
class PromptHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "category",
        "is_favorite",
        "created_at",
    )

    list_filter = (
        "category",
        "is_favorite",
        "created_at",
    )

    search_fields = (
        "original_prompt",
        "optimized_prompt",
        "user__username",
    )

    ordering = (
        "-created_at",
    )


@admin.register(PromptTemplate)
class PromptTemplateAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "category",
        "is_active",
        "created_at",
    )

    list_filter = (
        "category",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
        "template",
    )

    ordering = (
        "-created_at",
    )