from django.shortcuts import render, redirect, reverse
from .models import Instrument, Cart, Order, Receipt, Customer
from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.models import AnonymousUser, User
from .forms import InstrumentForm, CustomerForm, MessageForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
    if request.user.is_anonymous:
        request.session['cached_session_key'] = request.session.session_key
    return render(request, "index.html")


def addToCart(request, i_id):
    # Check session
    if request.session.session_key == None:
        return redirect('index')
    # End check session

    session = request.session.session_key
    instrumentToAdd = Instrument.objects.filter(pk=i_id)[0]
    newItem = Cart(usersession=session, instrument=instrumentToAdd)
    newItem.save()
    return redirect('cart')


def deleteFromCart(request, i_id):
    # Check session
    if request.session.session_key == None:
        return redirect('index')
    # End check session

    session = request.session.session_key
    instrumentToDelete = Instrument.objects.filter(pk=i_id)[0]
    deleteItem = Cart.objects.filter(usersession=session, instrument=instrumentToDelete).all()
    deleteItem.delete()
    return redirect('cart')


def cart(request):
    # Check session
    if request.session.session_key == None:
        return redirect('index')
    # End check session
    for row in Cart.objects.all().reverse():
        if Cart.objects.filter(usersession=row.usersession).filter(instrument=row.instrument).count() > 1:
            row.delete()
    user = request.session.session_key
    productids = Cart.objects.filter(usersession=user).values("instrument")
    productids = list(productids)
    productids = [o['instrument'] for o in productids]
    products = Instrument.objects.filter(pk__in=productids)
    len = products.count()
    test = Receipt.objects.filter(session=user).count()
    if test == 0:
        recLen = Receipt.objects.count()
        receipt = Receipt(session=user, receipt=recLen + 1)
        receipt.save()

    recContext = Receipt.objects.filter(session=user).first()
    context = {"user": user, "products": products, "len": len, "receipt": recContext}

    if recContext.discountpercent != None:
        percent = recContext.discountpercent
        context = {"user": user, "products": products, "len": len, "receipt": recContext, "percent": percent}

    return render(request, "cart.html", context)


def payment(request):
    # Check session
    if request.session.session_key == None:
        return redirect('index')
    # End check session

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            if customer.paymenttype == "Credit":
                # prevent saving real card information for prototype
                customer.cardholdername = 'Encrypted information'
                customer.cardnumber = 'Encrypted information'
                customer.cardexpiry = 'Encrypted information'
                customer.cardcvv = 'Encrypted information'
            customer.customersession = request.session.session_key
            form.save()
            return redirect('final')
    else:
        user = request.session.session_key
        productids = Cart.objects.filter(usersession=user).values("instrument")
        productids = list(productids)
        productids = [o['instrument'] for o in productids]
        products = Instrument.objects.filter(pk__in=productids)
        form = CustomerForm()
        receipt = Receipt.objects.filter(session=user).first()

    context = {"form": form, "products": products, "receipt": receipt}
    if receipt.discountpercent != None:
        percent = receipt.discountpercent / 100
        context = {"form": form, "products": products, "receipt": receipt, "percent": percent}

    return render(request, 'payment.html', context)


def final(request):
    # Check session
    if request.session.session_key == None:
        return redirect('index')
    # End check session

    sessionNow = request.session.session_key
    customer = Customer.objects.filter(customersession=sessionNow).first()
    receipt = Receipt.objects.filter(session=sessionNow).first()

    productids = Cart.objects.filter(usersession=sessionNow).values("instrument")
    productids = list(productids)
    productids = [o['instrument'] for o in productids]
    products = Instrument.objects.filter(pk__in=productids)
    total = 0
    for p in products:
        pr = Instrument.objects.get(pk=p.id)
        pr.quantity = pr.quantity - 1
        pr.save()
        total += p.price

    if receipt.discountpercent != None:
        percent1 = receipt.discountpercent / 100
        toReduce = total * percent1
        total -= toReduce

    total += 1000
    order = Order(customer=customer, receipt=receipt, totalprice=total)
    order.save()
    order.products.set(products)
    order.save()

    # context = {"total":total, "products":products, "customer":customer, "receipt":receipt}
    # return render(request, 'final.html', context=context)
    return redirect('finalview')


def finalview(request):
    # Check session
    if request.session.session_key == None:
        return redirect('index')
    # End check session

    sessionNow = request.session.session_key
    customer = Customer.objects.filter(customersession=sessionNow).first()
    receipt = Receipt.objects.filter(session=sessionNow).first()

    productids = Cart.objects.filter(usersession=sessionNow).values("instrument")
    productids = list(productids)
    productids = [o['instrument'] for o in productids]
    products = Instrument.objects.filter(pk__in=productids)
    total = 1000  # innitialy for shipment
    for p in products:
        total += p.price
    request.session.flush()
    context = {"total": total, "products": products, "customer": customer, "receipt": receipt}
    return render(request, 'final.html', context=context)


def discount(request, percent):
    # Check session
    if request.session.session_key == None:
        return redirect('index')
    # End check session
    user = request.session.session_key
    reciept = Receipt.objects.filter(session=user).first()
    reciept.discountpercent = percent
    reciept.save()
    strpercent = str(percent)
    return redirect(reverse('cart') + '?p=' + strpercent)


def categories(request):
    return render(request, 'categories.html')


def contact(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('contact') + '?sent=true')
    else:
        form = MessageForm()
        context = {"form": form}
        return render(request, 'contact.html', context)


def about(request):
    return render(request, 'about.html')


@login_required
def instruments(request):
    queryset = Instrument.objects.all()
    len1 = Instrument.objects.count()
    context = {"instruments": queryset, "len": len1}
    return render(request, 'instruments.html', context)


@login_required
def add(request):
    if request.method == 'POST':
        form = InstrumentForm(request.POST, request.FILES)
        if form.is_valid():
            instrument = form.save(commit=False)

            form.save()
            return redirect('add')
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


def violina(request):
    products = Instrument.objects.filter(type="Violina")
    context = {"products": products}
    return render(request, 'products/zicani/violina.html', context)


def gitara(request):
    products = Instrument.objects.filter(type="Gitara")
    context = {"products": products}
    return render(request, 'products/zicani/gitara.html', context)


def kontrabas(request):
    products = Instrument.objects.filter(type="Kontrabas")
    context = {"products": products}
    return render(request, 'products/zicani/kontrabas.html', context)


def harfa(request):
    products = Instrument.objects.filter(type="Harfa")
    context = {"products": products}
    return render(request, 'products/zicani/harfa.html', context)


def mandolina(request):
    products = Instrument.objects.filter(type="Mandolina")
    context = {"products": products}
    return render(request, 'products/zicani/mandolina.html', context)


def violoncelo(request):
    products = Instrument.objects.filter(type="Violoncelo")
    context = {"products": products}
    return render(request, 'products/zicani/violoncelo.html', context)


def flejta(request):
    products = Instrument.objects.filter(type="Flejta")
    context = {"products": products}
    return render(request, 'products/duvacki/flejta.html', context)


def klarinet(request):
    products = Instrument.objects.filter(type="Klarinet")
    context = {"products": products}
    return render(request, 'products/duvacki/klarinet.html', context)


def saksofon(request):
    products = Instrument.objects.filter(type="Saksofon")
    context = {"products": products}
    return render(request, 'products/duvacki/saksofon.html', context)


def truba(request):
    products = Instrument.objects.filter(type="Truba")
    context = {"products": products}
    return render(request, 'products/duvacki/truba.html', context)


def tapani(request):
    products = Instrument.objects.filter(type="Tapani")
    context = {"products": products}
    return render(request, 'products/udarni/tapani.html', context)


def ksilofon(request):
    products = Instrument.objects.filter(type="Ksilofon")
    context = {"products": products}
    return render(request, 'products/udarni/ksilofon.html', context)


def kahoni(request):
    products = Instrument.objects.filter(type="Kahoni")
    context = {"products": products}
    return render(request, 'products/udarni/kahoni.html', context)


def harmonika(request):
    products = Instrument.objects.filter(type="Harmonika")
    context = {"products": products}
    return render(request, 'products/klavijatura/harmonika.html', context)


def pijano(request):
    products = Instrument.objects.filter(type="Pijano")
    context = {"products": products}
    return render(request, 'products/klavijatura/pijano.html', context)


def sintisajzer(request):
    products = Instrument.objects.filter(type="Sintisajzer")
    context = {"products": products}
    return render(request, 'products/klavijatura/sintisajzer.html', context)
