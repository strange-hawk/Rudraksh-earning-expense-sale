from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name="sales"),
    path('sale/add-sale', views.add_sale, name='add-sale'),
    path('sale/edit-sale/<int:id>', views.edit_sale, name='edit-sale'),
    path('sale/delete-sale/<int:id>', views.delete_sale, name='delete-sale'),
    path("sale/search-sales", csrf_exempt(views.search_sales), name='search-sales')
]