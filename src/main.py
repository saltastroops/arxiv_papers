import csv
import dataclasses
import pathlib
import tomllib
from datetime import datetime
from typing import Annotated

import typer
from arxiv_papers import arxiv_papers, Configuration, CategoryQuery, Person, ArXivPaper


def query(
    start: Annotated[
        datetime,
        typer.Option(
            ...,
            help="The start date from which to query for (inclusive).",
            prompt="Start date (inclusive)",
            formats=["%Y-%m-%d"],
        ),
    ],
    end: Annotated[
        datetime,
        typer.Option(
            ...,
            help="The end date until which to query for (exclusive).",
            prompt="End date (exclusive)",
            formats=["%Y-%m-%d"],
        ),
    ],
):
    try:
        category_queries = _get_category_queries()
        start_date = start.date()
        end_date = end.date()
        config = Configuration(
            category_queries=category_queries, start=start_date, end=end_date
        )
        papers = arxiv_papers(config)
        out = pathlib.Path(
            f"SAAO_Papers_{start.strftime('%Y-%m-%d')}_to_{end.strftime('%Y-%m-%d')}.csv"
        )
        _save(sorted(papers), out)
    except Exception as e:
        typer.secho(str(e), fg=typer.colors.RED, bold=True)
        raise typer.Exit(1)


def _get_category_queries() -> list[CategoryQuery]:
    # Read in the configuration data
    config_file = pathlib.Path(__file__).parent.parent / "config.toml"
    if not config_file.exists():
        raise ValueError(f"Configuration file not found: {str(config_file.absolute())}")
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


def _parse_author(author: str) -> Person:
    author_parts = author.split(",")
    if len(author_parts) != 2:
        message = (
            "The author name must be of the form family name, given_name. "
            "Neither the given name nor the family name may contain a comma."
        )
        raise ValueError(message)
    return Person(
        given_name=author_parts[1].strip(), family_name=author_parts[0].strip()
    )


def _save(papers: list[ArXivPaper], out: pathlib.Path) -> None:
    with open(out, "w") as f:
        fieldnames = [
            "id",
            "submitted",
            "updated",
            "authors_of_interest",
            "authors",
            "title",
            "abstract",
            "url",
        ]
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
        csv_writer.writeheader()
        for paper in papers:
            csv_writer.writerow(dataclasses.asdict(paper))


def main():
    typer.run(query)


if __name__ == "__main__":
    main()
