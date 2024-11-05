from django.urls import path

from common.views import landing_page, home_page

app_name = 'common'
urlpatterns = [
    path('', landing_page, name="landing_page"),
    path('home/', home_page, name='home_page'),
]
