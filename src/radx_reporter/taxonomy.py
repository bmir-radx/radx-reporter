import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

from queue import Queue

class TaxonomyNode:
    
    def __init__(self, name, depth=0, parents=None, children=None):
        self.name = name
        self.depth = depth
        if parents is None:
            parents = {}
        self._parents = parents
        if children is None:
            children = {}
        self._children = children
        self._index_markers = set()

    def __hash__(self):
        return hash(self.name)

    def __lt__(self):
        return self.num_parents

    def add_markers(self, markers):
        self._index_markers.update(markers)

    def get_markers(self):
        return self._index_markers

    @property
    def count(self):
        return len(self._index_markers)

    def add_child(self, node):
        self._children[node.name] = node

    def add_parent(self, node):
        self._parents[node.name] = node
    
    def get_child(self, label):
        return self._children.get(label)

    def get_children(self):
        return self._children.values()

    def get_parent(self, label):
        return self._parents.get(label)

    def get_parents(self):
        return self._parents.values()

    @property
    def num_children(self):
        return len(self._children)

    @property
    def num_parents(self):
        return len(self._parents)

    @property
    def count_string(self):
        return f"{self.name}\nCount: {self.count}"

    @property
    def depth_string(self):
        return f"{self.name}\nDepth: {self.depth}"

    def __repr__(self):
        return f"Node(name={self.name})"

    def __str__(self):
        return f"Node(name={self.name}, count={self.count}, depth={self.depth}, " \
            + f"num_children={self.num_children}, num_parents={self.num_parents})"


class Taxonomy:
    def __init__(self, labels, edges, name="Made-up Taxonomy"):
        self.name = name
        self.labels = labels
        self.edges = edges

        self.root = TaxonomyNode("Total", -1)
        self.nodes = self.build_nodes(labels)
        self._graph = nx.DiGraph()
        self.connect_nodes(edges)
        self.mark_node_depths()

        # cache counts for subtrees that have already been processed
        self.count_cache = {}

    def build_nodes(self, labels):
        """Generate a dictionary of TaxonomyNode objects."""
        taxonomy_nodes = {label: TaxonomyNode(label) for label in labels}
        return taxonomy_nodes

    def connect_nodes(self, edges):
        """
        Connect TaxonomyNodes as specified by edges.
        Also generate a networkx graph for visualization.
        """
        for parent, child in edges:
            self.nodes[parent].add_child(self.nodes[child])
            self.nodes[child].add_parent(self.nodes[parent])
            self._graph.add_edge(parent, child)
        # find top-level nodes. these are nodes with no parents.
        top_level_nodes = [node for node in self.nodes.values() if node.num_parents == 0]
        # connect top-level nodes to the root sentinel
        for node in top_level_nodes:
            self.root.add_child(node)
            node.add_parent(self.root)
            self._graph.add_edge(self.root.name, node.name)

    def mark_node_depths(self):
        """
        Perform breadth-first search with some topological filtering such that nodes
        are only expanded after all of their parents have been discovered.
        This is valid for a DAG but breaks in a cyclical graph.
        """
        # counter for times edges have led into a node
        parents_processed = {}

        # frontier for expanding nodes
        frontier = Queue()
        for child in self.root.get_children():
            frontier.put(child)
            parents_processed[child] = 1

        # tracker for nodes already processed. these should not be processed again.
        processed = set()

        while frontier.qsize() > 0:
            for _ in range(frontier.qsize()):
                node = frontier.get()

                # skip a node that has already been processed
                # e.g., a child has three parents at the same depth
                # so it is valid to process the child the first time it comes up in queue
                if node in processed:
                    continue
                
                # skip a node if not all of its parents have been processed.
                # this will skip a node that is depth m by following one path but depth m+n by following another
                if parents_processed[node] != node.num_parents:
                    continue
                
                # set a node's depth as 1 deeper than its deepest parent
                node.depth = 1 + max([parent.depth for parent in node.get_parents()])

                # add children to frontier and increment number of parents processed for the child node
                for child in node.get_children():
                    frontier.put(child)
                    if child not in parents_processed:
                        parents_processed[child] = 1
                    else:
                        parents_processed[child] += 1

                # keep track of processed nodes
                processed.add(node)

    def add_markers(self, markers):
        """
        Given a dictionary of markers, assign markers to the appropriate
        nodes. Markers are the row indices of the data file that should
        count toward a specific node.
        Each node merges markers from its descendant. Markers are assigned
        to nodes in reverse depth order to avoid processing any node more
        than once.

        Args:
            markers (Dict[str, List[int]]): key is node labels. value is list of markers.
        """
        nodes_to_count = [self.nodes[name] for name in markers]
        nodes_by_depth = sorted(nodes_to_count, key=lambda node: node.depth, reverse=True)

        for node in nodes_by_depth:
            self.add_markers_to_node(node, markers[node.name])

    def add_markers_to_node(self, node, markers):
        """
        Naive approach to incrementing counts. Check all descendants
        for any markers and form the union with the provided set of
        markers.
        """
        node.add_markers(markers)
        node.add_markers(self.propagate_markers_recursively(node))

    def propagate_markers_recursively(self, node):
        """
        For a node, merge markers from its descendants.
        Assumes graph has no cycles.
        """
        # if subtree has already been processed, return the
        # deduplicated markers. no need to traverse the subtree
        # this cache makes it so that we need a one-shot allocation of
        # counts. if this is not the case, we need to traverse the
        # tree multiple times (or just once for every time the tree is reported)
        if node.name in self.count_cache:
            return node.get_markers()

        deduplicated_markers = set()
        for child in node.get_children():
            deduplicated_markers.update(self.propagate_markers_recursively(child))
        
        # store deduplication result for subtree
        node.add_markers(deduplicated_markers)
        # cache count
        self.count_cache[node.name] = node.count
        return node.get_markers()

    def get_counts(self, term):
        """
        Count markers over the whole subtree. If the count
        has not already been cached, it will be computed by
        merging markers from its descendants.
        """
        if not term in self.count_cache:
            # do a count over the subtree
            self.add_markers(term, set())
        return self.count_cache[term]

    def get_term(self, term):
        return self.nodes[term]

    def visualize_taxonomy(self, root=None):
        if root is None:
            graph = self._graph
        else:
            descendants = nx.descendants(self._graph, root)
            descendants.add(root)
            graph = self._graph.subgraph(descendants)
        plt.figure(figsize=(14, 6))
        pos = nx.drawing.nx_agraph.graphviz_layout(graph, prog="dot")
        nx.draw(graph, pos, with_labels=True, node_size=2000, node_color="thistle", font_size=10, font_weight="bold")
        plt.title(self.name)
        plt.show()

    def _add_counts_for_visualization(self, graph, node):
        for child in node.get_children():
            graph.add_edge(node.count_string, child.count_string)
            self._add_counts_for_visualization(graph, child)

    def aggregate_counts(self):
        # populate entire taxonomy with counts by processing ROOT node
        self.add_markers_to_node(self.root, set())

    def visualize_counts(self):
        # clear cache to ensure counts are accurate
        self.count_cache = {}
        self.aggregate_counts()
        graph = nx.DiGraph()
        self._add_counts_for_visualization(graph, self.root)
        plt.figure(figsize=(10,6))
        pos = nx.drawing.nx_agraph.graphviz_layout(graph, prog="dot")
        nx.draw(graph, pos, with_labels=True, node_size=3000, node_color="thistle", font_size=10, font_weight="bold")
        plt.title(self.name)
        plt.show()
        
    def _add_depth_for_visualization(self, graph, node):
        for child in node.get_children():
            graph.add_edge(node.depth_string, child.depth_string)
            self._add_depth_for_visualization(graph, child)

    def visualize_depth(self):
        graph = nx.DiGraph()
        self._add_depth_for_visualization(graph, self.root)
        plt.figure(figsize=(10,6))
        pos = nx.drawing.nx_agraph.graphviz_layout(graph, prog="dot")
        nx.draw(graph, pos, with_labels=True, node_size=3000, node_color="thistle", font_size=10, font_weight="bold")
        plt.title(self.name)
        plt.show()

    def flatten_counts(self):
        """
        Flatten the counts from a tree to a static dictionary that
        can be used for writing output (e.g., to a spreadsheet).
        """
        counts = {}
        frontier = Queue()
        frontier.put(self.root)
        processed = set()
        while frontier.qsize() > 0:
            node = frontier.get()
            if node in processed:
                continue
            counts[node.name] = node.count
            for child in node.get_children():
                frontier.put(child)
        return counts

    def to_csv(self, file_name: str = "counts.csv"):
        counts = self.flatten_counts()
        pairs = [(label, count) for label, count in counts.items()]
        counts = pd.DataFrame({
            "Label": [pair[0] for pair in pairs],
            "Count": [pair[1] for pair in pairs],
        })
        counts.to_csv(file_name, index=False)
