import pytest

from taxonomy import Taxonomy

class TestTaxonomy:

    @pytest.fixture(scope="function")
    def setup_before_each_test(self):
        self.nodes = {"Puppets", "Muppets", "Television Shows", "Comedy Shows"}
        self.depths = {"Puppets": 0, "Muppets": 2, "Television Shows": 0, "Comedy Shows": 1}
        self.edges = [
            ["Puppets", "Muppets"], ["Television Shows", "Comedy Shows"], ["Comedy Shows", "Muppets"],
        ]
        self.markers = {
            "Muppets": {13, 14, 15},
            "Puppets": {13, 16},
        }
        self.counts = {
            "Muppets": 3, "Puppets": 4, "Television Shows": 3, "Comedy Shows": 3,
        }

    def test_nodes(self, setup_before_each_test):
        taxonomy = Taxonomy(self.nodes, self.edges, "Test")
        taxonomy_nodes = set(taxonomy.nodes.keys())
        assert taxonomy_nodes == self.nodes, "Taxonomy does not have the correct nodes."

    def test_edges(self, setup_before_each_test):
        taxonomy = Taxonomy(self.nodes, self.edges, "Test")
        for parent, child in self.edges:
            assert taxonomy.nodes[parent].get_child(child) is not None, f"Edge {parent}->{child} not present."

    def test_depth(self, setup_before_each_test):
        taxonomy = Taxonomy(self.nodes, self.edges, "Test")
        for label, node in taxonomy.nodes.items():
            assert node.depth == self.depths[label], f"Node {label} has depth {node.depth}. Expected: {self.depths[label]}."

    def test_counts(self, setup_before_each_test):
        taxonomy = Taxonomy(self.nodes, self.edges, "Test")
        taxonomy.add_markers(self.markers)
        taxonomy.aggregate_counts()
        for label, count in self.counts.items():
            assert taxonomy.nodes[label].count == count, f"{label} has count {taxonomy.nodes[label].count}. Expected: {count}"
