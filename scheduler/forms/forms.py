from django import forms

from scheduler.models import TalkLocation


class TalkAddForm(forms.Form):

    def __init__(self, *args, **kwargs):
        locations = kwargs.pop('locations')
        super().__init__(*args, **kwargs)
        self.fields['talk_location'].queryset = locations

    talk_name = forms.CharField(
        label='Name',
        max_length=300,
        required=True)

    talk_location = forms.ModelChoiceField(
        label='Location',
        required=True,
        queryset=TalkLocation.objects.none())

    talk_date = forms.DateField(
        label='Date',
        required=True,
        help_text='e.g. 2019-01-25'
    )

    talk_start = forms.TimeField(
        label='Begins',
        required=True,
        help_text='e.g. 13:00'
    )

    talk_end = forms.TimeField(
        label='Ends',
        required=True,
        help_text='e.g. 17:00'
    )
