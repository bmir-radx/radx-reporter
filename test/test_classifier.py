import pytest

from radx_reporter.studies import classifier, study, vocabulary


class TestClassifier:

    @pytest.fixture
    def example_studies(self):
        study1 = study.Study(
            None,
            None,
            vocabulary.Program.RAD,
            "phs_1",
            [
                vocabulary.StudyDesign.CASECONTROL,
                vocabulary.StudyDesign.CLINICALGENETICTESTING,
            ],
            [vocabulary.DataType.BEHAVIORAL, vocabulary.DataType.CLINICAL],
            [
                vocabulary.CollectionMethod.CONTACTTRACING,
                vocabulary.CollectionMethod.INTERVIEW,
            ],
            [vocabulary.NihInstitute.NCATS, vocabulary.NihInstitute.NCCIH],
            [vocabulary.StudyDomain.AGING, vocabulary.StudyDomain.AIML],
            100,
            vocabulary.PopulationRange.SMALLEST,
            None,
            None,
            None,
        )
        study2 = study.Study(
            None,
            None,
            vocabulary.Program.RAD,
            "phs_2",
            [vocabulary.StudyDesign.CASECONTROL, vocabulary.StudyDesign.CLINICALTRIAL],
            [vocabulary.DataType.BEHAVIORAL, vocabulary.DataType.COGNITIVE],
            [
                vocabulary.CollectionMethod.CONTACTTRACING,
                vocabulary.CollectionMethod.QUESTIONNAIRE,
            ],
            [vocabulary.NihInstitute.NCATS, vocabulary.NihInstitute.NCI],
            [vocabulary.StudyDomain.AGING, vocabulary.StudyDomain.ANTIGEN],
            10,
            vocabulary.PopulationRange.SMALLEST,
            None,
            None,
            None,
        )
        studies = {"phs_1": study1, "phs_2": study2}
        return studies

    def equivalent_contents(self, list1, list2):
        set1 = frozenset(frozenset(l1) for l1 in list1)
        set2 = frozenset(frozenset(l2) for l2 in list2)
        return set1 == set2

    def test_label_studies(self, example_studies):
        study_labels = classifier.label_studies(example_studies)
        assert study_labels["phs"].to_list() == ["phs_1", "phs_2"]
        assert study_labels["Program"].to_list() == [
            vocabulary.Program.RAD.label,
            vocabulary.Program.RAD.label,
        ]

    def test_classify_studies(self, example_studies):
        studies_by_classifier = classifier.classify_studies(example_studies)
        assert studies_by_classifier[vocabulary.Classifier.PROGRAM][
            vocabulary.Program.RAD
        ] == [example_studies["phs_1"], example_studies["phs_2"]]

    def test_aggregate_counts_to_dataframe(self, example_studies):
        pass
