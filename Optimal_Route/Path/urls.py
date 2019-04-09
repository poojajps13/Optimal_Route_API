from django.urls import path
from .views import Add_Delivery,login,Route
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
	path('api/delivery',Add_Delivery.as_view()),
	path('api/login', login),
	path('api/route/<delivery_date>',Route.as_view()),
	#path('api/map',Map),
]