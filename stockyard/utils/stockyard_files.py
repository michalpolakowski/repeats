import os
from itertools import zip_longest

import datetime
from django.conf import settings

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
    # generate stockyard recall files, excluding MA lab and client requested
    stockyard_recall_repeat_samples = Repeat.objects.exclude(comment__icontains="client requested")\
        .exclude(batch_template__icontains="Pain_MA") \
        .exclude(batch_template__icontains="ETS_MA") \
        .exclude(batch_template__icontains="Barbs_MA") \
        .filter(disabled=False, created__date=datetime.date.today(), laboratory__name='california')

    stockyard_recall_repeat_samples_grouped = grouper(stockyard_recall_repeat_samples, settings.STOCKYARD_GROUP_COUNT)

    i = 1
    files_path = settings.LOCAL_STOCKYARD_REPEAT
    check_path(files_path)
    file_name = generate_file_name()

    generated_files = []

    for group in stockyard_recall_repeat_samples_grouped:
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
