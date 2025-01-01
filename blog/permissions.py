from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    自定义权限类：
    - 允许管理员进行所有操作
    - 允许其他用户只读
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    自定义权限类：
    - 允许作者编辑自己的文章
    - 允许其他用户只读
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user 