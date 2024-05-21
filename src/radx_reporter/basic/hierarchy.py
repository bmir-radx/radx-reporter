from . import vocabulary

focus_population_hierarchy = {
    "African American": {},
    "Native Hawaiian or other Pacific Islander": {},
    "Hispanic and Latino": {},
    "Asian": {},
    "Immigrants": {},
    "Racial and Ethnic Minorities": {},
    "Children": {},
    "Other Adults or Elderly": {},
    "Adults": {},
    "People Living with HIV/AIDs": {},
    "Dialysis Patients": {},
    "Pregnant (or Nursing) Women": {},
    "Intellectual and Developmental Disabilities": {},
    # "Socioeconomic Status and Vulnerable Populations": {
    "Lower Socioeconomic Status (SES) Population": {},
    "Homeless/Unhoused": {},
    "Incarcerated/Institutionalized (or Criminal Legal System Involvement)": {},
    "Rural Communities": {},
    "Underserved/Vulnerable Population": {},
    "School Community Members": {},
    "Essential Workers": {},
    "Sexual and Gender Minorities": {},
    "UNKNOWN OR INVALID": {},
}

study_domain_hierarchy = {
    # "Testing and Surveillance": {
    "Testing Rate/Uptake": {},
    "Antigen Testing": {},
    "Diagnostic Testing": {},
    "Point-of-Care (POC) Testing": {},
    "Screening Testing": {},
    "Virological Testing": {},
    "Rapid Diagnostic Testing": {},
    "Laboratory (PCR) Testing": {},
    "Serological (Antibody) Testing": {},
    "Mobile Unit Testing": {},
    "At-Home Testing": {},
    # "Epidemiology and Monitoring": {
    "COVID in School Settings": {},
    "COVID Hotspots": {},
    "COVID Testing Deserts": {},
    "Wastewater Surveillance": {},
    "Disease Surveillance": {},
    "Multimodal Surveillance": {},
    # "Variants and Immunity": {
    "Variants": {},
    "Immune Responses": {},
    "Seroprevalence": {},
    # "Pandemic Impact and Response": {
    "Pandemic Perceptions and Decision-Making": {},
    "Vaccination Rate/Uptake": {},
    # "Medical Conditions": {
    "Long COVID": {},
    "Comorbidities": {},
    "Multisystem Inflammatory Syndrome in Children (MIS-C)": {},
    "Multisystem Inflammatory Syndrome (MIS)": {},
    "Cancer": {},
    "Diabetes": {},
    "Obesity": {},
    "Infectious Diseases": { # 10
        "Influenza": {}, # 6
        "COVID": {}, # 4
    },
    "Aging": {},
    "Nutrition": {},
    "Mental Health": {},
    "Substance Use": {},
    # "Technology and Innovation": {
    "Medical Device Development": {},
    "Biosensor Technology": {},
    "Novel Biosensing and VOC": {},
    "Chemosensory Testing": {},
    "Artifical Intelligence and Machine Learning": {},
    "Next Generation Sequencing (NGS)": {},
    "Digital Health Applications": {},
    # "Social Factors and Public Health": {
    "Health Behaviors": {},
    "Social Determinants of Health": {},
    "Community Outreach Programs": {},
    "Children": {},
    "Minorities": {},
    "UNKNOWN OR INVALID": {},
}

collection_method_hierarchy = {
    "Technology": {
        "Wearable": {},
        "Smartphone": {},
    },
    "Survey": {},
    "Interview or Focus Group": {},
    # "Diagnostic Devices": {
    #     "COVID-19 Testing Devices": {
    "Antigen Testing Device": {},
    "Molecular (Nucleic Acid/PCR) Testing Device": {},
    "Antibody Testing / Other Adaptive Immune Response Test": {},
    "Unspecified COVID Testing Device": {},
    "Breath Analysis Device / Airborne Detection Device": {},
    "Chemosensory Testing Device": {},
    "Electrochemical Testing Device": {},
    "Contact Tracing": {},
    "Wastewater Sampling": {},
    "Disease Registry": {},
    "Biobank Samples": {},
    "Real-World Data": {},
    "Other": {},
    "UNKNOWN OR INVALID": {},
}

data_type_hierarchy = {
    # "Clinical and Medical Data": {
    "Clinical": {},
    "Electronic Medical Records": {},
    "Immulogical": {},
    # "Genetic and Molecular Data": {
    "Family History": {},
    "Genomic": {},
    "Genotyping": {},
    "Individual Genotype": {},
    "Individual Phenotype": {},
    "Individual Sequencing": {},
    "Metabolomic": {},
    "Proteomic": {},
    # "Behavioral and Psychological Data": {
    "Behavioral": {},
    "Cognitive": {},
    "Psychological": {},
    # "Lifestyle Data": {
    "Physical Activity": {},
    "Social": {},
    # "Imaging Data": {
    "Imaging": {},
    "Enviornmental (Physical)": {},
    "Questionnaires/Surveys": {},
    "Supporting Documents": {},
    "Other": {},
    "UNKNOWN OR INVALID": {},
}

study_design_hierarchy = {
    # "Observational Studies": {
    "Observational": {
        "Case-Control": {},
        "Cross-Sectional": {},
        "Longitudinal Cohort": {},
        "Open Cohort": {},
    },
    "Interventional/Clinical Trial": {},
    "Device Validation Study": {},
    # "Genetic Studies": {
    "Clinical Genetic Testing": {},
    "Family/Twins/Trios": {},
    "Mendelian": {},
    "Metagenomics": {},
    "Xenograft": {},
    # "Research Methodology": {
    "Mixed Methods": {},
    "Qualitative": {},
    "Time-Series": {},
    "Other": {},
    "UNKNOWN OR INVALID": {},
}


class VocabularyNode:
    def __init__(
        self, label, coded=False, synonyms=None, url=None, parent=None, children=None
    ):
        self.label = label
        self.coded = coded
        self.url = url
        self.parent = parent

        if synonyms is None:
            self.synonyms = []
        else:
            self.synonyms = synonyms
        if children is None:
            self.children = []
        else:
            self.children = children

    def __hash__(self):
        return hash(self.label)

    def __repr__(self):
        return f"VocabularyNode(label={self.label}, coded={self.coded}, synonyms={self.synonyms})"


def connect_nodes(graph, nodes):
    for key, children in graph.items():
        # make node if necessary
        if not key in nodes:
            nodes[key] = VocabularyNode(label=key, coded=False)
        for child in children:
            if not child in nodes:
                nodes[child] = VocabularyNode(label=child, coded=False)
            child_node = nodes[child]
            child_node.parent = nodes[key]
            nodes[key].children.append(child_node)
            connect_nodes(children, nodes)


def setup_hierarchy(terms, taxonomy):
    nodes = {}
    for term in terms:
        nodes[term.label] = VocabularyNode(label=term.label, url=term.url, coded=True)

    connect_nodes(taxonomy, nodes)
    return nodes


FOCUS_POPULATION_HIERARCHY = setup_hierarchy(
    vocabulary.FOCUS_POPULATIONS, focus_population_hierarchy
)
STUDY_DOMAIN_HIERARCHY = setup_hierarchy(
    vocabulary.STUDY_DOMAINS, study_domain_hierarchy
)
COLLECTION_METHOD_HIERARCHY = setup_hierarchy(
    vocabulary.COLLECTION_METHODS, collection_method_hierarchy
)
DATA_TYPE_HIERARCHY = setup_hierarchy(vocabulary.DATA_TYPES, data_type_hierarchy)
STUDY_DESIGN_HIERARCHY = setup_hierarchy(
    vocabulary.STUDY_DESIGNS, study_design_hierarchy
)
