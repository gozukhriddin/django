from .models import Newa

def latest_news(request):
    latest_news=Newa.pulished.all().order_by('-publish_time')[:10]

    context= {
        "latest_news":latest_news
    }
    return context