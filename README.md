# arxiv-papers

Query the [arxiv](https://arxiv.org) for a list of papers.

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
