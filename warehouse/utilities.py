import os
import time

from warehouse.settings import s3_client, S3_BUCKET_NAME


class ChoiceEnum(object):
    def __init__(self, names_enums):
        self.names_enums = names_enums

    def as_choices(self):
        return tuple(
            (enum, name)
            for name, enum in self.names_enums.iteritems()
        )

    def names(self):
        return self.names_enums.keys()

    def __getitem__(self, item):
        return self.names_enums[item]


def upload_to_s3(file_path, filename):
    return s3_client.upload_file(file_path, S3_BUCKET_NAME, filename)


def get_backup_path(name):
    return os.path.join(os.getcwd(), 'backups/txt/%s' % name)


def upload_backup_to_s3(backup_filename):
    file_path = get_backup_path(backup_filename)

    return upload_to_s3(file_path, backup_filename)


def list_s3_file_names():
    files_response = s3_client.list_objects(Bucket=S3_BUCKET_NAME)

    return [f['Key'] for f in files_response['Contents']]


def download_s3_file(filename, file_path):
    return s3_client.download_file(Bucket=S3_BUCKET_NAME, Key=filename, Path=file_path)


def download_all_backups_from_s3():
    file_names = list_s3_file_names()

    for backup_name in file_names:
        backup_path = get_backup_path(backup_name)
        download_s3_file(backup_name, backup_path)


