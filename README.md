# arxiv-papers

Query the [arxiv](https://arxiv.org) for a list of papers.

## Installation

Download or clone the code for this project and ensure that [uv](https://docs.astral.sh/uv/) is installed on your machine.

## Configuration

The arxiv catalogs and authors to query for must be configured in a [TOML](https://toml.io/en/) file `config.toml`, which must be located in the project root folder.

For each catalog `c` you have to define a table `[arxiv.c]` with a list of authors. Each author must be specified in the form family_name, given_name.

As an example, assume you want to query astro-ph for Jane Miller and John Doe, and q-bio for Peter Smith. Then your configuration file `config.toml` must have the following content:

```toml
[arxiv.astro-ph]
authors = [
    "Miller, Jane",
    "Doe, John"
]

[arxiv.q-bio]
authors = [
    "Smith, Peter"
]
```

An example configuration file (`config.example.toml`) is provided in the project root folder.

## Usage

To query the arXiv for papers, go to the project's root folder and execute this command in a terminal:

```bash
uv run arxiv
```

The command takes two required options:

Option | Description | Example value
--- | --- | ---
`--start` | Start date from which to query (inclusive), in the format `yyy-mm-dd` | `2025-04-13`
`--end` | End date until which to query (exclusive), in the format `yyyy-mm-dd` | `2025-05-03`

If you don't provide these options, you will be prompted for their value.

The start date is inclusive, the end date exclusive. This means that papers published on the start date are included in the query results, whereas papers published on the ebd date are not.

## Output

The `arxiv` command creates a CSV file with the following fields:

Field name | Description
--- | ---
id | Paper id.
submitted | The date and time of the first submission.
updated | The date and time of the latest submission.
authors_of_interest | The authors that are (potentially) of interest as their name matches oone of the queried persons for the category.
authors | The list of authors.
title | The title.
abstract | The abstract.
url | The URL of the arXiv page for the paper.

An "author of interest" is an author whose name contains one of the surnames which have been queried for the paper's arXiv category. For example, assume astro-ph was queried for John Doe and Jane Miller, and a paper contains the authors Alexandra Miller and John Smith. Then Alexandra Miller is considered an author of interest.

 Note that there may be papers with no author of interest if there are names with an umlaut. For example, if you query for Peter Muller and a paper has the author Dieter Müller, the paper will be returned by the query, but no author of interest will be indicated.

Both authors and authors of interest are separated with the pipe symbol (|).
