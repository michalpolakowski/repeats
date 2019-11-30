import datetime
import operator
import os
from functools import reduce
from itertools import zip_longest, chain

from django.conf import settings
from django.db.models import Count, Q, QuerySet

from stockyard.models import Repeat


def check_path(path):
    """
    Method to check if specified path exist.
    If not create this path.
    :param path: specified path to check
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)


class StockyardRepeatsFilesGenerator:
    def __init__(self, split):
        self._split = split
        self._files_path = settings.LOCAL_STOCKYARD_SPLIT_REPEAT if self._split else settings.LOCAL_STOCKYARD_REPEAT
        self._file_name = self._generate_file_name()
        excludes_list = ['Pain_MA', 'ETS_MA', 'Barbs_MA']
        todays_repeats = Repeat.objects.filter(created__date=datetime.date.today(),
                                               laboratory__name='california')
        reps_with_excluded_assays = todays_repeats.exclude(
            reduce(operator.or_, (Q(batch_template__icontains=item) for item in excludes_list))
        )
        self._stockyard_recall_repeat_samples = reps_with_excluded_assays.exclude(comment__icontains="client requested")
        self._queryset_types = {
            1: 'multiple',
            2: 'methdl',
            3: 'dilution',
            4: 'other'
        }

    @staticmethod
    def _generate_file_name():
        today = str(datetime.datetime.now().date())
        return today + settings.STOCKAYRD_FILE_NAME

    def generate_files(self):
        if self._split:
            return self._generate_stockyard_split_repeats_files()
        return self._generate_stockyard_repeats_files()

    def _generate_stockyard_repeats_files(self):
        stockyard_recall_repeat_samples_grouped = self._grouper(self._stockyard_recall_repeat_samples,
                                                                settings.STOCKYARD_GROUP_COUNT)
        check_path(self._files_path)

        generated_files = []

        for i, group in enumerate(stockyard_recall_repeat_samples_grouped, 1):
            generated_file_name = f'{self._file_name}{str(i)}.txt'
            self._save_row_to_file(group, generated_file_name)

            generated_files.append(generated_file_name)

        return {
            'files': generated_files,
            'samples': len(self._stockyard_recall_repeat_samples)
        }

    def _generate_stockyard_split_repeats_files(self):
        all_generated_files = []

        list_of_querysets = self._split_querysets()

        for i, queryset in enumerate(list_of_querysets, 1):
            generated_files_of_type = []
            queryset_grouped = self._grouper(queryset, settings.STOCKYARD_GROUP_COUNT)
            check_path(self._files_path)

            for j, group in enumerate(queryset_grouped, 1):
                generated_file_name = f'{self._file_name}{self._queryset_types[i]}-{str(j)}.txt'
                self._save_row_to_file(group, generated_file_name)

                generated_files_of_type.append(generated_file_name)
                all_generated_files.append(generated_file_name)

        return {
            'files': all_generated_files,
            'samples': len(self._stockyard_recall_repeat_samples)
        }

    def _split_querysets(self):
        list_of_querysets = []

        dupes = self._stockyard_recall_repeat_samples.values('accession').annotate(Count('id')).order_by().filter(
            id__count__gt=1)

        # getting multiple repeats and their ids
        multiple = self._stockyard_recall_repeat_samples \
            .filter(accession__in=[sample['accession'] for sample in dupes]) \
            .exclude(comment__startswith='Interference')
        multiple_ids = [rep.id for rep in multiple]
        list_of_querysets.append(multiple)

        # getting methdl repeats and their ids
        methdl_repeats = self._stockyard_recall_repeat_samples.filter(batch_template='MethDL')
        methdl_ids = [rep.id for rep in methdl_repeats]
        list_of_querysets.append(methdl_repeats)

        # getting repeats with dilution and their ids
        dilution_repeats = self._stockyard_recall_repeat_samples.filter(comment__startswith='Interference')
        dilution_ids = [rep.id for rep in dilution_repeats]
        list_of_querysets.append(dilution_repeats)

        # getting other repeats
        ids = list(chain(multiple_ids, methdl_ids, dilution_ids))
        stockyard_recall_repeat_samples = self._stockyard_recall_repeat_samples.exclude(id__in=ids)
        list_of_querysets.append(stockyard_recall_repeat_samples)
        return list_of_querysets

    @staticmethod
    def _grouper(iterable, n: int, fillvalue=None):
        """
        Collect data into fixed-length chunks or blocks
        :param iterable: collection to group
        :param n: how many elements in group
        :param fillvalue: value to fill
        :return: grouped collection
        """
        args = [iter(iterable)] * n
        return zip_longest(fillvalue=fillvalue, *args)

    @staticmethod
    def _save_row_to_file(group, stockyard_file):
        row = [repeat.accession for repeat in group if repeat]

        row_to_write = row[0]
        for element in row[1:]:
            row_to_write += ',' + element

        row_to_write += '\n'

        stockyard_open = open(stockyard_file, 'w')
        stockyard_open.write(row_to_write)
        stockyard_open.close()
