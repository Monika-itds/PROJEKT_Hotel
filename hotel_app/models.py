from django.db import models
from django.conf import settings

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
