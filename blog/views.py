from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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


class PostListview(ListView):
    model = Post
    # <app>/<model>_<viewtype>.html
    template_name ='blog/home.html'
    # same var name as above. So that template knows what object to use
    context_object_name = 'posts'
    # "-" sign to list posts from newest to oldest instead of old -> new.
    ordering = ['-date_posted']


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
