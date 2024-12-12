# flashcards/admin.py

from django.contrib import admin
from .models import FlashcardSet, Flashcard, Collection, SetLimit, User, HiddenCard, QuizAttempt
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('is_admin',)}),
    )
    list_display = ('username', 'is_admin', 'is_staff', 'is_superuser')

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('question', 'difficulty', 'hidden')
    list_filter = ('difficulty', 'hidden')
    search_fields = ('question', 'answer')

@admin.register(FlashcardSet)
class FlashcardSetAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'rating', 'user')
    search_fields = ('name', 'user__username')
    filter_horizontal = ('cards',)

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username')
    filter_horizontal = ('sets',)

@admin.register(SetLimit)
class SetLimitAdmin(admin.ModelAdmin):
    list_display = ('limit',)
    actions = ['set_new_limit']

    def set_new_limit(self, request, queryset):
        new_limit = request.POST.get('new_limit')
        if new_limit and new_limit.isdigit():
            for limit in queryset:
                limit.limit = int(new_limit)
                limit.save()
            self.message_user(request, "Set limit updated successfully.")
        else:
            self.message_user(request, "Invalid limit value.", level='error')
    set_new_limit.short_description = "Set new daily set creation limit"

@admin.register(HiddenCard)
class HiddenCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'card', 'hidden_at')
    search_fields = ('user__username', 'card__question')

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'flashcard_set', 'attempt_time', 'completion_time')
    search_fields = ('user__username', 'flashcard_set__name')
    list_filter = ('flashcard_set',)
