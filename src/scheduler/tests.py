from django.core.exceptions import ValidationError
from django.test import TestCase

from scheduler.models import Event


class EventTestCase(TestCase):
    def test_invalid_tz(self):
        with self.assertRaises(ValidationError):
            sut = Event()
            sut.name = 'unimportant'
            sut.timezone = 'invalid/timezone'
            sut.save()

    def test_valid_tz(self):
        sut = Event()
        sut.name = 'unimportant'
        sut.timezone = 'Europe/Berlin'
        sut.save()

