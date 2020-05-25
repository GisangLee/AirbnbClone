from django_countries import countries
from django.views.generic import ListView, DetailView
from django.http import Http404
from django.shortcuts import render
from . import models


class HomeView(ListView):
    """ Home View Definition """

    model = models.Room
    paginate_by = 10
    ordering = "created"
    context_object_name = "rooms"


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", context={"room": room})

    except models.Room.DoesNotExist:
        raise Http404()


def search(request):
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    room_types = models.RoomType.objects.all()
    return render(
        request,
        "rooms/search.html",
        context={"city": city, "countries": countries, "room_types": room_types}
    )
