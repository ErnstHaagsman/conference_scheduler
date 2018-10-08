import pytz
from django.contrib import admin
from django.utils import timezone
from psycopg2.extras import DateTimeTZRange

from scheduler.models import Event, Staffer, Availability, ExpoDay, ExpoDemand, TalkLocation, TalkRequest


class TalkRequestInline(admin.StackedInline):
    model = TalkRequest


class AvailabilityInline(admin.TabularInline):
    model = Availability


@admin.register(Staffer)
class StafferAdmin(admin.ModelAdmin):
    inlines = [
        TalkRequestInline,
        AvailabilityInline
    ]


def force_tz(date, tz):
    naive_date = date.replace(tzinfo=None)
    return pytz.timezone(tz).localize(naive_date)


def range_force_tz(time_range, tz):
    if time_range is None:
        return None

    lower = force_tz(time_range.lower, tz)
    upper = force_tz(time_range.upper, tz)
    return DateTimeTZRange(lower=lower, upper=upper)


class ExpoDayInline(admin.StackedInline):
    model = ExpoDay


class TalkLocationInline(admin.StackedInline):
    model = TalkLocation


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [
        ExpoDayInline,
        TalkLocationInline
    ]

    def get_inline_formsets(self,
                            request,
                            formsets,
                            inline_instances,
                            obj=None):

        if obj:
            timezone.activate(obj.timezone)
        else:
            timezone.deactivate()

        return super(). \
            get_inline_formsets(request, formsets, inline_instances, obj)

    def save_formset(self, request, form, formset, change):
        # Activate the event's timezone to ensure inline forms gets stored
        # with the correct timezone
        tz = form.cleaned_data['timezone']
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, ExpoDay):
                instance.expo_time = range_force_tz(instance.expo_time, tz)
                instance.lunch_time = range_force_tz(instance.lunch_time, tz)
            instance.save()


@admin.register(ExpoDemand)
class ExpoDemandAdmin(admin.ModelAdmin):
    pass
