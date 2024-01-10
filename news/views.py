from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from hitcount.views import HitCountDetailView

from .models import Newa, Category
from .forms import FormContact, CommentForm
from account.models import ProfileUser
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView, CreateView
from config.user_permission import OnlyLoggedSuperUser

# Create your views here.
class NewsList(ListView):
    model = Newa
    template_name = 'newslist.html'
    context_object_name = 'news'
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(status=Newa.Status.published)


class DetailNew(HitCountDetailView, DetailView):
    model = Newa
    template_name = 'new.html'
    context_object_name = 'new'
    slug_url_kwarg = 'news_slug'
    count_hit = True

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.new = self.get_object()
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
            return HttpResponseRedirect(self.request.path_info)
        else:
            return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['comments']=self.object.comments.filter(is_activ=True)
        context['comment_form']=CommentForm()
        return context




def news_detail(request, news_slug):
    print(news_slug)
    news=get_object_or_404(Newa, slug=news_slug, status=Newa.Status.published)
    comments=news.comments.filter(is_activ=True)
    new_comment=None
    if request.method=="POST":
        comment_form=CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.new=news
            new_comment.user=request.user
            new_comment.save()
            comment_form=CommentForm()
    else:
        comment_form=CommentForm()
    context={
            'new':news,
            'comments':comments,
            'new_comment':new_comment,
            'commet_form':comment_form,
        }

    return render(request, 'new.html', context=context)


class LocalNewsView(ListView):
    model = Newa
    template_name = 'localNew.html'
    context_object_name = 'localNews'

    def get_queryset(self):
       return self.model.pulished.all().filter(category__name='Mahalliy').order_by('-publish_time')



def homePageView(request):
    news=Newa.pulished.all().order_by('publish_time')[:10]
    category=Category.objects.all()
    context = {
        "news": news,
        "category": category,
    }
    return render(request, 'index.html', context=context)

class HomePageView(ListView):
    model = Newa
    template_name = 'index.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        context['news'] = Newa.pulished.all().order_by('-publish_time')[:10]
        context['category'] = Category.objects.all()
        news_comments = {}
        for news in context['news']:
            news_comments[news.id] = news.comments.filter(is_activ=True).count()
        print(news_comments)
        context['news_comments'] = news_comments
        return context


        # def contactForm(request):
#     form = FormContact(request.POST or None)
#     if request.method=="POST" and form.is_valid():
#         form.save()
#         return HttpResponse("<h2>Biz bilan bog'landingiz</h2>")
#     context = {
#         "form": form
#     }
#     return render(request, "base.html", context=context)

class ContactView(TemplateView):
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        form=FormContact()
        context ={
            "form" : form,
        }
        return render(request, 'base.html', context=context)
    def post(self, request, *args, **kwargs):
        form = FormContact(request.POST)
        if request.method=="POST" and form.is_valid():
            form.save()
            return HttpResponse("<h2>Biz bilan bo'g'langaningiz uchun rahmat!")
        context = {
            "form":form
        }
        return render(request, 'base.html', context=context)



class EditNews(UpdateView):
    model = Newa
    context_object_name = 'new'
    fields = (
    'title', 'title_uz', 'title_en', 'title_ru', 'text', 'text_uz', 'text_en', 'text_ru', 'image', 'category', 'status')


    template_name = 'crud/editNews.html'
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.slug = slugify(instance.title)
        instance.save()
        return redirect(instance.get_absolute_url())


class DeleteNews(OnlyLoggedSuperUser, DeleteView):
    model = Newa
    context_object_name = 'new'
    template_name = 'crud/deleteNews.html'
    success_url = reverse_lazy('home_page')


class CreateNews(OnlyLoggedSuperUser, CreateView):
    model = Newa
    fields = ('title', 'title_uz', 'title_en', 'title_ru','text','text_uz', 'text_en', 'text_ru', 'image', 'category','status')
    template_name = 'crud/createNew.html'
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.slug = slugify(instance.title)
        instance.save()
        return redirect(instance.get_absolute_url())

@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_list(request):
     admin_users=User.objects.filter(is_superuser=True)
     profile=ProfileUser.objects.filter(user__is_superuser=True)

     context={
         'admin':admin_users,
     }
     return render(request, 'pages/admin_page.html', context=context)


class SearchResultsList(ListView):
    model = Newa
    template_name = 'search_result.html'
    context_object_name = 'allnews'

    def get_queryset(self):
        query=self.request.GET.get('q')
        return Newa.object.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
        )
