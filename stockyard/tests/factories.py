import factory
from django.utils import timezone

from stockyard.models import Repeat

ACCESSIONS_DUPLICATES = [integer for integer in range(1, 30) for _ in (1, 0)]
ACCESSIONS = ACCESSIONS_DUPLICATES + [integer for integer in range(30, 80)]
BATCH_TEMPLATES = ['MethDL', None]
COMMENTS = ['Interference 1:10', 'Interference 1:5', 'Interference 1:50', None]


class RepeatFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Repeat

    accession = factory.Iterator(ACCESSIONS)
    batch_template = factory.Iterator(BATCH_TEMPLATES)
    comment = factory.Iterator(COMMENTS)
    repeat_date = factory.LazyFunction(timezone.localdate)
    row_position = factory.sequence(lambda n: n)

