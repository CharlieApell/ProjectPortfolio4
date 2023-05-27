from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchHeadline
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
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('account_logout')
    else:
        return render(request, 'delete_account.html')


def search_cocktails(request):
    if request.method == "POST":
        q = request.POST['q']
        vector = SearchVector('title', 'content')
        query = SearchQuery(q)
        search_headline = SearchHeadline('content', query)

        cocktails = Post.objects.annotate(search=vector).annotate(headline=search_headline).filter(search=query)
       
        return render(request, 'search_cocktails.html', {'q': q, 'cocktails': cocktails})
    else:
        return render(request, 'search_cocktails.html', {})


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 21


class PostDetail(View):

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

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Kommentaren har skickats.')
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
                },
            )


@login_required
def delete_comment(request, slug, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'The comment has been deleted.')
    return redirect('post_detail', slug=slug)


@login_required
def like_comment(request, comment_id, *args, **kwargs):
    comment = get_object_or_404(Comment, id=comment_id)
    like, created = CommentLike.objects.get_or_create(comment=comment, user=request.user)

    if not created:
        # Användaren har redan gillat kommentaren, ta bort gillningen
        like.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class PostLike(View):
    
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class CommentDelete(View):
    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        # Kontrollera om användaren är ägaren till kommentaren
        if comment.is_owner(request.user):
            comment.delete()
            messages.success(request, 'The comment has been deleted.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class CommentLikeView(View):
    def post(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
        comment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if not request.user.is_superuser and comment.id != request.user:
        messages.error(request, 'You do not have permission to edit this comment.')
        return redirect('post_detail', slug=comment.post.slug)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'The comment has been updated.')
            return redirect('post_detail', slug=comment.post.slug)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form, 'slug': comment.post.slug, 'comment': comment})

