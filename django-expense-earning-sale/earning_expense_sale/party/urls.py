from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="party"),
    path('add-party', views.add_party, name="add-party"),
    path('edit-party/<int:id>', views.edit_party, name="edit-party"),
    path('delete-party/<int:id>', views.delete_party, name='delete-party'),
    path("search-party/", csrf_exempt(views.search_parties), name='search-parties'),
    path("export-pdf", views.export_pdf, name="export-pdf")
] 
