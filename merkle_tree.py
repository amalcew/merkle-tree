from aux import *


class Node:
    def __init__(self, value, name):
        self.left_parent = None
        self.right_parent = None
        self.name = name
        self.value = value
        self.hash_value = get_hash_value(value)


class MerkleTree:
    def __init__(self, arr):
        self.leaves = arr
        self.node_dict = dict()
        self.child_nodes_dict = dict()

        self.final_hash = None

    # def build_tree(self):
        k = 0
        nodes = []
        for leaf in self.leaves:
            node = Node(leaf, leaf)
            nodes.append(node)
            self.node_dict[node.name] = node.hash_value

        for i in range(len(nodes)):
            tmp_array = []
            for j in range(0, len(nodes), 2):
                k += 1
                parent1 = nodes[j]
                if j+1 < len(nodes):
                    parent2 = nodes[j+1]
                else:
                    tmp_array.append(parent1)
                    break

                concatenated_hash = parent1.hash_value + parent2.hash_value
                concatenated_name = parent1.name + "|" + parent2.name
                child_node = Node(concatenated_hash, concatenated_name)
                self.child_nodes_dict[child_node.name] = child_node.hash_value

                tmp_array.append(child_node)
            nodes = tmp_array
        self.final_hash = nodes[0].hash_value

    def get_final_hash(self):
        return self.final_hash

    def check_inclusion(self, elem):
        if len(elem) == 64 and int(elem, 16):
            if elem in self.node_dict.values():
                return True
            else:
                return False
        else:
            if elem in self.node_dict.keys():
                return True
            else:
                return False


def check_consistency(tree1, tree2):  # tree1 - subtree, tree2 - maintree
    # create temporary trees and swap trees, if first given tree is not the smallest
    if len(tree1.leaves) > len(tree2.leaves):
        tree, subtree = tree1, tree2
    else:
        subtree, tree = tree1, tree2

    # check if tree1 is subset of tree2
    for i in range(len(subtree.leaves)):
        if subtree.leaves[i] is not tree.leaves[i]:
            return False

    tree_childs = tree.child_nodes_dict
    tree_left_parents = extract_parents(tree.node_dict, 0)
    tree_right_parents = extract_parents(tree.node_dict, 1)

    # TODO: write consistency proof function, because it would be MUCH easier than revere engineering droid76's solution
