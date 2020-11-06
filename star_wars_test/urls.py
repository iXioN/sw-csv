from django.urls import path

from . import views

urlpatterns = [
    path('', views.explore, name='explore'),
    path('fetch/', views.fetch, name='fetch'),
    path('collection/<int:collection_id>', views.collection, name='collection'),
    path('collection/<int:collection_id>/download', views.collection_download, name='collection_download'),

]
