
from rest_framework import serializers
from .models import *




class DepositeSerializer(serializers.ModelSerializer):
	phone_number = serializers.IntegerField(required=True)
	amount 		 = serializers.DecimalField(required=True, max_digits=15, decimal_places=2, min_value=10)
	class Meta:
		model  = Transaction
		fields = [
			'id',
			'phone_number',
			'amount',
			'timestamp', 
		]
		read_only_fields = ['id', 'phone_number', 'amount', 'timestamp']





class WithdrawSerializer(serializers.ModelSerializer):
	phone_number = serializers.IntegerField(required=True)
	amount 		 = serializers.DecimalField(required=True, max_digits=15, decimal_places=2, min_value=10)
	class Meta:
		model  = Transaction
		fields = [
			'id',
			'phone_number',
			'amount',
			'timestamp', 
		]
		read_only_fields = ['id', 'phone_number', 'amount', 'timestamp']
	





