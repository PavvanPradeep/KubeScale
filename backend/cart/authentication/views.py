# views.py
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cart, Address
from .serializer import CartSerializer, AddressSerializer
from rest_framework import permissions, status
from decimal import Decimal
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class CartList(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        cart_items = Cart.objects.all()
        serializer = CartSerializer(cart_items, many=True)

        total_price = sum(Decimal(item['price']) for item in serializer.data)
        for item in serializer.data:
            item['final_price'] = total_price

        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            # Extract product_id, brand, name, and price from the request data
            product_id = request.data.get('product_id')
            brand = request.data.get('brand')
            name = request.data.get('name')
            price = request.data.get('price')
            
            # Create the Cart instance with the product_id, brand, name, and price
            cart_item = Cart.objects.create(
                quantity=serializer.validated_data.get('quantity', 1),
                total_price=serializer.validated_data.get('total_price', Decimal('0.00')),
                user_id=serializer.validated_data.get('user_id', 1),
                product_id=product_id, # Use the product_id from the request data
                brand=brand,
                name=name,
                price=price
            )
            
            # Serialize the created cart item
            serializer = CartSerializer(cart_item)
            
            # Calculate final_price after the instance has been created
            total_price = Decimal(serializer.instance.total_price)
            final_price = total_price # Assuming final_price is the same as total_price for simplicity
            
            # Add final_price to the serialized data
            serializer.data['final_price'] = final_price

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        Cart.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@method_decorator(csrf_exempt, name='dispatch')
class CartDetail(APIView):
    authentication_classes = []  # Disable authentication for this view
    permission_classes = []
    def delete(self, request, product_id):
        try:
            cart_item = Cart.objects.filter(product_id=product_id).first()
            if cart_item:
                cart_item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)




class AddressList(APIView):
    def get(self, request):
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# from django.middleware.csrf import get_token
# from django.http import JsonResponse
# from django.views import View

# class GetCSRFTokenView(View):
#     def get(self, request, *args, **kwargs):
#         csrf_token = get_token(request)
#         return JsonResponse({'csrf_token': csrf_token})
