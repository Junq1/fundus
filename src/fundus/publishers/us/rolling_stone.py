import datetime
from typing import List, Optional

from lxml.cssselect import CSSSelector

from fundus.parser import ArticleBody, BaseParser, ParserProxy, attribute
from fundus.parser.utility import (
    extract_article_body_with_selector,
    generic_author_parsing,
    generic_date_parsing,
    generic_topic_parsing,
)


class RollingStoneParser(ParserProxy):
    class V1(BaseParser):
        _paragraph_selector = CSSSelector("div.a-content > * > p.paragraph")
        _summary_selector = CSSSelector("article > header > div.article-excerpt")
        _subheadline_selector = CSSSelector("article > header > div.article-kicker")

        @attribute
        def body(self) -> ArticleBody:
            return extract_article_body_with_selector(
                self.precomputed.doc,
                paragraph_selector=self._paragraph_selector,
                summary_selector=self._summary_selector,
                subheadline_selector=self._subheadline_selector,
            )

        @attribute
        def authors(self) -> List[str]:
            return generic_author_parsing(self.precomputed.meta.get("author"))

        @attribute
        def publishing_date(self) -> Optional[datetime.datetime]:
            return generic_date_parsing(self.precomputed.meta.get("published_at"))

        @attribute
        def title(self) -> Optional[str]:
            return self.precomputed.meta.get("title")

        @attribute
        def topics(self) -> List[str]:
            return generic_topic_parsing(self.precomputed.meta.get("topics"))
