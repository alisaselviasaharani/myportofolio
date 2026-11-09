from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """
    Permission untuk semua endpoint portfolio (Achievements, Experience, Education).
    Pembagian peran yang saya pakai (dari Tugas 4):
    - pengunjung / belum login : hanya boleh membaca (GET, HEAD, OPTIONS)
    - Editor                   : boleh membaca + PUT/PATCH, tapi tidak boleh POST dan DELETE
    - pemilik (is_superuser)   : boleh semuanya

    Note: pengecekan hak akses sengaja saya taruh di sini dan bukan di dalam view,
    jadi view cukup fokus ngurus data. Kalau ada yang ditolak, DRF otomatis
    balikin 403 Forbidden.
    """

    message = "You do not have permission to change this data."

    def has_permission(self, request, view):
        # method yang cuma baca (GET/HEAD/OPTIONS) boleh buat siapa saja
        if request.method in SAFE_METHODS:
            return True

        # selain itu wajib login dulu
        if not request.user.is_authenticated:
            return False

        # pemilik portfolio bebas ngapain aja
        if request.user.is_superuser:
            return True

        # Editor cuma boleh ubah data yang sudah ada (PUT/PATCH).
        # Cek berdasarkan group "Editor", bukan is_staff, supaya staff biasa tetap ditolak.
        return (
            request.method in ("PUT", "PATCH")
            and request.user.groups.filter(name="Editor").exists()
        )
