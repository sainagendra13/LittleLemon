from django.urls import path

from .views import MenuItemsView,MenuItemDetailView,ManagerUsersView,ManagerUserRemoveDetailView, api_root
from .views import DeliveryCrewView,CategoryView, DeliveryCrewUserDetailRemoveView,CartView,CartDeleteView,OrderView,OrderDetailView

urlpatterns = [
    path('', api_root, name='api-root'),
    path('categories/', CategoryView.as_view()),
    path('menu-items/', MenuItemsView.as_view()),
    path('menu-items/<int:pk>/', MenuItemDetailView.as_view()),
    path('groups/manager/users/', ManagerUsersView.as_view()),
    path('groups/manager/users/<int:userId>/', ManagerUserRemoveDetailView.as_view()),
    path('groups/delivery-crew/users/', DeliveryCrewView.as_view()),
    path('groups/delivery-crew/users/<int:userId>/', DeliveryCrewUserDetailRemoveView.as_view()),
    path('cart/menu-items/', CartView.as_view()),
    path('cart/clear/', CartDeleteView.as_view()),
    path('orders/', OrderView.as_view()),
    path('orders/<int:orderId>/', OrderDetailView.as_view()),
]