
from django.urls import path
from .views import NewsList, SearchResultsList, DetailNew, news_detail, admin_list, homePageView, ContactView, HomePageView, LocalNewsView, EditNews, DeleteNews,CreateNews

urlpatterns = [
    path("", HomePageView.as_view(), name="home_page"),
    path("adminpage/", admin_list, name='adimin_page'),
    path("searchresult/", SearchResultsList.as_view(), name='search'),
    path("contact-us/", ContactView.as_view(), name="contact"),
    path("all/", NewsList.as_view(), name='newslist'),
    path("local1/", LocalNewsView.as_view(), name='local_news'),
    path("add/", CreateNews.as_view(), name='add_new'),
    path("<slug:slug>/edit/", EditNews.as_view(), name='edit_news'),
    path("<slug:slug>/delete/", DeleteNews.as_view(), name='delete_news'),
    # path("<slug:news_slug>/", news_detail, name='newdetail'),
    path("<slug:news_slug>/", DetailNew.as_view(), name='newdetail'),
]