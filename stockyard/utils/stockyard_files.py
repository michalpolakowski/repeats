import operator
import os
from functools import reduce
from itertools import zip_longest

import datetime
from django.conf import settings
from django.db.models import Count, Q

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


def grouper(iterable, n, fillvalue=None):
    """
    Collect data into fixed-length chunks or blocks
    :param iterable: collection to group
    :param n: how many elements in group
    :param fillvalue: value to fill
    :return: grouped collection
    """
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def generate_file_name():
    today = str(datetime.datetime.now().date())
    return today + settings.STOCKAYRD_FILE_NAME


def generate_stockyard_repeats_files():
    excludes_list = ['Pain_MA', 'ETS_MA', 'Barbs_MA']

    stockyard_recall_repeat_samples = Repeat.objects.filter(disabled=False, created__date=datetime.date.today(),
                                                            laboratory__name='california') \
        .exclude(reduce(operator.or_, (Q(batch_template__icontains=item) for item in excludes_list))) \
        .exclude(comment__icontains="client requested")

    stockyard_recall_repeat_samples_grouped = grouper(stockyard_recall_repeat_samples, settings.STOCKYARD_GROUP_COUNT)

    files_path = settings.LOCAL_STOCKYARD_REPEAT
    check_path(files_path)
    file_name = generate_file_name()

    generated_files = []

    for i, group in enumerate(stockyard_recall_repeat_samples_grouped, 1):
        generated_file_name = file_name + str(i) + '.txt'
        stockyard_file = os.path.join(files_path, generated_file_name)
        row = []

        for repeat in group:
            if repeat:
                row.append(repeat.accession)

        row_to_write = ''
        for element in row:
            if row_to_write:
                row_to_write += ',' + element
            else:
                row_to_write = element

        row_to_write += '\n'

        stockyard_open = open(stockyard_file, 'w')
        stockyard_open.write(row_to_write)
        stockyard_open.close()

        generated_files.append(generated_file_name)
        i += 1

    return {
        'files': generated_files,
        'samples': len(stockyard_recall_repeat_samples)
    }


def generate_stockyard_split_repeats_files():
    queryset_types = {
        1: 'multiple',
        2: 'methdl',
        3: 'dilution',
        4: 'other'
    }
    excludes_list = ['Pain_MA', 'ETS_MA', 'Barbs_MA']

    stockyard_recall_repeat_samples = Repeat.objects.filter(disabled=False, created__date=datetime.date.today(),
                                                            laboratory__name='california') \
        .exclude(reduce(operator.or_, (Q(batch_template__icontains=item) for item in excludes_list))) \
        .exclude(comment__icontains="client requested")
    no_of_samples = len(stockyard_recall_repeat_samples)

    list_of_querysets = []

    dupes = stockyard_recall_repeat_samples.values('accession').annotate(Count('id')).order_by().filter(id__count__gt=1)
    multiple = stockyard_recall_repeat_samples.filter(accession__in=[sample['accession'] for sample in dupes])
    multiple_ids = multiple.values('id')
    list_of_querysets.append(multiple)

    methdl_repeats = stockyard_recall_repeat_samples.filter(batch_template='METH_DL')
    list_of_querysets.append(methdl_repeats)
    meth_dl_ids = methdl_repeats.values('id')

    dilution_repeats = stockyard_recall_repeat_samples.filter(comment__startswith='Interference')
    list_of_querysets.append(dilution_repeats)
    dilution_ids = dilution_repeats.values('id')

    stockyard_recall_repeat_samples = stockyard_recall_repeat_samples \
        .exclude(id__in=multiple_ids) \
        .exclude(id__in=meth_dl_ids) \
        .exclude(id__in=dilution_ids)
    list_of_querysets.append(stockyard_recall_repeat_samples)

    all_generated_files = []
    for i, queryset in enumerate(list_of_querysets, 1):
        generated_files_of_type = []
        queryset_grouped = grouper(queryset, settings.STOCKYARD_GROUP_COUNT)
        files_path = settings.LOCAL_STOCKYARD_SPLIT_REPEAT
        check_path(files_path)
        file_name = generate_file_name()

        for j, group in enumerate(queryset_grouped, 1):
            generated_file_name = file_name + f'{queryset_types[i]}-' + str(j) + '.txt'
            stockyard_file = os.path.join(files_path, generated_file_name)
            row = []

            for repeat in group:
                if repeat:
                    row.append(repeat.accession)

            row_to_write = ''
            for element in row:
                if row_to_write:
                    row_to_write += ',' + element
                else:
                    row_to_write = element

            row_to_write += '\n'

            stockyard_open = open(stockyard_file, 'w')
            stockyard_open.write(row_to_write)
            stockyard_open.close()

            generated_files_of_type.append(generated_file_name)
            all_generated_files.append(generated_file_name)

    return {
        'files': all_generated_files,
        'samples': no_of_samples
    }
