from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Newa, Category
from .forms import FormContact
from django.views.generic import ListView, DetailView, TemplateView


# Create your views here.
class NewsList(ListView):
    model = Newa
    template_name = 'newslist.html'
    context_object_name = 'news'
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(status=Newa.Status.published)


class DetailNew(DetailView):
    model = Newa
    template_name = 'new.html'
    context_object_name = 'new'
    slug_url_kwarg = 'slug'

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
        context['category' ] = Category.objects.all()
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







