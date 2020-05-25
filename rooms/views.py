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
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")
    super_host = bool(request.GET.get("super_host", False))
    instant = bool(request.GET.get("instant", False))

    form = {
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "super_host": super_host,
        "instant": instant,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "room_types": room_types,
        "countries": countries,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city
    
    filter_args["country"] = country
    
    if room_type != 0:
        filter_args["room_type__pk"] = room_type
        
    if price != 0:
        filter_args["price__lte"] = price
    
    if guests != 0:
        filter_args['guests__gte'] = guests
    
    if bedrooms != 0:
        filter_args['bedrooms__gte'] = bedrooms
    
    if beds != 0:
        filter_args['beds__gte'] = beds
    
    if baths != 0 :
        filter_args['baths__gte'] = baths
        
    if instant is True:
        filter_args['instant_book'] = True
        
    if super_host is True:
        filter_args['host__superhost'] = True
        
    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args['amenities__pk'] = int(s_amenity)

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args['facilities__pk'] = int(s_facility)
        
        
    rooms = models.Room.objects.filter(**filter_args)

    return render(
        request,
        "rooms/search.html",
        context={**form, **choices, "rooms": rooms})
