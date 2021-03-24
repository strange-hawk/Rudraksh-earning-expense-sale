from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name="earning"),
    path('add-earning/', views.add_earning, name='add-earning'),
    path('edit-earning/<int:id>', views.edit_earning, name='edit-earning'),
    path('delete-earning/<int:id>', views.delete_earning, name='delete-earning'),
    path("search-earnings", csrf_exempt(views.search_earnings), name='search-earnings')
]