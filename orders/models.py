from django.db import models
from datetime import datetime
from django.forms import ValidationError
from django.utils.timezone import now
from django.db.models.signals import post_save, post_delete
from functools import wraps
from django.core.mail import send_mail
from products.models import ProductUnit, ProductUnitBookingDates
from basket.models import Basket


FROM_EMAIL = 'mail@tochka-a-sochi.ru'
TO_EMAIL = 'tochka_a_sochi@mail.ru'

PAYMENT_TYPES = (
    ('bank_card', 'Банковская карта'),
    ('cash_courier', 'Наличными курьеру'),
    ('cash_shop', 'Наличными в магазине'),
)

STATUSES = (
    ('created', 'Создан'),
    ('approved_1', 'Подтвержден и ждет оплаты'),
    ('approved_2', 'Подтвержден и оплачен'),
    ('delivered', 'Выдан клиенту'),
    ('await', 'Ожидание возврата инвентаря'),
    ('finished', 'Выполнен'),
    ('cancelled', 'Отменен'),
    ('payment_error', 'Ошибка при оплате')
)


def intersects_interval(i1, i2):
    date_from1 = i1.date_from.replace(tzinfo=None)
    date_to1 = i1.date_to.replace(tzinfo=None)
    date_from2 = i2.date_from.replace(tzinfo=None)
    date_to2 = i2.date_to.replace(tzinfo=None)
    if date_from2 <= date_from1 < date_to2:
        return True
    if date_from2 < date_to1 <= date_to2:
        return True
    if date_to1 > date_from2 >= date_from1 and date_to1 >= date_to2 >= date_from1:
        return True
    return False


def get_product_units_for_date_range(product_in_basket, self, min):
    product_units = []
    for (index, product_unit) in enumerate(product_in_basket.product.product_units.all()):
        is_free = True
        for booking_date in product_unit.booking_dates.all():
            if intersects_interval(self, booking_date):
                is_free = False
                break
        if is_free:
            product_units.append(product_unit)
        if len(product_units) == product_in_basket.quantity and min:
            break
    return product_units


class Order(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.SET_NULL, null=True, verbose_name="Корзина")
    name = models.CharField(max_length=64, verbose_name="Имя", blank=True)
    phone = models.CharField(max_length=64, verbose_name="Телефон", blank=False)
    email = models.CharField(max_length=64, verbose_name="Почта", blank=False)
    city = models.CharField(max_length=64, verbose_name="Город", blank=True)
    address = models.CharField(max_length=64, verbose_name="Адрес", blank=True)
    comment = models.TextField(max_length=64, verbose_name="Комментарий", blank=True)
    date_from = models.DateField(verbose_name="Бронь от")
    date_to = models.DateField(verbose_name="Бронь до")
    created = models.DateTimeField(default=now, editable=False, verbose_name=u"Создание заказа")
    payment_type = models.CharField(max_length=32, choices=PAYMENT_TYPES, verbose_name="Тип оплаты", default='cash_shop')
    status = models.CharField(max_length=32, choices=STATUSES, verbose_name="Статус", default='created')
    total_price = models.IntegerField(verbose_name="Полная цена", null=True, blank=True)

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = u"Заказ"
        verbose_name_plural = u"Заказы"

    def save(self, *args, **kwargs):
        if self.basket and len(self.basket.products.all()) > 0:
            self.total_price = 0
            range = datetime(year=self.date_to.year, month=self.date_to.month, day=self.date_to.day, hour=self.date_to.hour) - \
                    datetime(year=self.date_from.year, month=self.date_from.month, day=self.date_from.day, hour=self.date_from.hour)

            for product_in_basket in self.basket.products.all():

                # проверяем, есть ли достаточное количество товаров в наличии для выполнения заказа
                if product_in_basket.quantity > len(product_in_basket.product.product_units.all()):
                    raise ValidationError("На складе нет необходимого количества товара")

                # найти product_units, которые можно забронировать на выбранные даты
                product_units = get_product_units_for_date_range(product_in_basket, self, True)

                # если найденное количество товаров меньше необходимого, выдаем ошибку
                if len(product_units) < product_in_basket.quantity:
                    raise ValidationError("На выбранные даты некоторые товары недоступны")

                if product_in_basket.product.hour_rate:
                    self.total_price += product_in_basket.quantity * product_in_basket.product.price * (range.seconds // 3600)
                else:
                    self.total_price += product_in_basket.quantity*product_in_basket.product.price*range.days

            if not self.pk:
                # to  admin
                message = 'Создан новый заказ. Зайдите в админ панель, чтобы посмотреть подробности.\n'
                message += 'Общая стоимость: {} руб.'.format(self.total_price)
                send_mail(
                    u'Бронирование на сайте',
                    message,
                    FROM_EMAIL,
                    [TO_EMAIL],
                    fail_silently=True,
                )

                # to client
                if self.email:
                    message = 'Вы успешно оформили заказ на сайте tochka-a-sochi.ru\n'
                    message += 'Общая стоимость: {} руб.\n'.format(self.total_price)
                    for product_in_basket in self.basket.products.all():
                        message += '\n{}: x{}, {} руб. за штуку'.format(product_in_basket.product.name, product_in_basket.quantity, product_in_basket.product.price)
                    message += '\n\nТелефон для связи: 8 938 4451 613'
                    send_mail(
                        u'Бронирование на сайте',
                        message,
                        FROM_EMAIL,
                        [self.email],
                        fail_silently=True,
                    )
        super().save(*args, **kwargs)


class ProductUnitInOrder(models.Model):
    product_unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE, blank=False, null=False, verbose_name="Товар")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=False, null=False, verbose_name="Заказ", related_name="products")
    quantity = models.IntegerField(verbose_name="Количество")
    price = models.IntegerField(verbose_name="Цена за час/день")

    def __str__(self):
        return self.product_unit.product.name

    class Meta:
        verbose_name = u"Товар в заказе"
        verbose_name_plural = u"Товары в заказе"


class FormApplication(models.Model):
    form = models.CharField(max_length=64, verbose_name="Форма", blank=True)
    name = models.CharField(max_length=64, verbose_name="Имя", blank=True)
    phone = models.CharField(max_length=64, verbose_name="Телефон")
    description = models.CharField(max_length=64, verbose_name="Описание", blank=True)
    date = models.DateTimeField(default=now, editable=False, verbose_name=u"Создание заказа")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"Заявка на обратный звонок"
        verbose_name_plural = u"Заявки на обратный звонок"

    def save(self, *args, **kwargs):
        if not self.pk:
            message = 'Поступила заявка с сайта.\n'
            message += 'Дата создания: {}\n'.format(self.date)
            message += 'Имя: {}\n'.format(self.name)
            message += 'Телефон: {}\n'.format(self.phone)
            if self.form:
                message += 'Форма: {}\n'.format(self.form)
            if self.description:
                message += 'Описание: {}'.format(self.description)
            send_mail(
                u'Заявка с сайта',
                message,
                FROM_EMAIL,
                [TO_EMAIL],
                fail_silently=True,
            )
        super().save(*args, **kwargs)


def disable_for_loaddata(signal_handler):
    """
    Decorator that turns off signal handlers when loading fixture data.
    """
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs['raw']:
            return
        signal_handler(*args, **kwargs)
    return wrapper


@disable_for_loaddata
def order_post_save(sender, instance, created, **kwargs):
    for product_in_basket in instance.basket.products.all():
        product_units = get_product_units_for_date_range(product_in_basket, instance, True)
        for product_unit in product_units:
            product_unit_in_order_data = {
                'product_unit': product_unit,
                'order': instance,
                'quantity': product_in_basket.quantity,
                'price': product_in_basket.product.price
            }
            p, c = ProductUnitInOrder.objects.get_or_create(**product_unit_in_order_data)
            print(p, c)

            product_unit_booking_dates_data = {
                'product_unit': product_unit,
                'date_from': instance.date_from,
                'date_to': instance.date_to
            }
            ProductUnitBookingDates.objects.get_or_create(**product_unit_booking_dates_data)


post_save.connect(order_post_save, sender=Order)