from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'main.html')

def place_list(request):
    return render(request, 'place_list.html')

def place_detail(request):
    return render(request, 'place_detail.html')

def place_route(request):
    return render(request, 'place_route.html')