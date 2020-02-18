from django.contrib import admin
from . import models


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = ("name", "photo_number", "favs")


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
