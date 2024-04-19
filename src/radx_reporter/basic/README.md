# Basic Reporter

## Required Input

The reporter aggregates statistics for categories `Program`, `NIH Institute`, `Collection Method`, `Study Design`, `Population Range`, `Data Type`, and `Study Domain` using controlled terms for each. These statistics are extracted from study metadata available in the RADx Data Hub, currently available to us in the form of an Excel spreadsheet of the database export. The following columns of the spreadsheet are read and mapped to the above categories as follows:

- "contribution" -> Program
- "institutes_supporting_study - CODED" -> NIH Institute
- "source - CODED" -> Collection Method
- "types - CODED" -> Study Design
- "estimated_participants" -> Population Range
- "data_general_types.1" -> Data Type
- "subject" -> Study Domain
- "description" -> Study Domain
- "phs" (PHS ID as an identifier)
- "studystartdate" (additional info about the study)
- "studyenddate" (additional info about the study)

## Output

There are two possible output formats for the basic report.

- Excel spreadsheet, in which each tab summarizes aggregation results over the controlled terms for each category, e.g., a tab for `Program`, in which each row has the study count and PHS IDs attributed to each DCC.
- JSON serialized (perhaps are more convenient format for use by another Data Hub component).

In the language of the Data Hub's search engine, each of the categories is a "name" and each controlled term for the category is a "facet." The search URL for studies that belong to a controlled term are automatically generated. It would be cool for search links to be published alongside the statistics for each controlled term.

Example: for the `Program` category and DCC `RADx-UP`, the search URL is https://radxdatahub.nih.gov/studyExplorer?&facets=%5B%7B%22name%22:%22dcc%22,%22facets%22:%5B%22RADx-rad%22%5D%7D%5D

## Deficiencies

The basic reporting tool currently has room for improvement.

- reliance string matches to "CODED" columns in the database
  - as a result, the reporter fails to classify a large number of studies in the `Study Domain` category, which is probably the most interesting
- the "CODED" terms are not part of an ontology and are not automatically generated for studies
