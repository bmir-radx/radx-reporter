# RADx Data Hub Content Reporter

The RADx Data Hub Content reporter is a Python package used to aggregate counting statistics on the contents of the RADx Data Hub. At the basic level, the reporter tool dumps a report in JSON format that counts the number of studies belonging to controlled terms in several categories, including the RADx Program (DCC) and Study Domain. The reporter effectively performs map-reduce using ontology terms as keys.

## Requirements

- Python>=3.10
- pandas>=2.1.4
- numpy>=1.26,<2.0
- python-dateutile>=2.8.2

## Running the reporter

Running the reporter requires installing it as a python package.
Using conda, run the following in the same directory as this README:

```bash
conda create -n radxreporter python=3.10 -y
conda activate radxreporter
pip install -r requirements.txt
pip install .
```

### Command Line
Once installed, the program can be executed using the `radx-study-metadata-reporter` command. It expects arguments for the input file and sheet name of the XLSX spreadsheet to parse:

```bash
radx-study-metadata-reporter -i input.xlsx -s summary
```

### Library
Alternatively, the content reporter can be used programmatically by importing the module.

```python
from radx_reporter import reporter
import pandas as pd

# load a dataframe from file or provide one from a database query
dataframe = pd.read_excel("2024-07-24_RADx-DataHub-Metadata-Spreadsheet.xlsx", sheet_name="summary")

# provide the dataframe and an optimal report name
reporter.Reporter.basic_report(dataframe, report_name="report")
```

Additional fields are also supported for reporting.
```python
from radx_reporter import reporter
import pandas as pd

# load a dataframe from file or provide one from a database query
dataframe = pd.read_excel("2024-07-24_RADx-DataHub-Metadata-Spreadsheet.xlsx", sheet_name="summary")

# supply any extra columns to report on. the required columns (above)
# are assumed to be present
extra_columns = ["NIH GRANT NUMBER", "FOA NUMBER"]

# provide the dataframe and any extra columns
reporter.Reporter.basic_report(dataframe, extra_columns, report_name="report")
```

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

Additional columns are supported, but these contain coded terms that point directly to facets in the RADx Data Hub Study Explorer.

## Output

There are two possible output formats for the basic report.

- Excel spreadsheet, in which each tab summarizes aggregation results over the controlled terms for each category, e.g., a tab for `Program`, in which each row has the study count and PHS IDs attributed to each DCC.
- JSON serialized (perhaps are more convenient format for use by another Data Hub component).

In the language of the Data Hub's search engine, each of the categories is a "name" and each controlled term for the category is a "facet." The search URL for studies that belong to a controlled term are automatically generated. It would be cool for search links to be published alongside the statistics for each controlled term.

Example: for the `Program` category and DCC `RADx-UP`, the search URL is https://radxdatahub.nih.gov/studyExplorer?&facets=%5B%7B%22name%22:%22dcc%22,%22facets%22:%5B%22RADx-rad%22%5D%7D%5D
