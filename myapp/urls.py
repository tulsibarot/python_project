
from django.urls import path 
from . import views

urlpatterns = [
   path('',views.index,name='index'),
   path('about/',views.about,name='about'),
   path('contact/',views.contact,name='contact'),
   path('course-details/',views.coursedetails,name='course-details'),
   path('courses/',views.courses,name='courses'),
   path('events/',views.events,name='events'),
   path('pricing/',views.pricing,name='pricing'),
   path('trainers/',views.trainers,name='trainers'),
   path('registration/',views.registration,name='registration'),
   path('index/login/',views.login,name='login'),
   path('otp/',views.otp,name='otp'),
   path('buy/paymenthandler/', views.paymenthandler, name='paymenthandler'),
   path('buy/', views.buy, name="buy"),
]
