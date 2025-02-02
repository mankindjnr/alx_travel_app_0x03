from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer

class ListingViewSet(ModelViewSet):
    """
    API endpoint for managing Listings.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(ModelViewSet):
    """
    API endpoint for managing Bookings.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
