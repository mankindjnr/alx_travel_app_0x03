from rest_framework import serializers
from .models import Listing, Booking


class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Listing model.
    """
    class Meta:
        model = Listing
        fields = [
            'property_id',
            'host',
            'title',
            'description',
            'price_per_night',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['property_id', 'created_at', 'updated_at']


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model.
    """
    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'property',
            'user',
            'start_date',
            'end_date',
            'total_price',
            'status',
            'created_at'
        ]
        read_only_fields = ['booking_id', 'status', 'created_at']
