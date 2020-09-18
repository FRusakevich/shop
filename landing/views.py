from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from .forms import BuyersForm


# from products.models import *
# Create your views here.
def landing(request):
    form = BuyersForm(request.POST or None)
    if request.method == "POST" and form.is_valid():

        form.save()

    return render(request, 'landing.html', {'form': form})
