from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrReadOnly(BasePermission):
    """Semua pengunjung boleh membaca; hanya pemilik (is_superuser) yang boleh menulis."""

    message = "Only the portfolio owner can change this data."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
        )


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """
    Peran dari Tugas 4:
    - pengunjung: hanya membaca
    - Editor: boleh membaca serta PUT/PATCH
    - pemilik (is_superuser): boleh semuanya (POST, PUT/PATCH, DELETE)
    """

    message = "You do not have permission to change this data."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return (
            request.method in ("PUT", "PATCH")
            and request.user.groups.filter(name="Editor").exists()
        )
