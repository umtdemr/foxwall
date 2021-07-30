from django.contrib import admin


from user.models import User, UserProfile


class UserProfileInline(admin.TabularInline):
    model = UserProfile
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline]
    search_fields = ("username",)
    exclude = ("password",)
