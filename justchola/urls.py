
from django.urls import path
from justchola import views

urlpatterns = [
     path('', views.home, name='home'),
     path('nav/', views.nav, name='nav'),
     path('purchase/', views.purchase, name='purchase'),
     path('checkout/', views.checkout, name='checkout'),
     path('handlerequest/', views.handlerequest, name="HandleRequest"),
     # path('about', views.about, name="AboutUs"),
     # path('contactus',views.contactus,name='contactus'),
     # path('tracker', views.tracker, name="TrackingStatus"),
     # path('products/<int:myid>', views.productView, name="ProductView"),
     # path("flutterwave_redirect", views.flutterwave_redirect, name="flutterwave_redirect"),
    
]
