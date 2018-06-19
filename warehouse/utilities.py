import json
import os

from django.db import transaction

from warehouse.markets.models import CurrencyTicker
from warehouse.settings import s3_client, S3_BUCKET_NAME, BACKUP_DIR


def get_backup_path(name):
    from warehouse.settings import BACKUP_DIR

    return os.path.join(BACKUP_DIR, name)


def upload_to_s3(file_path, filename):
    return s3_client.upload_file(file_path, S3_BUCKET_NAME, filename)


def upload_backup_to_s3(backup_filename):
    file_path = get_backup_path(backup_filename)

    return upload_to_s3(file_path, backup_filename)


# TODO: remove me once backups are fixed
def get_tickers_from_file(filename):
    file_path = get_backup_path(filename)

    with open(file_path, 'r') as f:
        file_contents = f.read()

    entries = [
        '{' + entry + '}'
        for entry in file_contents.split('}{')
    ]
    entries[0] = entries[0][1:]
    entries[1] = entries[-1][:-2]

    return [
        CurrencyTicker(**json.loads(entry))
        for entry in entries
    ]


def list_s3_file_names():
    files_response = s3_client.list_objects(Bucket=S3_BUCKET_NAME)

    return [f['Key'] for f in files_response['Contents']]


def download_s3_file(filename, file_path):
    return s3_client.download_file(Bucket=S3_BUCKET_NAME, Key=filename, Filename=file_path)


def download_all_backups_from_s3():
    file_names = list_s3_file_names()
    existing_backups = os.listdir(BACKUP_DIR)
    needed_backups = list(set(file_names) - set(existing_backups))

    for backup_name in needed_backups:
        backup_path = get_backup_path(backup_name)
        download_s3_file(backup_name, backup_path)


def restore_tickers_from_backup(backup):
    file_path = os.path.join(BACKUP_DIR, backup)

    with open(file_path, 'r') as f:
        lines = [json.loads(line) for line in f.readlines()]

    existing_uuids = set([
        str(uuid)
        for uuid in CurrencyTicker.objects.all().values_list('uuid')
    ])

    with transaction.atomic():
        for line in lines:
            line_uuid = str(line['uuid'])

            if line_uuid in existing_uuids:
                continue

            CurrencyTicker(**line).save()


def restore_tickers_from_s3():
    download_all_backups_from_s3()

    for backup_name in os.listdir(BACKUP_DIR):
        restore_tickers_from_backup(backup_name)
