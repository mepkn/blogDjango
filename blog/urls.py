from django.urls import path

from .views import (
    BlogCreateView,
    BlogDeleteView,
    BlogDetailView,
    BlogListView,
    BlogUpdateView,
    TogglePostVisibilityView,
)

urlpatterns = [
    path("", BlogListView.as_view(), name="home"),
    path("post/new/", BlogCreateView.as_view(), name="post_new"),
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/edit/", BlogUpdateView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/", BlogDeleteView.as_view(), name="post_delete"),
    path(
        "post/<int:pk>/toggle_visibility/",
        TogglePostVisibilityView.as_view(),
        name="toggle_post_visibility",
    ),
]
