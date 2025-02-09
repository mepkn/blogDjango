from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from blog.forms import CommentForm, PostForm

from .models import Post


class BlogListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "home.html"
    paginate_by = 9

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(Q(is_public=True) | Q(author=user)).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.get_queryset()
        paginator = Paginator(posts, self.paginate_by)
        page = self.request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context["posts"] = posts
        context["page_obj"] = posts
        return context


class CommentGet(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_queryset(self):
        return Post.objects.filter(Q(is_public=True) | Q(author=self.request.user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentPost(SingleObjectMixin, FormView):
    model = Post
    form_class = CommentForm
    template_name = "blog/post_detail.html"

    def get_queryset(self):
        return Post.objects.filter(Q(is_public=True) | Q(author=self.request.user))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.is_public and self.object.author != request.user:
            return HttpResponseForbidden("You are not authorized to view this post.")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        post = self.object
        return reverse("post_detail", kwargs={"pk": post.pk})


class BlogDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])
        if not post.is_public and post.author != request.user:
            return HttpResponseForbidden("You are not authorized to view this post.")
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])
        if not post.is_public and post.author != request.user:
            return HttpResponseForbidden("You are not authorized to view this post.")
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/post_new.html"
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "blog/post_edit.html"
    form_class = PostForm

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class TogglePostVisibilityView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return HttpResponseForbidden(
                "You are not authorized to change the visibility of this post."
            )
        post.is_public = not post.is_public
        post.save()
        return redirect(reverse("post_detail", kwargs={"pk": post.pk}))
