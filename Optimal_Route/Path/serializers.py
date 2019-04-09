from rest_framework import serializers
from .models import Deliveries

class DeliveriesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Deliveries
		#fields = ('name','address','lat','lng','delievery_date','status')
		fields = '__all__'