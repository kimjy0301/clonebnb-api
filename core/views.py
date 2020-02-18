from django.shortcuts import render
from rooms.models import Room
from django.http import HttpResponse

import json
from django.core import serializers

def list_rooms(request):
    data = serializers.serialize("json",Room.objects.all())
    response = HttpResponse(content=data)
    return response
