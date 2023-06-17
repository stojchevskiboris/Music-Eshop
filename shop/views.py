from django.shortcuts import render, redirect
from .models import Instrument, Cart
from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.models import AnonymousUser, User
from .forms import InstrumentForm

# Create your views here.

def index(request):
    if request.user.is_anonymous:
        request.session['cached_session_key'] = request.session.session_key
    return render(request, "index.html")


def addToCart(request, i_id):
    session = request.session.session_key
    instrumentToAdd = Instrument.objects.filter(pk=i_id)[0]
    print(instrumentToAdd)
    newItem = Cart(usersession=session, instrument=instrumentToAdd)
    newItem.save()
    return redirect('cart')


def cart(request):
    user = request.session.session_key
    productids = Cart.objects.filter(usersession=user).values("instrument")
    productids = list(productids)
    productids = [o['instrument'] for o in productids]
    products = Instrument.objects.filter(pk__in=productids)
    context = {"user": user, "products": products}
    return render(request, "cart.html", context)


def categories(request):
    return render(request, 'categories.html')


def contact(request):
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')


def instruments(request):
    queryset = Instrument.objects.all()
    context = {"instruments": queryset}
    return render(request, 'instruments.html', context)


def add(request):
    if request.method == 'POST':
        form = InstrumentForm(request.POST, request.FILES)
        if form.is_valid():
            instrument = form.save(commit=False)
            form.save()
            return redirect('index')
    else:
        form = InstrumentForm()

    context = {"form": form}
    return render(request, 'add.html', context)


def loginView(request):
    return redirect('index')


def logoutView(request):
    user = getattr(request, "user", None)
    if not getattr(user, "is_authenticated", True):
        user = None
    user_logged_out.send(sender=user.__class__, request=request, user=user)
    request.session.flush()
    if hasattr(request, "user"):
        request.user = AnonymousUser()
    return redirect('index')



def zicani(request):
    return render(request, 'products/zicani.html')

def duvacki(request):
    return render(request, 'products/duvacki.html')

def udarni(request):
    return render(request, 'products/udarni.html')

def klavijatura(request):
    return render(request, 'products/klavijatura.html')