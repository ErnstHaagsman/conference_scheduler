from django.contrib.postgres.fields import DateTimeRangeField
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
import pytz


def validate_timezone(timezone):
    if timezone not in pytz.all_timezones:
        raise ValidationError(
            f"{timezone} is not a valid timezone string. "
            "Please use a string like 'Europe/Berlin'"
        )


class Event(models.Model):
    name = models.CharField(max_length=300)
    timezone = models.CharField(
        max_length=100,
        validators=[
            validate_timezone
        ]
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Staffer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.get_full_name()} at {self.event.name}"


class Availability(models.Model):
    staffer = models.ForeignKey(
        Staffer,
        on_delete=models.CASCADE
    )
    time = DateTimeRangeField()

    class Meta:
        verbose_name = 'Availability'
        verbose_name_plural = 'Availability'


class ExpoDay(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )
    expo_time = DateTimeRangeField()
    lunch_time = DateTimeRangeField(
        null=True,
        blank=True
    )

    def __str__(self):
        tz = pytz.timezone(self.event.timezone)
        local_date = self.expo_time.lower.astimezone(tz)
        return local_date.strftime('%b %d')


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

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


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
