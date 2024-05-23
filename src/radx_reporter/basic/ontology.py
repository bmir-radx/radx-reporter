from queue import Queue

import pandas as pd


class Node:

    def __init__(self, name, label=None, alt_labels=None, is_auxiliary_term=False):
        self.name = name
        self.label = label
        self.alt_labels = alt_labels
        self.coded = not is_auxiliary_term
        self.parents = set()
        self.children = set()
        self.values = {}

    def __repr__(self):
        return f"Node(name={self.name}, label={self.label})"

    def __hash__(self):
        return hash(self.label)

    def add_parent(self, parent: "Node"):
        self.parents.add(parent)

    def add_child(self, child: "Node"):
        self.children.add(child)

    @property
    def url(self):
        """This is a hack to make count aggregation work for now."""
        return None



class Ontology:

    def __init__(
        self,
        labels_tsv,
        auxiliary_terms_csv,
        alt_labels_tsv,
        hierarchy_tsv,
        start="owl:Thing",
    ):
        labels = pd.read_csv(labels_tsv, sep="\t")
        alt_labels = pd.read_csv(alt_labels_tsv, sep="\t")
        hierarchy = pd.read_csv(hierarchy_tsv, sep="\t")
        auxiliary_terms = pd.read_csv(auxiliary_terms_csv, sep="\t")
        self.labels = self.parse_labels(labels)
        self.auxiliary_terms = self.parse_auxiliary_terms(auxiliary_terms)
        self.alt_labels = self.parse_alt_labels(alt_labels)
        self.graph = self.convert_hierarchy_to_graph(hierarchy)
        self.element_nodes = self.build_ontology(
            start, self.labels, self.auxiliary_terms, self.alt_labels, self.graph
        )
        self.label_to_node = {node.label: node for node in self.element_nodes.values()}
        self.root = self.element_nodes[start]
        self.top_level_nodes = {self.root}.union(self.root.children)

    def parse_labels(self, labels):
        node_labels = {}
        for i, row in labels.iterrows():
            node_labels[row["subject"]] = row["object"]
        return node_labels

    def parse_auxiliary_terms(self, auxiliary_terms_df):
        auxiliary_terms = set()
        for _, row in auxiliary_terms_df.iterrows():
            auxiliary_terms.add(row["subject"])
        return auxiliary_terms

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

    def make_node(self, node_name, node_labels, auxiliary_terms, alt_labels):
        if node_name in node_labels:
            node_label = node_labels[node_name]
        else:
            node_label = None
        if node_name in alt_labels:
            alt = alt_labels[node_name]
        else:
            alt = set()
        is_aux = node_name in auxiliary_terms
        return Node(node_name, node_label, alt, is_auxiliary_term=is_aux)

    def build_ontology(
        self, start_name: str, node_labels, auxiliary_terms, alt_labels, graph
    ):
        """
        This builds the graph for DataElement entries in the RADx Ontology.
        DataElements are connected to child DataElements through the isSubclass
        predicate, which serves as a directed edge here. Children are also linked
        to their parents if possible.
        Element nodes are built for the subgraph starting start_name.
        Assign label and altLabel to each node and connect parents to children.
        """
        element_nodes = {}
        start_node = self.make_node(
            start_name, node_labels, auxiliary_terms, alt_labels
        )
        element_nodes[start_name] = start_node
        frontier = Queue()
        frontier.put(start_node)
        visited = set()
        while frontier.qsize() > 0:
            node = frontier.get()
            if node.name in graph:
                for child_name in graph[node.name]:
                    if child_name in element_nodes:
                        child_node = element_nodes[child_name]
                    else:
                        child_node = self.make_node(
                            child_name, node_labels, auxiliary_terms, alt_labels
                        )
                        element_nodes[child_name] = child_node
                    child_node.add_parent(node)
                    node.add_child(child_node)
                    if not child_name in visited:
                        frontier.put(child_node)
                        visited.add(child_name)
        return element_nodes

    def find_ancestors(self, labels):
        frontier = Queue()
        visited = set()
        for label in labels:
            if label in self.label_to_node:
                node = self.label_to_node[label]
                frontier.put(node)
                visited.add(node)
        parents = set()
        while frontier.qsize() > 0:
            node = frontier.get()
            for parent in node.parents:
                if not parent in visited:
                    visited.add(parent)
                    parents.add(parent)
                    frontier.put(parent)
        # prune top-level nodes
        ancestors = []
        for parent in parents:
            if parent in self.top_level_nodes:
                continue
            ancestors.append(parent)
        return ancestors
