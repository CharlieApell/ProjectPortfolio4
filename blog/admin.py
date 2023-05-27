from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Admin configuration for the Post model.
    """
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Comment model.
    """
    list_display = ('user', 'name', 'body', 'post', 'created_on')
    search_fields = ('user__username', 'name', 'body')

    def save_model(self, request, obj, form, change):
        """
        Custom save method to associate the user with the comment.
        """
        if not obj.user_id:
            obj.user = request.user
        obj.save()
