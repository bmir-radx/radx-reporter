import pandas as pd
from queue import Queue
import re


class ValueNode:
    """
    Represents subclasses of DataElementValue in the RADx Ontology.
    DataElementValues do not have alt labels or children and they
    only belong to one parent (the corresponding DataElement) through
    the seeAlso predicate.
    """

    def __init__(self, name, label, code, value, parent=None):
        self.name = name
        self.label = label
        self.code = code
        self.value = value
        self.parent = parent

    def __repr__(self):
        components = [
            "ValueNode(",
            f"name={self.name},",
            f"label={self.label},",
            f"code={self.code},",
            f"value={self.value},",
            f"parent={self.parent.name}",
            ")",
        ]
        return "".join(components)

    def assign_parent(self, parent):
        self.parent = parent


class DataElementNode:
    """
    Represents subclasses of DataElement in the RADx Ontology.
    DataElements can have altLabels and can be connected to multiple
    parents through the isSubclassOf predicate.
    The DataElementNode may contain a set of ValueNodes if
    it is a data element with choice responses.
    The DataElementNode may have subclasses, which stored as children.
    """

    def __init__(self, name, label=None, alt_labels=None):
        self.name = name
        self.label = label
        self.alt_labels = alt_labels
        self.parents = set()
        self.children = set()
        self.values = {}

    def __repr__(self):
        return f"DataElementNode(name={self.name}, label={self.label})"

    def __hash__(self):
        return hash(self.label)

    def add_parent(self, parent: "DataElementNode"):
        self.parents.add(parent)

    def add_child(self, child: "DataElementNode"):
        self.children.add(child)

    def add_value(self, value_node: ValueNode):
        self.values[value_node.code] = value_node


class GCBO:
    def __init__(
        self, labels_tsv, alt_labels_tsv, hierarchy_tsv, see_also_tsv, start="owl:Thing"
    ):
        labels = pd.read_csv(labels_tsv, sep="\t")
        alt_labels = pd.read_csv(alt_labels_tsv, sep="\t")
        hierarchy = pd.read_csv(hierarchy_tsv, sep="\t")
        see_also = pd.read_csv(see_also_tsv, sep="\t")
        self.labels = self.parse_labels(labels)
        self.alt_labels = self.parse_alt_labels(alt_labels)
        self.graph = self.convert_hierarchy_to_graph(hierarchy)
        self.element_nodes = self.build_element_nodes(
            start, self.labels, self.alt_labels, self.graph
        )
        self.connect_elements_to_values(self.element_nodes, self.labels, see_also)
        self.root = self.element_nodes[start]

    def parse_labels(self, labels):
        node_labels = {}
        for i, row in labels.iterrows():
            node_labels[row["subject"]] = row["object"]
        return node_labels

    def parse_alt_labels(self, altLabels):
        alt_labels = {}
        for i, row in altLabels.iterrows():
            if not row["subject"] in alt_labels:
                alt_labels[row["subject"]] = set()
            alt_labels[row["subject"]].add(row["object"])
        return alt_labels

    def convert_hierarchy_to_graph(self, hierarchy):
        edges = []
        for i, row in hierarchy.iterrows():
            edges.append((row["object"], row["subject"]))

        graph = {}
        for start, end in edges:
            if not start in graph:
                graph[start] = set()
            graph[start].add(end)
        return graph

    def make_data_element_node(self, node_name, node_labels, alt_labels):
        if node_name in node_labels:
            node_label = node_labels[node_name]
        else:
            node_label = None
        if node_name in alt_labels:
            alt = alt_labels[node_name]
        else:
            alt = set()
        return DataElementNode(node_name, node_label, alt)

    def build_element_nodes(self, start_name: str, node_labels, alt_labels, graph):
        """
        This builds the graph for DataElement entries in the RADx Ontology.
        DataElements are connected to child DataElements through the isSubclass
        predicate, which serves as a directed edge here. Children are also linked
        to their parents if possible.
        Element nodes are built for the subgraph starting start_name.
        Assign label and altLabel to each node and connect parents to children.
        """
        element_nodes = {}
        start_node = self.make_data_element_node(start_name, node_labels, alt_labels)
        element_nodes[start_name] = start_node
        frontier = Queue()
        frontier.put(start_node)
        visited = set()
        while not frontier.qsize() == 0:
            node = frontier.get()
            if node.name in graph:
                for child_name in graph[node.name]:
                    if child_name in element_nodes:
                        child_node = element_nodes[child_name]
                    else:
                        child_node = self.make_data_element_node(
                            child_name, node_labels, alt_labels
                        )
                        element_nodes[child_name] = child_node
                    child_node.add_parent(node)
                    node.add_child(child_node)
                    if not child_name in visited:
                        frontier.put(child_node)
                        visited.add(child_name)
        return element_nodes

    def deconstruct_value_label(self, label):
        pattern = r", (\d+) \((.*?)\)"
        match = re.search(pattern, label)
        if match:
            code = int(match.group(1))
            value = match.group(2)
        else:
            code = None
            value = None
        return code, value

    def read_value_labels(self, element_nodes, node_labels, see_also_dataframe):
        """
        Create values and assign them to their appropriate elements.
        """
        values = {}
        for i, row in see_also_dataframe.iterrows():
            element_name = row["subject"]
            value_name = row["object"]
            # e.g., bmir-radx:nih_high_temp and bmir-radx:nih_high_temp_97
            if element_name in value_name:
                if not element_name in values:
                    values[element_name] = []
                value_label = node_labels[value_name]
                code, value = self.deconstruct_value_label(value_label)
                value_node = ValueNode(value_name, value_label, code, value)
                values[element_name].append(value_node)
        return values

    def connect_elements_to_values(self, element_nodes, node_labels, seeAlso):
        """
        Create ValueNodes and assign them to DataElementNodes.
        """
        for i, row in seeAlso.iterrows():
            element_name = row["subject"]
            value_name = row["object"]
            # e.g., bmir-radx:nih_high_temp and bmir-radx:nih_high_temp_97
            if element_name in value_name:
                element_node = element_nodes[element_name]
                value_label = node_labels[value_name]
                code, value = self.deconstruct_value_label(value_label)
                value_node = ValueNode(
                    value_name, value_label, code, value, element_node
                )
                element_node.add_value(value_node)
