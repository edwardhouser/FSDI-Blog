from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    ListView,
)

from .models import Post
from django.urls import reverse_lazy

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "posts/edit.html"
    model = Post
    fields = [
        "title", "subtitle", "body", "status"
    ]

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "posts/delete.html"
    model = Post
    success_url = reverse_lazy("list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

class PostCreateView(CreateView):
    template_name = "posts/new.html"
    model = Post
    fields = [
        "title", "subtitle", "body", "status"
    ]




class PostListView(ListView):
    template_name = "posts/list.html"
    model = Post

class ArchivedPostListView(LoginRequiredMixin, ListView):
    template_name = "posts/archivedlist.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        archived = status.objects.get(name="archived")
        context["title"] = "Archived"
        context["post_list"] = (
            Post.objects
            .filter(status=archived)
            .order_by("created_on").reverse()
        )
        return context
    
class PostDetailView(DetailView):
    template_name = "posts/detail.html"
    model = Post

    def test_func(self):
        if post.status.name == "published":
            return True
        elif post.status.name == "archived" and self.request.user.is_authenticated:
            return True
        elif post.status.name == "draft" and self.request.user == post.author:
            return True
        else:
            return False