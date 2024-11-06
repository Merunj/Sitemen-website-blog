from audioop import reverse
from winreg import CreateKey

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.transaction import commit
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from django.core.cache import cache

from .forms import AddPostForm, UploadFileForm
from .models import Men, Category, TagPost
from .utils import DataMixin


class MenHome(DataMixin, ListView):
    template_name = 'men/index.html'
    context_object_name = 'posts'
    title_page = "Главная страница"
    cat_selected = 0

    def get_queryset(self):
        m_lst = cache.get("men_posts")
        if not m_lst:
            m_lst = Men.published.all().select_related('cat')
            cache.set('men_posts', m_lst, 60)
        return m_lst

@login_required
def about(request):
    contact_list = Men.published.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'men/about.html', {'title': "О сайте", 'page_obj': page_obj})


class ShowPost(DataMixin, DetailView):
    model = Men
    template_name = 'men/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Men.published, slug=self.kwargs[self.slug_url_kwarg])

class AddPage(PermissionRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'men/addpage.html'
    success_url = reverse_lazy('home')
    title_page = "Добавление статьи"
    permission_required = 'men.add_men'

    def form_valid(self, form):
        m = form.save(commit=False)
        m.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Men
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'men/addpage.html'
    success_url = reverse_lazy('home')
    title_page = "Редактирование статьи"
    permission_required = 'men.change_men'

    def get_queryset(self):
        return Men.objects.filter(author=self.request.user)



class DeletePage(PermissionRequiredMixin, DataMixin, DeleteView):
    model = Men
    success_url = reverse_lazy('home')
    context_object_name = 'post'
    title_page = "Удаление статьи"
    permission_required = 'men.delete_men'


class MenCategory(DataMixin, ListView):
    template_name = 'men/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Men.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title="Категория" + cat.name, cat_selected=cat.id)


class TagPostList(DataMixin, ListView):
    template_name = 'men/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title="Тег: " + tag.tag)

    def get_queryset(self):
        return Men.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
