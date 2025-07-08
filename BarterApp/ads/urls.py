from django.urls import path

from .views import (main_page,
                    create_ad,
                    ad_page,
                    rm_ad,
                    update_ad,
                    create_trade,
                    trade_page,
                    update_trade_status)

app_name = 'main'

urlpatterns = [
    path('',
         view=main_page,
         name='index'),
    path('<int:id>/',
         view=ad_page,
         name='detail'),
    path('createad/',
         view=create_ad,
         name='createform'),
    path('delete/<int:id>/',
         view=rm_ad,
         name='delete_ad'),
    path('update/<int:id>/',
         view=update_ad,
         name='update_ad'),
    path('<int:id>/createtrade/',
         view=create_trade,
         name='create_trade'),
    path('trades/',
         view=trade_page,
         name='trade'),
    path('<int:id>/updatetrade/',
         view=update_trade_status,
         name='update_trade')
]
