from django.test import TestCase

from stockyard.models import Laboratory
from stockyard.tests.factories import RepeatFactory
from stockyard.utils.stockyard_files import generate_stockyard_repeats_files, generate_stockyard_split_repeats_files


class StockyardFilesTestCase(TestCase):
    def setUp(self) -> None:
        laboratory = Laboratory.objects.create(name='california')
        self.repeats = RepeatFactory.create_batch(80, laboratory=laboratory)

    def test_stockyard_recall(self):
        results = generate_stockyard_repeats_files()
        self.assertEqual(len(results['files']), 4)
        self.assertEqual(results['samples'], 80)

    def test_stockyard_recall_split(self):
        results = generate_stockyard_split_repeats_files()
        self.assertEqual(len(results['files']), 7)
        self.assertEqual(results['samples'], 80)
