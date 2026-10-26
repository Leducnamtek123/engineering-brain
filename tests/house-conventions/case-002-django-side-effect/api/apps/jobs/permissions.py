from rest_framework.permissions import BasePermission


class IsCompanyMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.company_id == request.user.company_id
