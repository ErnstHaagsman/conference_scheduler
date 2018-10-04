from django.contrib.postgres.fields import DateTimeRangeField
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
import pytz


def validate_timezone(timezone):
    return timezone in pytz.all_timezones


class Event(models.Model):
    name = models.CharField(max_length=300)
    timezone = models.CharField(
        max_length=100,
        validators=[
            validate_timezone
        ]
    )


class Staffer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )


class Availability(models.Model):
    staffer = models.ForeignKey(
        Staffer,
        on_delete=models.CASCADE
    )
    time = DateTimeRangeField()


class ExpoDay(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )
    expo_time = DateTimeRangeField()
    lunch_time = DateTimeRangeField()


class ExpoDemand(models.Model):
    day = models.ForeignKey(
        ExpoDay,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(
        "The amount of staffers needed in this time range"
    )
    time = DateTimeRangeField()


class TalkLocation(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=300)
    travel_distance = models.IntegerField(
        "The time to travel from the booth to/from this location, in minutes"
    )


class TalkRequest(models.Model):
    staffer = models.ForeignKey(
        Staffer,
        on_delete=models.CASCADE
    )
    talk_location = models.ForeignKey(
        TalkLocation,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=300)
    time = DateTimeRangeField()
    priority = models.IntegerField(
        "Lowest number has the highest priority. Only the rank matters."
    )


class ScheduleEntry(models.Model):
    TALK = 'TALK'
    LUNCH = 'LUNCH'
    BOOTH_DUTY = 'BOOTH_DUTY'
    FREE = 'FREE'

    TYPE_CHOICES = (
        (TALK, 'Attend talk'),
        (LUNCH, 'Have lunch'),
        (BOOTH_DUTY, 'Booth duty'),
        (FREE, 'Free time')
    )

    staffer = models.ForeignKey(
        Staffer,
        on_delete=models.CASCADE
    )
    talk = models.ForeignKey(
        TalkRequest,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    type = models.CharField(
        max_length=300,
        choices=TYPE_CHOICES
    )
    time = DateTimeRangeField()
    current = models.BooleanField(
        "Whether this is a current or a historical schedule entry"
    )
    final = models.BooleanField(
        "Whether this schedule entry may be changed in the future"
    )
    created = models.DateTimeField(
        "The time this schedule entry was created"
    )

    def clean(self):
        if self.type == self.TALK and self.talk is None:
            raise ValidationError(
                "Schedule entries for talks should refer to a talk: please set"
                "the 'talk' field"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
