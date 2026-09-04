from django.shortcuts import render


def home_page(request):
    return render(request,"home.html")

def aboutme_page(request):
    return render(request, "aboutme.html")