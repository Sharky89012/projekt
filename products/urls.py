from django.urls import path
from . import views
from .views import ArtikelBeschreibungAPI

urlpatterns = [
    path('', views.home_view, name='home'),
    path('index.html', views.home_view, name='index'),
    path('about', views.about_view, name='about'),
    path('details', views.detail_page_view, name='details_pages'),
    path('listings', views.listing_page_view, name='details_listing'),
    path('search/', views.search_page, name='search_page'),
    path('api/search/', views.search_api_view, name='search_api_view'),
    path('artikel/<int:artikel_id>/', views.artikel_detail_page, name='artikel_detail_page'),
    path('api/artikel/<int:artikel_id>/', views.artikel_detail_api, name='artikel_detail_api'),
    path('kategorie/<str:kategorie_name>/', views.kategorie_page, name='kategorie_page'),
    path('api/kategorie/<str:kategorie_name>/', views.kategorie_api_view, name='kategorie_api'),
    path('api/top-saving/<int:position>/', views.get_top_saving, name='top_saving'),
    path('api/top-savings-all/', views.all_sorted_savings_view, name='top_savings_all'),
    path('all-produkt24/', views.all_produkt24_view, name='all_produkt24'),
    path('api/all-produkte-sorted/', views.api_all_produkte_sorted_by_saving, name='all_produkte_sorted'),
    path('sitemap.xml', views.sitemap_view, name='sitemap'),
    path('api/subscribe/', views.subscribe_email, name='subscribe_email'),
    path('api/artikel/<int:artikel_id>/', ArtikelBeschreibungAPI.as_view(), name='artikel-beschreibung-api'),
    path('datenschutz', views.datenschutz, name='datenschutz'),



]

