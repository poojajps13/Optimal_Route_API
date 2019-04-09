from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Deliveries
from .serializers import DeliveriesSerializer
from rest_framework import generics
import geocoder
import datetime
from math import sin, cos, sqrt, atan2, radians
import tsp 
#import folium 

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'}, status = HTTP_400_BAD_REQUEST)
    user = authenticate(username = username, password = password)
    if not user:
        return Response({'error': 'Invalid Credentials'}, status = HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user = user)
    return Response({'token': token.key}, status = HTTP_200_OK)

"""def Map(request):
	return render(request,'my_map.html')"""
	
class Add_Delivery(APIView):
	def get(self, request):
		delivery = Deliveries.objects.all()
		serializer = DeliveriesSerializer(delivery, many = True)
		return Response(serializer.data)
	def post(self, request, *args, **kwargs):
		a_delivery = Deliveries.objects.create(
			name = request.data["name"],
			address = request.data["address"],
			lat = request.data["lat"],
			lng = request.data["lng"],
			delivery_date = request.data["delivery_date"],
			status = request.data["status"],
			)
		return Response(
            data = DeliveriesSerializer(a_delivery).data,
            status = status.HTTP_201_CREATED
        )


class Route(APIView):
	def get(self, request, delivery_date):
		try:
			datetime.datetime.strptime(delivery_date,'%Y-%m-%d')
			g = geocoder.ip('me') 
			route = Deliveries.objects.filter(delivery_date = delivery_date, status = "pending")
			if not route:
				return Response({'success': 'No pending delivery for today'}, status = HTTP_200_OK)
			else :
				size = route.count()
				latitude = {}
				latitude[0] = g.latlng[0]
				i=1
				for r in route:
					latitude[i]=r.lat
					i=i+1
				longitude = {}
				longitude[0] = g.latlng[1]
				i=1
				for s in route:
					longitude[i]=s.lng
					i=i+1
				Addr = {}
				i=1
				for t in route:
					Addr[i]=[t.name,t.address]
					i=i+1
				R = 6373.0
				Matrix = [[0 for x in range(0,size+1,1)] for y in range(0,size+1,1)]
				for i in range(0,size+1,1):
					for j in range(0,size+1,1):
						if i!=j:
							latitude[i] = float(latitude[i])
							latitude[j] = float(latitude[j])
							longitude[i] = float(longitude[i])
							longitude[j] = float(longitude[j])
							lat1 = radians(latitude[i])
							lon1 = radians(longitude[i])
							lat2 = radians(latitude[j])
							lon2 = radians(longitude[j])
							dlon = lon2 - lon1
							dlat = lat2 - lat1
							a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
							c = 2 * atan2(sqrt(a), sqrt(1 - a))
							Matrix[i][j] = R * c
				r = range(0,size+1,1)
				dist = {(i, j): Matrix[i][j] for i in r for j in r}
				rout = tsp.tsp(r, dist)
				rout = rout[1]
				"""my_map = folium.Map(location = [latitude[0],longitude[0]],zoom_start = 12)
				for i in range(0,size+1,1):
					folium.Marker([latitude[i], longitude[i]]).add_to(my_map)
				for i in range(0,size,1):
					folium.PolyLine(locations = [(latitude[i], longitude[i]), (latitude[i+1], longitude[i+1])]).add_to(my_map)
				my_map.save("my_map.html")"""
				my_obj_list = []
				for i in rout:
					if(i!=0):
						my_obj_list.append({"name":Addr[i][0], "address":Addr[i][1]})
				return Response(my_obj_list)
		except ValueError:
			return Response({'error': 'Incorrect data format, should be YYYY-MM-DD'}, status = HTTP_400_BAD_REQUEST)




