"""
Generator for course's metadata(title, description, etc.) using the description as text.
"""
import json
import logging
from pydantic import BaseModel, Field

from .gen_base_v3 import GenBaseV3
from .utils import extract_json_from_text, get_native_languages


class CourseMetadataModel(BaseModel):
    title: str = Field(
        description="title of the course of only 3 words")
    description: str = Field(
        description="description of the course which is an introduction article of maximum 40 words")


class _TranslateCourseMetadata(GenBaseV3):
    """
    Generator class for translating course metadata.
    """
    PROMPT_NAME = "translate_course_metadata"

    def __init__(self, llm, lang: str = "en", verbose: bool = False):
        self.logger = logging.getLogger(__name__)
        super().__init__(llm, lang, verbose, self.logger)

    def parse_output(self, output: str) -> CourseMetadataModel:
        self.logger.debug(f"Parsing output: {output}")
        metadata = extract_json_from_text(output)
        return CourseMetadataModel(**metadata)

    def generate(self,
                 metadata: str,
                 target_lang: str,
                 ) -> CourseMetadataModel:

        translated_content = self.generate_output(
            target_lang=target_lang,
            metadata=metadata,
        )

        return translated_content


class GenCourseMetadata(GenBaseV3):
    """
    Generator class for course metadata(title, description, etc.) using the description as text.
    """
    PROMPT_NAME = "gen_course_title_desc"

    def __init__(self, llm, lang: str, verbose: bool = False):
        self.logger = logging.getLogger(__name__)
        self.output_lang = lang
        if lang not in get_native_languages():
            self.logger.warning(f"Language '{lang}' is not in the list of native languages. "
                                f"Setting language to 'en' (English).")
            lang = "en"
            self.translator = _TranslateCourseMetadata(llm, lang, verbose)
        super().__init__(llm, lang, verbose, self.logger)

    def parse_output(self, output: str) -> (CourseMetadataModel, str):
        try:
            self.logger.debug(f"Parsing output: {output}")
            metadata = extract_json_from_text(output)
            return CourseMetadataModel(**metadata), metadata
        except json.JSONDecodeError:
            self.logger.error(f"Output is not a valid JSON: {output}")
            raise

    def generate(self,
                 course_description: str,
                 ) -> CourseMetadataModel:

        model, metadata = self.generate_output(
            course_description=course_description,
        )

        if self.output_lang not in get_native_languages():
            translated_model = self.translator.generate(metadata=metadata, target_lang=self.output_lang)
            return translated_model

        return model
