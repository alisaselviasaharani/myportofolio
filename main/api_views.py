from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Achievements, Education, Experience
from main.permissions import IsPortfolioOwnerOrEditorOrReadOnly
from main.serializers import AchievementsSerializer, EducationSerializer, ExperienceSerializer


# ---------- helper bersama (pola sama untuk Achievements, Experience, dan Education) ----------
# Note: awalnya saya nulis view-nya satu-satu per model dan hasilnya hampir kembar semua.
# Biar ga copy-paste terus, saya pisahin jadi 3 helper (_list, _detail, _star) yang dipakai ulang.
# Validasi data ada di serializer dan izin akses ada di permission class,
# jadi di sini cuma ngurus alur request -> response + status code-nya.

def _list(request, model, serializer_class, search_field="title", order_fields=None):
    """GET/HEAD -> daftar data (bisa dicari lewat ?<search_field>=...), POST -> buat data baru."""
    if request.method in ("GET", "HEAD"):
        if order_fields is None:
            order_fields = ("title", "id")
        # prefetch_related supaya hitung star ga bikin query baru untuk tiap baris (N+1)
        items = model.objects.prefetch_related("starred_by").order_by(*order_fields)
        search_value = request.query_params.get(search_field, "").strip()
        if search_value:
            items = items.filter(**{f"{search_field}__icontains": search_value})
        serializer = serializer_class(items, many=True, context={"request": request})
        return Response(serializer.data)

    # POST: kalau data tidak valid, raise_exception otomatis balikin 400 beserta pesan errornya
    serializer = serializer_class(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def _detail(request, model, serializer_class, pk):
    """GET/HEAD -> satu data, PUT/PATCH -> ubah data, DELETE -> hapus data."""
    # kalau id-nya ga ada langsung 404
    obj = get_object_or_404(model.objects.prefetch_related("starred_by"), pk=pk)

    if request.method in ("GET", "HEAD"):
        return Response(serializer_class(obj, context={"request": request}).data)

    if request.method == "DELETE":
        obj.delete()
        # 204 = berhasil tapi memang tidak ada isi yang dikembalikan
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PUT = semua field wajib dikirim, PATCH = partial=True jadi boleh kirim sebagian saja
    serializer = serializer_class(
        obj, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


def _star(request, model, serializer_class, pk):
    """Toggle star: kalau user sudah nge-star berarti di-unstar, kalau belum berarti di-star."""
    obj = get_object_or_404(model, pk=pk)
    # yang dipakai selalu request.user (bukan dari body), jadi user ga bisa nge-star atas nama orang lain
    if obj.starred_by.filter(pk=request.user.pk).exists():
        obj.starred_by.remove(request.user)
    else:
        obj.starred_by.add(request.user)
    return Response(serializer_class(obj, context={"request": request}).data)


# Tiap endpoint di bawah ini dibuat dengan pola yang sama:
# - SessionAuthentication -> login lewat session Django, sama seperti halaman web biasa
# - permission_classes    -> yang nentuin siapa boleh ngapain (lihat main/permissions.py)
# - IsAuthenticated       -> khusus endpoint star, siapa pun yang sudah login boleh

# ---------- Achievements ----------

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def achievements_list(request):
    return _list(request, Achievements, AchievementsSerializer)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def achievements_detail(request, achievements_id):
    return _detail(request, Achievements, AchievementsSerializer, achievements_id)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def achievements_star(request, achievements_id):
    return _star(request, Achievements, AchievementsSerializer, achievements_id)


# ---------- Experience ----------

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_list(request):
    return _list(request, Experience, ExperienceSerializer)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_detail(request, experience_id):
    return _detail(request, Experience, ExperienceSerializer, experience_id)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def experience_star(request, experience_id):
    return _star(request, Experience, ExperienceSerializer, experience_id)


# ---------- Education ----------

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_list(request):
    return _list(
        request,
        Education,
        EducationSerializer,
        search_field="institution",
        order_fields=("institution", "id"),
    )


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_detail(request, education_id):
    return _detail(request, Education, EducationSerializer, education_id)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def education_star(request, education_id):
    return _star(request, Education, EducationSerializer, education_id)
