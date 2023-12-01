from django.urls import path
from . import views

app_name = 'strategy'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('post/', views.CreatePhotoView.as_view(), name='post'),

    path('post_done/',
         views.PostSuccessView.as_view(),
         name='post_done'),

    path('strategys/<int:category>/',
         views.CategoryView.as_view(),
         name = 'strategys_cat'),

    path('user-list/<int:user>/',
         views.UserView.as_view(),
         name = 'user_list'),
    
    path('strategy-detail/<int:pk>/',
         views.DetailView.as_view(),
         name = 'strategy_detail'),

    path('mypage/', views.MypageView.as_view(), name = 'mypage'),

    path('strategy/<int:pk>/delete/',
         views.StrategyDeleteView.as_view(),
         name = 'strategy_delete'
         ),

     path('strategy/<int:pk>/update/',
         views.StrategyUpdateView.as_view(),
         name = 'strategy_update'
         ),
     path(
        'contact/',
        views.ContactView.as_view(),
        name = 'contact'
          ),

     path('strategy-detail/<int:pk>/comment/create/', 
          views.CommentCreate.as_view(), 
          name='comment_create'
          ),
     

     path('strategy-detail/<int:pk>/comment/delete/',
         views.CommentDeleteView.as_view(),
         name = 'comment_delete'
         ),

     path('strategy-detail/<int:pk>/comment/update/',
         views.CommentUpdateView.as_view(),
         name = 'comment_update'
         ),
]