from datetime import datetime

import pytz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction, connection
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from psycopg2._range import DateTimeTZRange

from scheduler.forms.forms import TalkAddForm
from scheduler.models import TalkRequest, Event, TalkLocation, Staffer
from scheduler.util import force_tz


class IndexView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        # Get the user's next upcoming conference, and send them to the talk
        # list for that conf

        with connection.cursor() as cursor:
            cursor.execute("""
                select
                  se.slug
                from scheduler_expoday
                inner join scheduler_event se on scheduler_expoday.event_id = se.id
                inner join scheduler_staffer staffer on se.id = staffer.event_id
                where staffer.user_id = %s and expo_time && tstzrange(now(), 'infinity')
                group by se.slug
                order by min(lower(expo_time))
                limit 1;
            """, [request.user.id])

            row = cursor.fetchone()

        if row:
            return redirect('talk_list', row[0])
        else:
            return render(request, 'scheduler/no_event.html', {})


class TalkListView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        event_slug = kwargs['event_slug']
        event = get_object_or_404(Event, slug=event_slug)

        timezone.activate(event.timezone)

        talk_requests = TalkRequest.objects\
            .filter(staffer__user=request.user,
                    staffer__event=event) \
            .order_by('priority')



        return render(request, 'scheduler/talk_list.html', {
            'event' : event,
            'talk_requests' : talk_requests
        })


class TalkReprioritizeView(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        direction = kwargs['direction']
        talk_id = kwargs['talk_id']
        event_slug = kwargs['event_slug']

        talk = TalkRequest.objects.get(id=talk_id)
        talk_count = TalkRequest.objects.filter(staffer=talk.staffer).count()

        if talk.priority == 1 and direction == 'up' or \
                talk.priority == talk_count and direction == 'down':

            # No way to move the first talk up or the last talk down
            return HttpResponseBadRequest("Can't move the first talk up, or the last talk down.")

        talk_priority = talk.priority

        with transaction.atomic():
            if direction == 'up':
                swap_with = TalkRequest.objects.get(staffer=talk.staffer, priority=talk_priority - 1)
                swap_with.priority += 1
                swap_with.save()
                talk.priority -= 1
                talk.save()
            else:
                swap_with = TalkRequest.objects.get(staffer=talk.staffer, priority=talk_priority + 1)
                swap_with.priority -= 1
                swap_with.save()
                talk.priority += 1
                talk.save()

        return redirect('talk_list', event_slug)



class TalkDeleteView(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        talk_id = kwargs['talk_id']
        event_slug = kwargs['event_slug']

        talk = TalkRequest.objects.get(id=talk_id)
        lower_prio_talks = TalkRequest.objects.filter(priority__gt=talk.priority)

        with transaction.atomic():
            talk.delete()
            for to_move in lower_prio_talks:
                to_move.priority -= 1
                to_move.save()

        return redirect('talk_list', event_slug)


class TalkAddView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        event_slug = kwargs['event_slug']

        event = Event.objects.get(slug=event_slug)
        locations = TalkLocation.objects.filter(event__slug=event_slug)
        form = TalkAddForm(locations=locations)

        return render(request, 'scheduler/add_talk.html', {
            'event': event,
            'form': form
        })

    def post(self, request, **kwargs):
        event_slug = kwargs['event_slug']

        event = Event.objects.get(slug=event_slug)
        locations = TalkLocation.objects.filter(event__slug=event_slug)

        form = TalkAddForm(request.POST, locations=locations)

        if form.is_valid():
            tr = TalkRequest()
            tr.staffer = Staffer.objects.get(user=request.user)
            tr.name = form.cleaned_data['talk_name']
            tr.talk_location = form.cleaned_data['talk_location']

            # Set the priority of the new talk, to the count of requests + 1
            count = TalkRequest.objects.filter(staffer=tr.staffer).count()
            tr.priority = count + 1

            # Construct the time range
            tz = pytz.timezone(event.timezone)
            lower = tz.localize(datetime.combine(form.cleaned_data['talk_date'],
                                                 form.cleaned_data['talk_start']))
            upper = tz.localize(datetime.combine(form.cleaned_data['talk_date'],
                                                 form.cleaned_data['talk_end']))

            tr.time = DateTimeTZRange(lower=lower, upper=upper)

            tr.save()

            return redirect('talk_list', event_slug)

        return render(request, 'scheduler/add_talk.html', {
            'event': event,
            'form': form
        })
