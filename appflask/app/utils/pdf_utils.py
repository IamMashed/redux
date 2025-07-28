from PyPDF2 import PdfFileMerger


def merge_pdf_files(output_file_path, input_files=None):
    """
    Merge a list of pdf files

    :param output_file_path: The output path of the result .pdf file
    :param input_files: The list of file objects to merge / list of str path to files
    """
    if input_files is None:
        input_files = []

    merger = PdfFileMerger()

    for pdf in input_files:
        merger.append(pdf)

    merger.write(output_file_path)
    merger.close()
