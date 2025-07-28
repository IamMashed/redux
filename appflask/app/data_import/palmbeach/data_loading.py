import csv
import os

# configure this variable depending on your machine's hardware configuration

CHUNK_SIZE = 100000


def read_txt_file_as_chunks(file_path, chunk_size, callback,
                            encoding='ISO_8859-1'):
    """
    Read file line by line regardless of its size

    :param encoding:
    :param file_path: absolute path of file to read
    :param chunk_size: size of data to be read at at time
    :param callback: callback method, def callback(data, eof)
    """

    def read_in_chunks(file_obj, size=5000):
        """
        Lazy function to read a file
        Default chunk size: 5000.
        """
        while True:
            data = file_obj.read(size)
            if not data:
                break
            yield data

    fp = open(file_path, encoding=encoding)
    data_left_over = None

    # loop through characters
    for chunk in read_in_chunks(fp, chunk_size):

        # if uncompleted data exists
        if data_left_over:
            # print('\n left over found')
            current_chunk = data_left_over + chunk
        else:
            current_chunk = chunk

        # split chunk by new line
        lines = current_chunk.splitlines()

        # check if line is complete
        if current_chunk.endswith("\n"):
            data_left_over = None

        else:
            data_left_over = lines.pop()

        # callback(data=lines, eof=False, file_path=file_path)
        for line in lines:
            callback(data=line, eof=False)
            pass

    if data_left_over:

        current_chunk = data_left_over
        if current_chunk is not None:
            lines = current_chunk.splitlines()
            # callback(data=lines, eof=False, file_path=file_path)

            for line in lines:
                callback(data=line, eof=False)
                pass

    callback(data=None, eof=True)


def append_row_to_csv(data: dict, file_path: str):
    file_exists = os.path.isfile(file_path)
    with open(file_path, 'a', newline='') as f:
        field_names = list(data.keys())
        writer = csv.DictWriter(f,
                                delimiter=',',
                                lineterminator='\n',
                                fieldnames=field_names
                                )

        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
