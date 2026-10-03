from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import MenuItem, OrderItem, Order, Cart, Category
from .permissions import IsCustomer, IsManager, IsCustomer
from .serializers import OrderSerializer, CartSerializer,CategorySerializer, MenuItemSerializer, UserSerializer
# Create your views here.
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'register': '/api/users/',
        'login': '/api/token/login/',
        'current_user': '/api/users/me/',
        'menu_items': '/api/menu-items/',
        'cart': '/api/cart/menu-items/',
        'orders': '/api/orders/',
        'manager_users': '/api/groups/manager/users/',
        'delivery_crew': '/api/groups/delivery-crew/users/',
    })

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsManager()]

class MenuItemsView(generics.ListCreateAPIView):
    queryset=MenuItem.objects.all()
    serializer_class=MenuItemSerializer
    filterset_fields = ['category','price']
    search_fields = ['category__title','title']
    ordering_fields = ['title','price']
    
    def get_permissions(self):
        if self.request.method=='GET':
            return [ IsAuthenticated() ]
        return [ IsManager()]
        
class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=MenuItem.objects.all()
    serializer_class= MenuItemSerializer
    
    def get_permissions(self):
        if self.request.method=='GET':
            return [ IsAuthenticated() ]
        return [ IsManager()]
    
class ManagerUsersView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [ IsManager ] 

    def get_queryset(self):
        group = Group.objects.get(name='Manager')
        return group.user_set.all()

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('username')
        if not user_id:
            return Response( { 'error': 'username is required'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404( User, username=user_id)
        group = Group.objects.get( name='Manager')
        group.user_set.add(user)
        return Response( UserSerializer(user).data, status=status.HTTP_201_CREATED)
    
    
class ManagerUserRemoveDetailView(generics.DestroyAPIView):
    permission_classes = [IsManager]
    
    def delete( self, request, userId, *args, **kwargs):
        user = get_object_or_404( User, id=userId)
        group = get_object_or_404( Group, name='Manager')
        group.user_set.remove(user)
        return Response(status=status.HTTP_200_OK)
    

class DeliveryCrewView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        group = Group.objects.get(name='Delivery crew')
        return group.user_set.all()
    
    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        if not username:
            return Response({'error': 'username is required'},status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User,username=username)
        group = Group.objects.get(name='Delivery crew')
        group.user_set.add(user)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

class DeliveryCrewUserDetailRemoveView(generics.DestroyAPIView):
    permission_classes = [IsManager]
    def delete(self,request,userId,*args,**kwargs):
        user = get_object_or_404(User,id=userId)
        group = get_object_or_404(Group,name='Delivery crew')
        group.user_set.remove(user)
        return Response(status=status.HTTP_200_OK)

class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
        
    def create(self, request, *args, **kwargs):
        menuitem_id = request.data.get('menuitem')
        quantity = request.data.get('quantity')
        menuitem = MenuItem.objects.get(id=menuitem_id)
        unit_price = menuitem.price
        price = unit_price * int(quantity)
        cart = Cart.objects.create(user=request.user,menuitem=menuitem,quantity=quantity,unit_price=unit_price,price=price)
        return Response(CartSerializer(cart).data,status=status.HTTP_201_CREATED)


class CartDeleteView(generics.DestroyAPIView):
    permission_classes = [IsCustomer]
    def delete(self,request,*args,**kwargs):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_200_OK)
    
    
class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        if user.groups.filter(name='Delivery crew').exists():
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsCustomer()]

    def create(self,request,*args,**kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'},status=status.HTTP_400_BAD_REQUEST)
        total = sum(item.price for item in cart_items)
        order = Order.objects.create(user=request.user,total=total,status=False)
        for item in cart_items:
            OrderItem.objects.create(order=order,menuitem=item.menuitem,quantity=item.quantity,unit_price=item.unit_price,price=item.price)
        cart_items.delete()
        return Response(OrderSerializer(order).data,status=status.HTTP_201_CREATED)
    
    
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer

    def get_object(self):
        order = get_object_or_404(Order, id=self.kwargs['orderId'])
        return order
        # user = self.request.user
        # is_manager = user.groups.filter(name='Manager').exists()
        # is_delivery = user.groups.filter(name='Delivery crew').exists()
        # if is_manager:
        #     return order

        # if is_delivery:
        #     if order.delivery_crew != user:
        #         from rest_framework.exceptions import PermissionDenied
        #         raise PermissionDenied()
        #     return order

        # if order.user != user:
        #     from rest_framework.exceptions import PermissionDenied
        #     raise PermissionDenied()
        #return order

    def get_permissions(self):
        user = self.request.user
        if self.request.method == 'DELETE':
            return [IsManager()]

        if self.request.method == 'GET':
            return [IsAuthenticated()]

        if self.request.method == 'PATCH':
            return [IsAuthenticated()]

        if self.request.method == 'PUT':
            return [IsAuthenticated()]
        return [IsAuthenticated()]
    
    def update(self,request,*arg,**kwargs):
        order = self.get_object()
        user = request.user
        is_manager = user.groups.filter(name='Manager').exists()
        is_delivery = user.groups.filter(name='Delivery crew').exists()
        # if is_delivery:
        #     allowed_fields = ['status']
        #     for field in request.data:
        #         if field not in allowed_fields:
        #             return Response(
        #                 {
        #                     'error':
        #                     'Delivery crew can only update status'
        #                 },
        #                 status=status.HTTP_403_FORBIDDEN)

        if is_manager:
            if 'delivery_crew' in request.data:
                crew_id = request.data['delivery_crew']
                crew = get_object_or_404(User,id=crew_id)
                if not crew.groups.filter(name='Delivery crew').exists():
                    return Response(
                        {
                            'error':
                            'User is not delivery crew'
                        },
                        status=status.HTTP_400_BAD_REQUEST)
                order.delivery_crew = crew
            if 'status' in request.data:
                order.status = request.data['status']
            order.save()
            return Response(OrderSerializer(order).data,status=status.HTTP_200_OK)
        if is_delivery:
            if 'status' not in request.data:
                return Response({'error':'Status is required'}, status=status.HTTP_400_BAD_REQUEST)
            order.status = request.data['status']
            order.save()
            return Response(OrderSerializer(order).data,status=status.HTTP_200_OK)
        return Response(
            {
                'detail':
                'You do not have permission to perform this action.'
            },status=status.HTTP_403_FORBIDDEN)