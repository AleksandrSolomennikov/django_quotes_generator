from django.test import TestCase
from .models import Source, Quote

class QuoteModelTests(TestCase):
    def test_max_three_per_source(self):
        s = Source.objects.create(name='Test', type='other')
        for i in range(3):
            Quote.objects.create(source=s, text=f'Q{i}', weight=1)
        with self.assertRaises(Exception):
            Quote.objects.create(source=s, text='Q3', weight=1)

    def test_unique_text(self):
        s = Source.objects.create(name='S2', type='book')
        Quote.objects.create(source=s, text='Unique', weight=1)
        with self.assertRaises(Exception):
            Quote.objects.create(source=s, text='Unique', weight=2)