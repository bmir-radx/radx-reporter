# Basic Reporter

## Required Input

The reporter aggregates statistics for categories `Program`, `NIH Institute`, `Collection Method`, `Study Design`, `Population Range`, `Data Type`, and `Study Domain` using controlled terms for each. These statistics are extracted from study metadata available in the RADx Data Hub. The CLI for the reporter takes an Excel spreadsheet as input. It performs the following steps in sequence:

1. Conversion of the target Excel spreadsheet to a Pandas Dataframe.
2. Mapping of studies to ontology terms that characterize them.
3. Aggregation of study counts over the ontology terms.
4. Generation of bar charts for visualization.

The reporter can also be used programmatically, in which case, step 1 can be skipped by providing a dataframe of the necessary data directly.

The Dataframe requires the following columns:

- STUDY STATUS
- STUDY PROGRAM
- NIH INSTITUTE OR CENTER
- DATA COLLECTION METHOD
- STUDY DESIGN
- ESTIMATED COHORT SIZE
- DATA TYPES
- STUDY DOMAIN
- STUDY PHS
- STUDY POPULATION FOCUS
- STUDY STATUS

## Output

There are two possible output formats for the basic report.

- Excel spreadsheet, in which each tab summarizes aggregation results over the controlled terms for each category, e.g., a tab for `Program`, in which each row has the study count and PHS IDs attributed to each DCC.
- JSON serialized (perhaps are more convenient format for use by another Data Hub component).

In the language of the Data Hub's search engine, each of the categories is a "name" and each controlled term for the category is a "facet." The search URL for studies that belong to a controlled term are automatically generated. It would be cool for search links to be published alongside the statistics for each controlled term.

Example: for the `Program` category and DCC `RADx-UP`, the search URL is https://radxdatahub.nih.gov/studyExplorer?&facets=%5B%7B%22name%22:%22dcc%22,%22facets%22:%5B%22RADx-rad%22%5D%7D%5D
