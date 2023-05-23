from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchHeadline
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.db.models import Q
from .models import Post
from .forms import CommentForm


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from allauth.account.views import LogoutView

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
        
        return render(request, '../templates/search_cocktails.html'
        , {'q': q, 'cocktails': cocktails})
    else:
        return render(request, '../templates/search_cocktails.html', {})


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 21


class PostDetail(View):
    

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
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
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
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


class PostLike(View):
    
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
        