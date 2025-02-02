from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Listing(models.Model):
    host = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="listings",
        verbose_name=_("Host")
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("Title")
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        null=True
    )
    location = models.CharField(
        max_length=255,
        verbose_name=_("Location")
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Price"),
        help_text=_("Price per night or unit")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At")
    )

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=["location"], name="listing_location_idx"),
            models.Index(fields=["price"], name="listing_price_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gt=0),
                name="check_listing_price_positive"
            )
        ]


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', _("Pending")),
        ('confirmed', _("Confirmed")),
        ('canceled', _("Canceled")),
    ]

    booking_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("Booking ID")
    )
    property = models.ForeignKey(
        'Listing',
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name=_("Property")
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name=_("User")
    )
    start_date = models.DateField(
        verbose_name=_("Start Date")
    )
    end_date = models.DateField(
        verbose_name=_("End Date")
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Total Price")
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name=_("Status")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )

    def __str__(self):
        return f"Booking {self.booking_id} for {self.property.title} by {self.user.username}"

    class Meta:
        indexes = [
            models.Index(fields=["booking_id"], name="booking_id_idx"),
            models.Index(fields=["property"], name="booking_property_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(total_price__gt=0),
                name="check_booking_total_price_positive"
            ),
        ]


class Review(models.Model):
    review_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("Review ID")
    )
    property = models.ForeignKey(
        'Listing',
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("Property")
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("User")
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name=_("Rating"),
        help_text=_("Rating must be between 1 and 5")
    )
    comment = models.TextField(
        verbose_name=_("Comment")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )

    def __str__(self):
        return f"Review {self.review_id} for {self.property.title} by {self.user.username}"

    class Meta:
        indexes = [
            models.Index(fields=["review_id"], name="review_id_idx"),
            models.Index(fields=["property"], name="review_property_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                name="check_review_rating_range"
            )
        ]