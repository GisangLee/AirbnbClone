from django.views import View
from django_countries import countries
from django.views.generic import ListView, DetailView, UpdateView
from django.http import Http404
from django.core.paginator import Paginator
from django.shortcuts import render
from . import forms
from . import models


class HomeView(ListView):
    """ Home View Definition """

    model = models.Room
    paginate_by = 12
    ordering = "created"
    context_object_name = "rooms"


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", context={"room": room})

    except models.Room.DoesNotExist:
        raise Http404()


def search(request):
    country = request.GET.get("country")

    if country:
        form = forms.SearchForm(request.GET)

        if form.is_valid():
            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")
            price = form.cleaned_data.get("price")
            guests = form.cleaned_data.get("guest")
            bedrooms = form.cleaned_data.get("bedrooms")
            beds = form.cleaned_data.get("beds")
            baths = form.cleaned_data.get("baths")
            superhost = form.cleaned_data.get("superhost")
            instant_book = form.cleaned_data.get("instant_book")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")

            filter_args = {}

            if city != "Anywhere":
                filter_args["city__startswith"] = city

            filter_args["country"] = country

            if room_type is not None:
                filter_args["room_type"] = room_type

            if price is not None:
                filter_args["price__lte"] = price

            if guests is not None:
                filter_args['guests__gte'] = guests

            if bedrooms is not None:
                filter_args['bedrooms__gte'] = bedrooms

            if beds is not None:
                filter_args['beds__gte'] = beds

            if baths is not None:
                filter_args['baths__gte'] = baths

            if instant_book is True:
                filter_args['instant_book'] = True

            if superhost is True:
                filter_args['host__superhost'] = True

            for amenity in amenities:
                filter_args['amenities'] = amenity

            for facility in facilities:
                filter_args['facilities'] = facility

            qs = models.Room.obejcts.filter(**filter_args).order_by("-created")

            paginator = Paginator(qs, 10, orphans=5)
            page = request.GET.get_page("page", 1)
            rooms = paginator.get_page(page)

            return render(
                request, "rooms/search.html", {"form": form, "rooms": rooms}
            )

    else:
        form = forms.SearchForm()

    return render(request, "rooms/search.html", {"form": form})


class EditRoomView(UpdateView):
    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "houserules",
    )


