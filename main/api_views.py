from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Achievements, Experience
from main.permissions import IsPortfolioOwnerOrEditorOrReadOnly
from main.serializers import AchievementsSerializer, ExperienceSerializer


# ---------- helper bersama (pola sama untuk Achievements dan Experience) ----------

def _list(request, model, serializer_class):
    if request.method in ("GET", "HEAD"):
        items = model.objects.prefetch_related("starred_by").order_by("title", "id")
        title = request.query_params.get("title", "").strip()
        if title:
            items = items.filter(title__icontains=title)
        serializer = serializer_class(items, many=True, context={"request": request})
        return Response(serializer.data)

    serializer = serializer_class(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def _detail(request, model, serializer_class, pk):
    obj = get_object_or_404(model.objects.prefetch_related("starred_by"), pk=pk)

    if request.method in ("GET", "HEAD"):
        return Response(serializer_class(obj, context={"request": request}).data)

    if request.method == "DELETE":
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = serializer_class(
        obj, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


def _star(request, model, serializer_class, pk):
    obj = get_object_or_404(model, pk=pk)
    if obj.starred_by.filter(pk=request.user.pk).exists():
        obj.starred_by.remove(request.user)
    else:
        obj.starred_by.add(request.user)
    return Response(serializer_class(obj, context={"request": request}).data)


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
