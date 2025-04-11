from django.test import TestCase

# Create your tests here.

def test_function(request):
    return render(request, 'vibelink/test.html')
