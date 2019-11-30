from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class Laboratory(models.Model):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

    name = models.CharField(
        max_length=100,
        validators=[alphanumeric, ]
    )

    def __str__(self):
        return self.name


class Repeat(models.Model):
    accession = models.CharField(max_length=15)
    analyte = models.CharField(max_length=50)
    comment = models.CharField(max_length=50, null=True, blank=True)
    entered_by = models.CharField(max_length=20, null=True, blank=True)
    row_position = models.IntegerField(default=0)
    repeat_date = models.DateField(default=None, null=True, blank=True)
    remark = models.CharField(max_length=50, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

    batch_template = models.CharField(max_length=50, null=True, blank=True)

    disabled = models.BooleanField(default=False)
    file_name = models.CharField(default='', max_length=90, blank=True, null=True)
    deactivation_date = models.DateTimeField(default=None, null=True, blank=True)
    archivum_file = models.CharField(default='', max_length=90, blank=True, null=True)
    translated_at = models.DateTimeField(default=timezone.now)
    laboratory = models.ForeignKey(Laboratory, null=True, blank=True, on_delete=models.SET_NULL)
    inventory_check = models.BooleanField(default=False)

    def __str__(self):
        return 'Repeat sample: {}'.format(self.accession)
