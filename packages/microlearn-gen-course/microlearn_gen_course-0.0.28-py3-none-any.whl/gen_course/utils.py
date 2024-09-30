import json
import logging
import re
import json_repair
from typing import List

_iso_639_1_to_language = {
    'en': ('English', 'English'),
    'es': ('Spanish', 'Español'),
    'fr': ('French', 'Français'),
    'de': ('German', 'Deutsch'),
    'it': ('Italian', 'Italiano'),
    'pt': ('Portuguese', 'Português'),
    'ru': ('Russian', 'Русский'),
    'zh': ('Chinese (Simplified)', '中文'),
    'ja': ('Japanese', '日本語'),
    'ko': ('Korean', '한국어'),
    'ar': ('Arabic', 'العربية'),
    'hi': ('Hindi', 'हिन्दी'),
    'bn': ('Bengali', 'বাংলা'),
    'id': ('Indonesian', 'Bahasa Indonesia'),
    'tr': ('Turkish', 'Türkçe'),
    'vi': ('Vietnamese', 'Tiếng Việt'),
    'th': ('Thai', 'ไทย'),
    'pl': ('Polish', 'Polski'),
    'uk': ('Ukrainian', 'Українська'),
    'nl': ('Dutch', 'Nederlands'),
    'ro': ('Romanian', 'Română'),
    'sv': ('Swedish', 'Svenska'),
    'da': ('Danish', 'Dansk'),
    'fi': ('Finnish', 'Suomi'),
    'no': ('Norwegian', 'Norsk'),
    'el': ('Greek', 'Ελληνικά'),
    'he': ('Hebrew', 'עברית'),
    'hu': ('Hungarian', 'Magyar'),
    'cs': ('Czech', 'Čeština'),
    'sk': ('Slovak', 'Slovenčina'),
    'bg': ('Bulgarian', 'Български')
}

_native_languages = ["en", "it"]


def extract_json_from_text(text):
    """
    Extracts JSON content from a given text.

    Args:
    text (str): Text from which JSON content needs to be extracted.

    Returns:
    dict: Json content extracted from the text.
    """
    logger = logging.getLogger(__name__)
    json_pattern = re.compile(r'((\[[^\}]{3,})?\{s*[^\}\{]{3,}?:.*\}([^\{]+\])?)', re.DOTALL)
    match = json_pattern.search(text)

    if match:
        json_str = match.group(0)
        try:
            json_data = json.loads(json_str)
            return json_data
        except json.JSONDecodeError:
            try:
                logger.warning("JSON is not valid. Trying to repair it.")
                json_reparied = json_repair.loads(json_str)
                logger.info(f"JSON repaired successfully:\n\n=====================\nOriginal JSON:\n{json_str}\n\nRepaired JSON:\n{json_reparied}\n=====================")
                return json_reparied
            except json.JSONDecodeError as e:
                raise e
    else:
        raise


def remove_html(html_string):
    """
    Function that removes HTML tags from a string.

    Args:
        html_string: str

    Returns:
        str: String without HTML tags
    """
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html_string)


def remove_markdown(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)

    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)

    text = re.sub(r'`(.*?)`', r'\1', text)
    text = re.sub(r'```[\s\S]+?```', '', text)

    text = re.sub(r'^\s*#(#+)\s+', '', text, flags=re.MULTILINE)
    return text


def get_native_languages() -> List[str]:
    """
    Function that returns the native languages.

    Returns:
        list[str]: Native languages
    """
    return _native_languages


def get_supported_languages_iso_639_1() -> dict[str:(str, str)]:
    """
    Function that returns the supported languages with their ISO 639-1 codes.

    Returns:
        dict[str:(str, str)]: Supported languages with their ISO 639-1 codes
    """
    return _iso_639_1_to_language


def get_iso_639_1_from_language_name(language_name: str) -> str:
    """
    Function that returns the ISO 639-1 code from the language name.

    Args:
        language_name: str

    Returns:
        str: ISO 639-1 code or None if not found
    """
    iso_639_1 = {v[0]: k for k, v in _iso_639_1_to_language.items()}.get(language_name, None)
    if iso_639_1 is None:
        iso_639_1 = {v[1]: k for k, v in _iso_639_1_to_language.items()}.get(language_name, None)
    return iso_639_1


def get_language_name_from_iso_639_1(iso_639_1: str) -> (str, str):
    """
    Function that returns the language name from the ISO 639-1 code.

    Args:
        iso_639_1: str

    Returns:
        (str, str): Language name in English and in the language itself
    """
    language_name = _iso_639_1_to_language.get(iso_639_1, None)
    return language_name