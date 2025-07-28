# flake8: noqa
import os
import sys
from datetime import datetime

# Supervisor unable to set env variables
# Implementing as a workaround

curdir = os.getcwd()
os.chdir('../..')
sys.path.insert(0, os.getcwd())
os.chdir(curdir)

import time
from pathlib import Path
from config import IMAGES_OBSERVER_DIR


class SimpleApplicationsWatcher:
    SUPPORTED_FORMATS = ('.pdf', )
    # SUPPORTED_FORMATS = ('.png', '.jpg', '.jpeg', '.pdf')
    STATUS_SUCCESS = 'status_success'
    STATUS_UNSUPPORTED = 'status_unsupported'
    STATUS_UNEXPECTED_ERROR = 'status_unexpected_error'

    processed_path = 'processed'  # Path to the processed files
    unprocessed_path = 'unprocessed'  # Path to the files that could not be processed. For example: wrong format

    def __init__(self):
        pass

    @staticmethod
    def ls_files(dir_path):
        for file_name in os.listdir(dir_path):
            if os.path.isfile(Path(dir_path) / file_name):
                yield Path(dir_path) / file_name

    @staticmethod
    def move_file(file_path, new_dir_path, app_id=None):
        # Move a file by renaming it's path to 'processed' directory
        new_file_name = os.path.basename(file_path.as_posix())
        if app_id:
            new_file_name = '_'.join([
                str(app_id), new_file_name
            ])
        else:
            # file moved to unprocessed, mark it with timestamp
            new_file_name = '_'.join([
                datetime.now().strftime("%H_%M_%S_%d_%m_%Y"), new_file_name
            ])
        os.rename(file_path.as_posix(), Path(new_dir_path) / new_file_name)
        return True

    @staticmethod
    def supported_format(file_path):
        filename, file_extension = os.path.splitext(file_path)
        return file_extension in SimpleApplicationsWatcher.SUPPORTED_FORMATS

    def run(self):
        from my_logger import logger

        # Initialize dirs
        base_dir = IMAGES_OBSERVER_DIR
        processed_dir = Path(base_dir) / self.processed_path
        unprocessed_dir = Path(base_dir) / self.unprocessed_path
        processed_dir.mkdir(parents=True, exist_ok=True)
        unprocessed_dir.mkdir(parents=True, exist_ok=True)

        while True:
            #  TODO: log the statuses for each file somewhere for traceability
            files_list = self.ls_files(base_dir)
            for file_path in files_list:
                # If the file is modified only a minute ago or less, then we skip it (might be in upload stage)
                diff = int(time.time()) - os.stat(file_path).st_mtime
                if diff < 60:
                    logger.info("Skipping file {} as too young".format(file_path))
                    continue

                app_id = None
                try:
                    app_id, process_file_status = self.process_file(file_path)
                except Exception as e:
                    logger.info("Exception processing file {}: {}".format(file_path, str(e)))
                    process_file_status = self.STATUS_UNEXPECTED_ERROR

                logger.info("DEBUG: Processed file " + str(file_path) + " Status: " + process_file_status)

                # move file to directory according to process file status
                if process_file_status == self.STATUS_SUCCESS:
                    self.move_file(file_path, processed_dir, app_id=app_id)
                else:
                    self.move_file(file_path, unprocessed_dir)

            print("Applications Watcher Heartbeat")
            time.sleep(30)

    def process_file(self, file_path):
        from my_logger import logger

        if not self.supported_format(file_path):
            return None, self.STATUS_UNSUPPORTED
        base_file = file_path.name
        logger.info(f'new application scan received: {base_file}')

        # when we receive a new scan, process and create physical application object
        from app.case_management.services import CaseService
        application_id = CaseService.make_physical_application(file_path)
        if application_id:
            logger.info(f'created physical application with id={application_id}')
            return application_id, self.STATUS_SUCCESS
        else:
            return None, self.STATUS_UNEXPECTED_ERROR


if __name__ == "__main__":
    print('Watch a directory for scan:')
    print(IMAGES_OBSERVER_DIR)
    SimpleApplicationsWatcher().run()
