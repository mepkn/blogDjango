from django.contrib import admin

from .models import Comment, Post


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "short_body",
        "author",
    ]
    inlines = [
        CommentInline,
    ]

    def short_body(self, obj):
        words = obj.body.split()
        if len(words) <= 25:
            return obj.body
        else:
            return " ".join(words[:25]) + "..."

    short_body.short_description = "Body"


admin.site.register(Comment)
admin.site.register(Post, PostAdmin)
