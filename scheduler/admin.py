from django.contrib import admin

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


@admin.register(ExpoDemand)
class ExpoDemandAdmin(admin.ModelAdmin):
    pass
