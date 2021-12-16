from django.db import models
from django.conf import settings
from django.urls import reverse_lazy

# Create your models here.

class Room(models.Model):
    ROOM_CATEGORIES = (
        ('STA', 'standard'),
        ('DEL', 'deluxe'),
        ('SUP', 'superior'),
        ('PRE', 'prezydencki'),
        ('KIN', 'królewski')
    )
    number = models.IntegerField()
    category = models.CharField(max_length=3, choices=ROOM_CATEGORIES)
    beds = models.IntegerField()
    capacity = models.IntegerField()

    def __str__(self):
        return f'{self.number}.{self.category} z {self.beds} łóżkami dla {self.capacity} gości'

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    def __str__(self):
        return f'{self.user} ma zarezerwowane {self.room} od {self.check_in} do {self.check_out}'

    def get_room_category(self):
        room_categories = dict(self.room.ROOM_CATEGORIES)
        room_category = room_categories.get(self.room.category)
        return room_category

    def get_cancel_booking_url(self):
        return reverse_lazy('hotel_app:CancelBookingView', args=[self.pk, ])