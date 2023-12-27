
from django.urls import path
from .views import NewsList, DetailNew, homePageView, ContactView, HomePageView, LocalNewsView

urlpatterns = [
    path("", HomePageView.as_view(), name="home_page"),
    path("contact-us/", ContactView.as_view(), name="contact"),
    path("all/", NewsList.as_view(), name='newslist'),
    path("local1/", LocalNewsView.as_view(), name='local_news'),
    path("<slug:slug>/", DetailNew.as_view(), name='newdetail'),
]