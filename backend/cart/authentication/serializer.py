from rest_framework import serializers
from .models import Cart, Address

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Calculate final_price based on your logic
        final_price = instance.quantity * instance.total_price
        representation['final_price'] = final_price
        return representation




class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'zipcode']
