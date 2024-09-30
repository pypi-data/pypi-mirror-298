import json
import logging
from typing import List, Tuple

from .gen_base_v3 import GenBaseV3
from .models import CourseArticleWTitleModel, CourseArticleKeypointsModel
from .utils import extract_json_from_text, get_native_languages, get_language_name_from_iso_639_1


class GenCourseKeypoints(GenBaseV3):
    """
    Generator class for course's article's keypoints.
    """
    PROMPT_NAME = "gen_articles_keypoints"

    def __init__(self, llm, lang: str, verbose: bool = False):
        self.logger = logging.getLogger(__name__)
        super().__init__(llm, lang, verbose, self.logger)

    def parse_output(self, output: str) -> List[CourseArticleKeypointsModel]:
        try:
            self.logger.debug(f"Parsing output: {output}")
            articles = extract_json_from_text(output)["articles"]
            return [CourseArticleKeypointsModel(**article) for article in articles]
        except json.JSONDecodeError:
            self.logger.error(f"Output is not a valid JSON: {output}")
            raise

    def generate(self,
                 course_title: str,
                 course_description: str,
                 num_articles: int = 10,
                 ) -> List[CourseArticleKeypointsModel]:
        return self.generate_output(
            course_title=course_title,
            course_description=course_description,
            num_articles=num_articles,
        )


class _TranslateCourseContent(GenBaseV3):
    """
    Generator class for translating course's article's content in batch.
    """
    PROMPT_NAME = "translate_articles_content"

    def __init__(self, llm, lang: str = "en", verbose: bool = False):
        self.logger = logging.getLogger(__name__)
        super().__init__(llm, lang, verbose, self.logger)

    def parse_output(self, output: str) -> List[CourseArticleWTitleModel]:
        self.logger.debug(f"Parsing output: {output}")
        articles = extract_json_from_text(output)["articles"]
        return [CourseArticleWTitleModel(**article) for article in articles]

    def generate(self,
                 articles: str,
                 target_lang: str,
                 ) -> List[CourseArticleWTitleModel]:

        translated_content = self.generate_output(
            articles_content=articles,
            target_lang=target_lang,
        )

        return translated_content


class GenCourseContent(GenBaseV3):
    """
    Generator class for course's article's content in batch using articles keypoints.
    """
    PROMPT_NAME = "gen_articles_content"

    def __init__(self, llm, lang: str, verbose: bool = False):
        self.logger = logging.getLogger(__name__)
        self.output_lang = lang
        if lang not in get_native_languages():
            self.logger.warning(f"Language '{lang}' is not in the list of native languages. "
                                f"Setting language to 'en' (English).")
            lang = "en"
            self.translator = _TranslateCourseContent(llm, lang, verbose)
        super().__init__(llm, lang, verbose, self.logger)
        self.keypoints_generator = GenCourseKeypoints(llm, lang, verbose)

    def parse_output(self, output: str) -> Tuple[List[CourseArticleWTitleModel], str]:
        self.logger.debug(f"Parsing output: {output}")
        articles = extract_json_from_text(output)["articles"]
        return [CourseArticleWTitleModel(**article) for article in articles], json.dumps({"articles": articles})

    def generate(self,
                 course_title: str,
                 course_description: str,
                 articles_count: int = 10,
                 max_words: int = 150,
                 min_words: int = 40,
                 ) -> List[CourseArticleWTitleModel]:

        articles_keypoints = self.keypoints_generator.generate(
            course_title=course_title,
            course_description=course_description,
            num_articles=articles_count,
        )

        titles_and_keypoints = ""
        for article in articles_keypoints:
            titles_and_keypoints += f"{article.to_plain_text()}\n\n"

        generated_content, json_output = self.generate_output(
            titles_and_keypoints=titles_and_keypoints,
            max_words=max_words,
            min_words=min_words,
            num_articles=articles_count
        )

        if self.output_lang not in get_native_languages():
            translated_content = self.translator.generate(
                articles=json_output,
                target_lang=get_language_name_from_iso_639_1(self.output_lang),
            )
            return translated_content

        return generated_content
