from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
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
