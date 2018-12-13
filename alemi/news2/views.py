from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from news.models import Post
from django.utils import timezone
from news.forms import PostForm
from braces.views import SelectRelatedMixin
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class PostListView(SelectRelatedMixin, generic.ListView):
    model = Post
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(generic.DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin, generic.CreateView):
    # form_class = forms.PostForm
    login_url = '/loginmama/'
    fields = ('title','text')
    model = Post

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,generic.UpdateView):
    login_url = '/loginmama/'
    form_class = PostForm

    model = Post


class DraftListView(LoginRequiredMixin,generic.ListView):
    model = Post
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


class PostDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = Post
    success_url = reverse_lazy('news:post_list')

#######################################
## Functions that require a pk match ##
#######################################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('news:post_detail', pk=pk)
