from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('search_cocktails/', views.search_cocktails, name='search_cocktails'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>/', views.PostLike.as_view(), name='post_like'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/like/', views.CommentLikeView.as_view(), name='like_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
]
