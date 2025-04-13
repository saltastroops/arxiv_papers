import dataclasses
from datetime import date

import arxiv


@dataclasses.dataclass(frozen=True)
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


@dataclasses.dataclass(frozen=True)
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


@dataclasses.dataclass(frozen=True)
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
    submitted: str
    updated: str
    authors: str
    title: str
    abstract: str
    url: str

    def __lt__(self, other: "ArXivPaper") -> bool:
        return self.id < other.id


@dataclasses.dataclass(frozen=True)
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


def arxiv_papers(config: Configuration) -> set[ArXivPaper]:
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
    arxiv_ = ArXiv()
    category_queries = config.category_queries
    papers: list[ArXivPaper] = []
    for category_query in category_queries:
        category = category_query.category
        for author in category_query.authors:
            papers.extend(
                arxiv_.query_arxiv(category, author, config.start, config.end)
            )

    return set(papers)


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
    ) -> set[ArXivPaper]:
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
        au = author.family_name.lower().replace(" ", "_")
        cat = category
        submitted_date = (
            "["
            + start.strftime("%Y%m%d0000")
            + " TO "
            + end.strftime("%Y%m%d0000")
            + "]"
        )
        query = f"cat:{cat}.* AND au:{au} AND submittedDate:{submitted_date}"
        search = arxiv.Search(
            query=query, max_results=100, sort_by=arxiv.SortCriterion.LastUpdatedDate
        )
        results = self._client.results(search)
        return set(self._parse_result(result) for result in results)

    @staticmethod
    def _parse_result(result: arxiv.Result) -> ArXivPaper:
        return ArXivPaper(
            id=result.entry_id.split("/")[-1],
            submitted=result.published.strftime("%Y-%m-%d %H:%M"),
            updated=result.updated.strftime("%Y-%m-%d %H:%M"),
            authors="|".join([a.name for a in result.authors]),
            title=result.title,
            abstract=result.summary,
            url=result.entry_id,
        )
