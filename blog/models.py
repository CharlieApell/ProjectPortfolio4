from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.urls import reverse


STATUS = ((0, "Draft"), (1, "Published"))


class Post(models.Model):
    """
    Represents a blog post.
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blog_posts")
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User,
        related_name='blogpost_like',
        blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        """
        Returns the number of likes on the post.
        """
        return self.likes.count()

    def number_of_comments(self):
        """
        Returns the number of comments on the post.
        """
        return self.comments.count()

    def is_owner(self, user):
        """
        Checks if the user is the owner of the post.
        """
        return self.author == user


class Comment(models.Model):
    """
    Represents a comment on a blog post.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User,
        through='CommentLike',
        related_name='comment_likes',
        blank=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"

    def number_of_likes(self):
        """
        Returns the number of likes on the comment.
        """
        return self.likes.count()

    def is_liked_by_user(self):
        """
        Checks if the comment is liked by the user.
        """
        return self.likes.filter(id=self.user.id).exists()

    def is_owner(self, user):
        """
        Checks if the user is the owner of the comment.
        """
        return self.user == user


class CommentLike(models.Model):
    """
    Represents a like on a comment.
    """
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Like by {self.user.username} on {self.comment}"


class DeletedAccount(models.Model):
    """
    Represents a deleted user account.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
