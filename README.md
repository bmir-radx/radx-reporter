# RADx Data Hub Content Reporter

The RADx Data Hub Content reporter is a Python package used to aggregate counting statistics on the contents of the RADx Data Hub. At the basic level, the reporter tool dumps a report in JSON format that counts the number of studies belonging to controlled terms in several categories, including the RADx Program (DCC) and Study Domain.

## Requirements

- Python >= 3.10

## Running the reporter

Running the reporter requires installing it as a python package. In the same directory as this README (perhaps in a virtual environment), run:

```
pip install .
```

Once installed, the program can be executed using the `radx-study-metadata-reporter` command. It expects arguments for the input file to parse and the name of the output file to save:

```
radx-study-metadata-reporter -i input.xlsx -o report.json
```
