import json
import logging
from typing import List

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .gen_base_v3 import GenBaseV3
from .gen_course_articles import _TranslateCourseContent
from .models import CourseArticleWTitleModel
from .utils import extract_json_from_text, get_native_languages, get_language_name_from_iso_639_1


class GenSummaryFromDoc(GenBaseV3):
    PROMPT_NAME = "gen_doc_summary"

    def __init__(self, llm, lang: str, verbose: bool = False):
        self.logger = logging.getLogger(__name__)
        super().__init__(llm, lang, verbose, self.logger)

    def parse_output(self, output: str):
        try:
            self.logger.debug(f"Parsing output:\n{output}")
            return extract_json_from_text(output)["summary"]
        except json.JSONDecodeError:
            self.logger.error(f"Output is not a valid JSON: {output}")
            raise

    def generate(self, doc_content: str):
        return self.generate_output(
            text=doc_content
        )


class _TranslateDocCourseContent(GenBaseV3):
    """
    Generator class for translating course's article's content in batch.
    """
    PROMPT_NAME = "translate_articles_content_doc"

    def __init__(self, llm, lang: str = "en", verbose: bool = False):
        self.logger = logging.getLogger(__name__)
        super().__init__(llm, lang, verbose, self.logger)

    def parse_output(self, output: str):
        self.logger.debug(f"Parsing output: {output}")
        output_data = extract_json_from_text(output)
        articles = output_data["articles"]
        title = output_data["title"]
        description = output_data["description"]
        return {
            "title": title,
            "description": description,
            "articles": [CourseArticleWTitleModel(**article) for article in articles]
        }

    def generate(self,
                 title: str,
                 description: str,
                 articles: str,
                 target_lang: str,
                 ) -> List[CourseArticleWTitleModel]:

        translated_content = self.generate_output(
            title=title,
            description=description,
            articles_content=articles,
            target_lang=target_lang,
        )

        return translated_content


class GenCourseContentFromDoc(GenBaseV3):
    """
    Generator class for course's article's content in batch from document.
    """
    PROMPT_NAME = "gen_article_content_doc"

    def __init__(self, llm, lang: str, verbose: bool = False):
        self.logger = logging.getLogger(__name__)
        self.output_lang = lang
        if lang not in get_native_languages():
            self.logger.warning(f"Language '{lang}' is not in the list of native languages. "
                                f"Setting language to 'en' (English).")
            lang = "en"
            self.translator = _TranslateDocCourseContent(llm, lang, verbose)
        super().__init__(llm, lang, verbose, self.logger)
        self.summary_generator = GenSummaryFromDoc(llm, lang, verbose)

    def parse_output(self, output: str):
        try:
            self.logger.debug(f"Parsing output:\n{output}")
            course_info = extract_json_from_text(output)
            articles = course_info["articles"]
            article_models = [CourseArticleWTitleModel(**article) for article in articles]
            return {
                "title": course_info["title"],
                "description": course_info["description"],
                "articles": article_models,
            }, articles
        except json.JSONDecodeError:
            self.logger.error(f"Output is not a valid JSON: {output}")
            raise

    def _gen_summaries(self, docs):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=12000, chunk_overlap=1000)
        split_docs = text_splitter.split_text(docs)

        summaries = []
        for doc in split_docs:
            summary = self.summary_generator.generate(doc)
            summaries.append(summary)

        return summaries

    def generate(self,
                 file_path: str,
                 articles_count: int = 10,
                 max_words: int = 150,
                 min_words: int = 40,
                 ):
        docs = load_docs(file_path)
        summaries = self._gen_summaries(docs)

        summaries_string = ""
        for index, summary in enumerate(summaries):
            if index == 0:
                summaries_string += summary
            else:
                summaries_string += "\n\n" + summary

        generated_content, json_output = self.generate_output(
            articles_count=articles_count,
            max_words=max_words,
            min_words=min_words,
            text=summaries_string
        )

        if self.output_lang not in get_native_languages():
            translated_content = self.translator.generate(
                title=generated_content["title"],
                description=generated_content["description"],
                articles=json_output,
                target_lang=get_language_name_from_iso_639_1(self.output_lang),
            )
            return translated_content

        return generated_content


def load_docs(file_path):
    loader = PyMuPDFLoader(file_path=file_path)
    docs = loader.load()

    combined_text = ""
    for doc in docs:
        combined_text += doc.page_content

    return combined_text
