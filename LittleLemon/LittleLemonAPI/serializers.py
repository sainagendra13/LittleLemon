from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category,Cart,Order,OrderItem,MenuItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields=['id', 'slug', 'title']
        model=Category
        
class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category=CategorySerializer(read_only=True)
    class Meta:
        model=MenuItem
        fields=['id','title','price','category','category_id','featured']
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields=['id','menuitem','quantity','unit_price','price']
        read_only_fields= ['unit_price', 'price']
        
        
class OrderItemSerializer(serializers.ModelSerializer):
    menuitem= MenuItemSerializer(read_only=True)
   # order=OrderSerializer(read_only=True)
    class Meta:
        model=OrderItem
        fields=['id','menuitem','quantity','unit_price','price']
        
        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    delivery_crew=UserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = [ 'id','user', 'delivery_crew', 'status', 'total', 'date', 'items']
        read_only_fields = [ 'user', 'total', 'date', 'items']
    
    
    
    
    