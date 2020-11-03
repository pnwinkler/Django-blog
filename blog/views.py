import feedparser
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    # <app>/<model>_<viewtype>.html
    template_name = 'blog/home.html'
    # same var name as above. So that template knows what object to use
    context_object_name = 'posts'
    # "-" sign to list posts from newest to oldest instead of old -> new.
    ordering = ['-date_posted']
    paginate_by = 5


# get only X latest posts
class LatestPostsView(PostListView):
    template_name = 'blog/home.html'

    def get_queryset(self):
        return Post.objects.all().order_by('-date_posted')[:3]


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    # username var will be passed into URL. Override func
    def get_queryset(self):
        # this line is why we need "from django.contrib.auth.models import User"
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        # we're overriding the function responsible for ordering, so we remove "ordering" var from above
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # instead of redirecting to post detail, could redirect to home
    # success_url = '/'

    # override so we can set post's author to currently logged in author
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# each mixin asserts a condition, for a user to access a given view.
# mixin must be to the left of the inheritance! (namely the UpdateView)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def announcements(request):
    feed_items = feedparser.parse('https://github.com/pnwinkler/Django-blog/commits/main.atom')
    context = {'feed_items': feed_items}
    template_name = 'blog/announcements.html'
    return render(request, template_name, context)
