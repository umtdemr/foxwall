from django.contrib import admin

from post.models import Post, PostImage


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline]
    search_fields = (
        "user",
        "text",
    )
    list_display = ["user", "status", "visibility", "parent"]
