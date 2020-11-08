from django.shortcuts import render

# Create your views here.

def profile(request):
    # user_info = request.user
    # context = {
    #     'user_info': user_info
    # }
    return render(request, 'profile.html')