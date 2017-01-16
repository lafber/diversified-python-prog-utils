"""

Extracting from a pdf the text and cleaning it

This CLI program is used to extract from a pdf file
the text cleaning unnecessary elements like ending page number.

    Arguments:
    input file name
    '-h': help file of usage of the script
    '-o': output file name, by default the input pdf name in txt
    '-c': cleaning options

    Default settings:
    'output_path' is the current directory
    'output file name' is the input file with txt extension

    Example usage:
    >> python3 pdf_to_clean_text.py input/churchillww1_index_pers.pdf

    [TODO] implement cleaning options as they are all forced atm

"""

# Modules importation
import os
import argparse
from PyPDF2 import PdfFileReader
import re

# Constants

# Globals Variables

# Functions


def get_arguments():
    """ Define CLI parameters and then get user supplied arguments """

    # Define a new parser to parse the command line in Python
    parser = argparse.ArgumentParser(description="extract from a pdf its text")

    # Define arguments coming from the command line
    parser.add_argument("input_file",
                        help="pdf input file with extension", type=str)
    parser.add_argument("-o", "--output_file",
                        help="txt output file with extension", type=str)
    parser.add_argument("-c", "--cleaning", required=False,
                        help="cleaning options: pages, spaces, unwrap")

    # parsing user supplied command line arguments
    args = parser.parse_args()

    # checking input pdf file
    is_valid_file(parser, args.input_file, ".pdf", "input")

    # If not output file specified we generate a default output file in
    # the same directory as the input file and with the same name
    if not args.output_file:
        args.output_file = args.input_file.replace(".pdf", ".txt")

    return args.input_file, args.output_file, args.cleaning


def is_valid_file(parser, file, file_ext, file_io):
    """ Checking that the input file exist and is a pdf """

    if not os.path.exists(file):
        parser.error("The {} file {} does not exist.".format(file_io, file))
        parser.exit()
    elif not file.endswith(file_ext):
        parser.error("The {} file {} extension is not .pdf".format(file_io,
                                                                   file))
        parser.exit()
    else:
        print("The {} file {} is valid".format(file_io, file))


def parse_file(arguments):
    """ Parsing pdf file to extract the text and generate a txt file """

    all_text = ""
    input_file = arguments[0]

    pdf_input_file = PdfFileReader(open(str(input_file), "rb"))

    # extract from each page in the pdf the text
    for page_num in range(0, pdf_input_file.getNumPages()):
        page = pdf_input_file.getPage(page_num)
        if page.extractText():
            all_text += page.extractText()
            print("Text successfuly extracted from page {}/{}"
                  .format(page_num+1, pdf_input_file.getNumPages()))

    return cleaning_unwrap(all_text)


def cleaning_unwrap(text):
    """ clean text from artefact"""

    #  Remove all line feed and carriage return
    cleaned_text = re.subn(r"\n|\r|\r\n", "", text)
    print("{} line break replaced".format(cleaned_text[1]))

    # Remove all page numbers
    cleaned_text = re.subn(r"\d{1,3}.", "", cleaned_text[0])
    print("{} page references removed".format(cleaned_text[1]))

    # Remove multiple spaces
    cleaned_text = re.subn(r"\s{1,}", " ", cleaned_text[0])
    print("{} multiple spaces removed".format(cleaned_text[1]))

    # Add line feed in place of ":"
    cleaned_text = re.subn(r":", "\n", cleaned_text[0])
    print("{} line feed added".format(cleaned_text[1]))

    return cleaned_text[0]


def generate_output_file(text, output_file):
    """ Generate the text output file and append all the extracted text
        from the pdf """

    with open(output_file, 'w') as txt_output:
        txt_output.write(text)
    print("Output file {} successfuly created".format(output_file))


# MAIN
if __name__ == "__main__":
    arguments = get_arguments()
    generate_output_file(parse_file(arguments), arguments[1])
