from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from scheduler.models import TalkRequest, Event


class TalkListView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        event_slug = kwargs['event_slug']
        event = get_object_or_404(Event, slug=event_slug)

        talk_requests = TalkRequest.objects\
            .filter(staffer__user=request.user,
                    staffer__event=event) \
            .order_by('priority')



        return render(request, 'scheduler/request_list.html', {
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
