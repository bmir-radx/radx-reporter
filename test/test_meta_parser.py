import datetime

import pandas as pd
import pytest
import pytz

from radx_reporter.studies import meta_parser, study, vocabulary


class TestMetaParser:

    @pytest.fixture
    def example_dataframe(self):
        data = {
            "contribution": ["RADx-Tech", None],
            "data_general_types.1": ["Questionnaires/Surveys; Clinical", None],
            "description": [
                "There are two device studies under the 2183 banner. The 2183b study uses an enhanced visual display compared to the original study (2183a), so it has been renamed. These prospective clinical studies seek to examine the performance of the 2183 device (a and b), a lateral flow immunoassay for the point-of-care (POC) detection of SARS-CoV-2 nucleocapsid protein antigen, compared to the Roche 6800 Cobas PCR for SARS-CoV-2 assay. The goal of the 2183b study is for EUA approval for the device to be used among symptomatic persons by trained healthcare personnel collected mid-turbinate specimens. Note: no device performance data will be included in the data files.",
                None,
            ],
            "estimated_participants": [488, None],
            "institutes_supporting_study - CODED": ["NHLBI; NIBIB", None],
            "phs": ["phs002682", "failure"],
            "source - CODED": [
                "Questionnaire/Survey; Smartphone; COVID Testing Device",
                None,
            ],
            "studyenddate": ["2020-11-06 16:32:30+00", None],
            "studystartdate": ["2020-10-16 15:32:30+00", None],
            "subject": ["Aging", None],
            "types - CODED": ["Methods", None],
        }
        return pd.DataFrame(data)

    def test_parse_program(self, example_dataframe):
        program = meta_parser.parse_program(example_dataframe.loc[0])
        assert program == vocabulary.Program.TECH

    def test_parse_program_missing(self, example_dataframe):
        program = meta_parser.parse_program(example_dataframe.loc[1])
        assert program == vocabulary.Program.MISSING

    def test_parse_institute(self, example_dataframe):
        institutes = meta_parser.parse_nih_institutes(example_dataframe.loc[0])
        assert set(institutes) == {
            vocabulary.NihInstitute.NHLBI,
            vocabulary.NihInstitute.NIBIB,
        }

    def test_parse_institute_missing(self, example_dataframe):
        institutes = meta_parser.parse_nih_institutes(example_dataframe.loc[1])
        assert set(institutes) == {vocabulary.NihInstitute.MISSING}

    def test_parse_population(self, example_dataframe):
        population, population_range = meta_parser.parse_population(
            example_dataframe.loc[0]
        )
        assert population == 488
        assert population_range == vocabulary.PopulationRange.SMALLER

    def test_parse_population_unknown(self, example_dataframe):
        population, population_range = meta_parser.parse_population(
            example_dataframe.loc[1]
        )
        assert population is None
        assert population_range == vocabulary.PopulationRange.UNKNOWN

    def test_parse_data_types(self, example_dataframe):
        data_types = meta_parser.parse_data_types(example_dataframe.loc[0])
        assert set(data_types) == {
            vocabulary.DataType.QUESTIONNAIRE,
            vocabulary.DataType.CLINICAL,
        }

    def test_parse_data_types_missing(self, example_dataframe):
        data_types = meta_parser.parse_data_types(example_dataframe.loc[1])
        assert data_types == [vocabulary.DataType.MISSING]

    def test_parse_study_domains(self, example_dataframe):
        study_domains = meta_parser.parse_study_domains(example_dataframe.loc[0])
        assert set(study_domains) == {vocabulary.StudyDomain.AGING}

    def test_parse_study_domains_missing(self, example_dataframe):
        study_domains = meta_parser.parse_study_domains(example_dataframe.loc[1])
        assert set(study_domains) == {vocabulary.StudyDomain.MISSING}

    def test_parse_dates(self, example_dataframe):
        start_date, end_date = meta_parser.parse_dates(example_dataframe.loc[0])
        assert start_date == datetime.datetime(
            2020, 10, 16, 15, 32, 30, tzinfo=pytz.UTC
        )
        assert end_date == datetime.datetime(2020, 11, 6, 16, 32, 30, tzinfo=pytz.UTC)

    def test_parse_dates_missing(self, example_dataframe):
        start_date, end_date = meta_parser.parse_dates(example_dataframe.loc[1])
        assert start_date is None
        assert end_date is None

    def test_parse_phs(self, example_dataframe):
        phs = meta_parser.parse_phs(example_dataframe.loc[0])
        assert phs == "phs002682"

    def test_parse_metadata_dataframe(self, example_dataframe):
        pass
