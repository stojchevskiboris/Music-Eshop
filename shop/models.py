from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Instrument(models.Model):
    class Categories(models.TextChoices):
        ZHICHANI = "Zhichani", "Жичани"
        DUVACHKI = "Duvachki", "Дувачки"
        UDARNI = "Udarni", "Ударни"
        KLAVIJATURA = "Klavijatura", "Клавијатура"

    class Types(models.TextChoices):
        VIOLINA = "Violina", "Виолина"
        GITARA = "Gitara", "Гитара"
        KONTRABAS = "Kontrabas", "Контрабас"
        HARFA = "Harfa", "Харфа"
        MANDOLINA = "Mandolina", "Мандолина"
        VIOLONCELO = "Violoncelo", "Виолончело"
        FLEJTA = "Flejta", "Флејта"
        KLARINET = "Klarinet", "Кларинет"
        TRUBA = "Truba", "Труба"
        SAKSOFON = "Saksofon", "Саксофон"
        TAPANI = "Tapani", "Тапани"
        KSILOFON = "Ksilofon", "Ксилофон"
        KAHONI = "Kahoni", "Кахони"
        PIJANO = "Pijano", "Пијано"
        HARMONIKA = "Harmonika", "Хармоника"
        SINTISAJZER = "Sintisajzer", "Синтисајзер"

    category = models.CharField(max_length=11, choices=Categories.choices, default=Categories.ZHICHANI)
    type = models.CharField(max_length=12, choices=Types.choices, default=Types.GITARA)
    manufacturer = models.CharField(max_length=80)
    model = models.CharField(max_length=80)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'{self.manufacturer} {self.model}'


class Cart(models.Model):
    usersession = models.CharField(max_length=50)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    # quantity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.usersession} {self.instrument}'


class Customer(models.Model):
    class Payment(models.TextChoices):
        CASH = "Cash", "Во готово"
        CARD = "Credit", "Со кредитна картичка"
        BANK = "Bank", "Преку банкарска трансакција"

    customersession = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    municipality = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    paymenttype = models.CharField(max_length=10, choices=Payment.choices, default=Payment.CASH)
    cardholdername = models.CharField(max_length=50, null=True, blank=True)
    cardnumber = models.CharField(max_length=16, null=True, blank=True)
    cardexpiry = models.CharField(max_length=5, null=True, blank=True)
    cardcvv = models.CharField(max_length=3, null=True, blank=True)

    def __str__(self):
        return f'{self.name} {self.surname}'


class Receipt(models.Model):
    receipt = models.IntegerField()
    session = models.CharField(max_length=50)
    discountpercent = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.receipt}'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    products = models.ManyToManyField(Instrument)
    # products = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)
    # cart = models.ManyToManyField(Cart)
    totalprice = models.IntegerField()
    orderdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer}'


class Message(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    message = models.TextField()
