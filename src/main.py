import csv
import dataclasses
import pathlib
import tomllib
from datetime import date

from arxiv_papers import arxiv_papers, Configuration, CategoryQuery, Author, ArXivPaper


def main():
    category_queries = _get_category_queries()
    start = date(2025, 1, 28)
    end = date(2025, 3, 20)
    config = Configuration(category_queries=category_queries, start=start, end=end)
    papers = arxiv_papers(config)
    out = pathlib.Path("papers.csv")
    _save(papers, out)


def _get_category_queries() -> list[CategoryQuery]:
    # Read in the configuration data
    config_file = pathlib.Path(__file__).parent.parent / "config.toml"
    with open(config_file, "rb") as f:
        config_data = tomllib.load(f)

    # Loop over all the categories
    category_queries: list[CategoryQuery] = []
    for category in config_data["arxiv"]:
        authors = [
            _parse_author(author)
            for author in config_data["arxiv"][category]["authors"]
        ]
        category_query = CategoryQuery(category=category, authors=authors)
        category_queries.append(category_query)

    return category_queries


def _parse_author(author: str) -> Author:
    author_parts = author.split(",")
    if len(author_parts) != 2:
        message = (
            "The author name must be of the form family name, given_name. "
            "Neither the given name nor the family name may contain a comma."
        )
        raise ValueError(message)
    return Author(
        given_name=author_parts[1].strip(), family_name=author_parts[0].strip()
    )


def _save(papers: list[ArXivPaper], out: pathlib.Path) -> None:
    with open(out, "w") as f:
        fieldnames = [
            "id",
            "submitted",
            "updated",
            "authors",
            "title",
            "abstract",
            "url",
        ]
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
        csv_writer.writeheader()
        for paper in papers:
            csv_writer.writerow(dataclasses.asdict(paper))


if __name__ == "__main__":
    main()
