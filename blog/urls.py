from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostList.as_view(), name="home"),
    path("delete-account/", views.delete_account, name="delete_account"),
    path("<slug:slug>/", views.PostDetail.as_view(), name="post_detail"),
    path("like/<slug:slug>/", views.PostLike.as_view(), name="post_like"),
    path("comment/<int:pk>/delete/", views.CommentDelete.as_view(), name="comment_delete"),
    path('comment/<int:comment_id>/like/', views.CommentLikeView.as_view(), name='like_comment'),
    path("search_cocktails/", views.search_cocktails, name="search_cocktails"),
]

# from . import views
# from django.urls import path

# urlpatterns = [
#     path('', views.PostList.as_view(), name='home'),
#     path('delete-account/', views.delete_account, name='delete_account'),
#     path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
#     path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
#     path('search_cocktails', views.search_cocktails, name='search-cocktails'),
# ]
