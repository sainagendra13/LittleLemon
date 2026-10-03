from rest_framework.permissions import BasePermission


class IsManager(BasePermission):

    def has_permission(self, request, view):
        return ( request.user.is_authenticated and request.user.groups.filter(name='Manager').exists())


class IsDeliveryCrew(BasePermission):

    def has_permission(self, request, view):
        return ( request.user.is_authenticated and request.user.groups.filter(name='Delivery crew').exists())

        return (
            request.user.is_authenticated
            and request.user.groups.filter(
                name='Delivery crew'
            ).exists()
        )

class IsCustomer(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.groups.filter( name__in=['Manager','Delivery crew']).exists()