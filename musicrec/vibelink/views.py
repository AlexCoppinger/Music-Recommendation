from django.shortcuts import render

# Create your views here.

def test_function(request):
    return render(request, 'vibelink/test.html')