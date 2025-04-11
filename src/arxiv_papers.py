import dataclasses
from datetime import date, datetime

import arxiv
from openpyxl.workbook import Workbook


@dataclasses.dataclass()
class Author:
    """
    An author.

    Note that arXiv queries only use an author's family name (surname).

    Parameters
    ----------
    given_name:
        The author's given name (first name).
    family_name:
        The author's family name (surname).
    """

    given_name: str
    family_name: str

    def __str__(self):
        return f"{self.given_name} {self.family_name}"


@dataclasses.dataclass()
class CategoryQuery:
    """
    The parameters for a subject category query.

    These parameters include the subject category and a list of authors to query. The
    category must be one of the arXiv's categories, such as astro-ph or q-bio.

    Parameters
    ----------
    category:
        The arXiv subject category, such astro-ph.
    authors:
        The list of authors to query.
    """

    category: str
    authors: list[Author]


@dataclasses.dataclass()
class ArXivPaper:
    """
    Details about a paper on the arXiv.

    Parameters
    ----------
    id:
        The entry id, such as 2503.02829v1.
    submitted:
        The date and time when the paper was submitted.
    updated:
        The date and time when the paper was last updated.
    authors:
        The authors.
    title:
        The title of the paper.
    abstract:
        The abstract of the paper.
    url:
        The URL of the arXiv page for the paper.
    """

    id: str
    submitted: datetime
    updated: datetime
    authors: list[str]
    title: str
    abstract: str
    url: str


@dataclasses.dataclass()
class Configuration:
    """
    The configuration for the arXiv query.

    The configuration includes a list of catalog queries, a start date and an end date.
    Each catalog query consists of a catalog name and a list of authors. For each of
    these catalog queries the arXiv is queried for papers published between the start
    and end date, where the start date is inclusive and the end date exclusive. For
    example, if you want to query papers published in April 2025, you should choose
    1 April 2025 as the start date and 1 May 2025 as the end date.

    Parameters
    ----------
    category_queries:
        The list of subject categories and authors to query for them.
    start:
        The start date, inclusive.
    end:
        The end date, exclusive.
    """

    category_queries: list[CategoryQuery]
    start: date
    end: date


def arxiv_papers(config: Configuration) -> Workbook:
    """
    Query the arxiv for a list of papers.

    The query is performed for a list of authors and a date range. Both the start and
    end date of the date range are inclusive, i.e. papers published on the start or end
    date are included.

    Parameters
    ----------
    config:
        The query configuration.

    Returns
    -------
    An Excel workbook with the papers found.
    """
    pass


class ArXiv:
    """
    A class for querying the arXiv.

    The main purpose of the class is to ensure that the same client is used for all
    queries, as this ensures that the rate limits for the arXiv API are honoured.
    """

    _client: arxiv.Client | None = None

    def __init__(self):
        if ArXiv._client is None:
            ArXiv._client = arxiv.Client()

    def query_arxiv(
        self, category: str, author: Author, start: date, end: date
    ) -> list[ArXivPaper]:
        """
        Query the arXiv for a list of papers.

        The given catalog is queried for all the papers published between the given
        start date (inclusive) and end date (exclusive) by the given author.

        Parameters
        ----------
        category:
            The arXiv subject category to query.
        author:
            The author to query for.
        start:
            The start date from which to query, inclusive.
        end:
            The end date until which to query, exclusive.

        Returns
        -------
        The query results.
        """
        pass
