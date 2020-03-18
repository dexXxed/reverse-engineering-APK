import argparse
from argparse import RawTextHelpFormatter
import json
import os
import re
import sys
import logging
from datetime import datetime

from ninjadroid.use_cases.get_apk_info_in_html import GetApkInfoInHtml
from ninjadroid.use_cases.get_apk_info_in_json import GetApkInfoInJson
from ninjadroid.use_cases.extract_apk_entries import ExtractApkEntries
from ninjadroid.errors.apk_parsing_error import APKParsingError
from ninjadroid.errors.parsing_error import ParsingError
from ninjadroid.parsers.apk import APK

logger = logging.getLogger("NinjaDroid")


def read_target_file(filepath: str, no_string_processing: bool):
    apk = None
    print("Reading target apk...")
    try:
        apk = APK(filepath, no_string_processing)
    except APKParsingError:
        print("The target file (i.e. '%s') must be an APK package!", filepath)
    except ParsingError:
        print("The target file (i.e. '%s') must be an existing, readable file!", filepath)
    return apk


def get_apk_filename_without_extension(filepath: str) -> str:
    filename = os.path.basename(filepath)
    if re.search("\.apk", filepath, re.IGNORECASE):
        filename = str(filename[0:-4])
    return filename


def extract_apk_info_to_directory(apk: APK, filepath: str, filename: str, output_directory: str):
    """
    Extract all the APK entries and info to a given directory.

    :param apk: The APK class object.
    :param filepath: The target APK file path.
    :param filename: The target APK file name.
    :param output_directory: The directory where to save the APK entries and info.
    """
    if output_directory == "./":
        output_directory += filename
    print("Target: " + filepath)
    extract_apk_entries(apk, filepath, filename, output_directory)
    get_apk_info(apk, filename, output_directory)


def extract_apk_entries(apk: APK, filepath: str, filename: str, output_directory: str):
    ExtractApkEntries(apk, filepath, filename, output_directory, logger).execute()


def get_apk_info(apk: APK, filename: str, output_directory: str):
    GetApkInfoInHtml(apk, filename, output_directory, logger).execute()
    GetApkInfoInJson(apk, filename, output_directory, logger).execute()


def complete_apk_analyze(filename, path):
    apk = read_target_file(filename, True)

    if apk is None:
        sys.exit(1)

    filename_1 = get_apk_filename_without_extension(filename)

    extract_apk_info_to_directory(apk, filename, filename_1, f"./{path}/{filename}-{datetime.now().strftime('%d.%m.%Y-%H:%M:%S')}/")
