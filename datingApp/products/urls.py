from django.urls import path
from products.views import ParseCategories, ParseCategory

urlpatterns = [
    path('parse/categories/', ParseCategories.as_view()),
    path('parse/category/<str:slug>/', ParseCategory.as_view()),
]
