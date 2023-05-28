from django.shortcuts import *
from django.contrib.postgres.search import *
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.db.models import Q
from .models import Post, Comment, CommentLike
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from allauth.account.views import LogoutView
from django.contrib import messages


@login_required
def delete_account(request):
    """
    Deletes the user account.
    """
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('account_logout')
    else:
        return render(request, 'delete_account.html')


def search_cocktails(request):
    """
    Handles the search functionality for cocktails.
    """
    if request.method == "POST":
        q = request.POST['q']
        vector = SearchVector('title', 'content')
        query = SearchQuery(q)
        search_headline = SearchHeadline('content', query)

        # Perform the search using PostgreSQL full-text search features
        cocktails = Post.objects.annotate(search=vector).annotate(
            headline=search_headline).filter(search=query)

        return render(
            request, 'search_cocktails.html', {'q': q, 'cocktails': cocktails})
    else:
        return render(request, 'search_cocktails.html', {})


class PostList(generic.ListView):
    """
    Displays a list of blog posts.
    """
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 21


class PostDetail(View):
    """
    Displays the details of a blog post and handles comments.
    """
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.order_by("-created_on")
        liked = False

        if post.likes.filter(id=request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.order_by("-created_on")
        liked = False

        if post.likes.filter(id=request.user.id).exists():
            liked = True

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.save()
                return redirect('post_detail', slug=slug)
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "comment_form": comment_form,
                "liked": liked,
            },
        )


@login_required
def edit_comment(request, comment_id):
    """
    Edits a comment.
    """
    comment = get_object_or_404(Comment, id=comment_id)

    if not request.user.is_superuser and request.user != comment.user:
        messages.error(
            request, 'You do not have permission to edit this comment.')
        return redirect('post_detail', slug=comment.post.slug)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'The comment has been updated.')
            return redirect('post_detail', slug=comment.post.slug)
    else:
        form = CommentForm(instance=comment)

    return render(
        request, 'edit_comment.html',
        {'form': form, 'slug': comment.post.slug, 'comment': comment})


@login_required
def delete_comment(request, comment_id):
    """
    Deletes a comment.
    """
    comment = get_object_or_404(Comment, id=comment_id)

    if not request.user.is_superuser and request.user != comment.user:
        messages.error(
            request, 'You do not have permission to delete this comment.')
        return redirect('post_detail', slug=comment.post.slug)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'The comment has been deleted!')

    return redirect('post_detail', slug=comment.post.slug)


class PostLike(View):
    """
    Handles the like functionality for blog posts.
    """
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class CommentLikeView(View):
    """
    Handles the like functionality for comments.
    """
    def post(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
        comment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
