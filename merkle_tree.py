from hashlib import sha256
import treelib
from graphviz import Source
from os import remove
from datetime import datetime
from time import sleep


class Node:
    """ Stores crucial data of the parent node, children nodes, name and values """
    def __init__(self, _left_child, _right_child, _name, _value):
        self.parent = None
        self.left_child = _left_child
        self.right_child = _right_child
        self.name = _name
        self.value = _value
        self.hash_value = sha256(self.value.encode('utf-8')).hexdigest()


class MerkleTree:
    """ Tree structure storing leaves, branches and root hashes """
    def __init__(self, lst):
        self.nodes = list()
        tmp = list()
        for elem in lst:
            node = Node(None, None, elem, elem)
            self.nodes.insert(-len(self.nodes), node)  # inserts node at the beginning to maintain proper indexing
            tmp.append(node)  # temporary list used in build_tree() function
        self.structure = self.build_tree(tmp)

    def create_parent(self, left_child, right_child):
        """ Creates the parent node from given children and updates fields of children and parent """
        if right_child is not None:  # case 1: parent has two children
            concatenated_name = left_child.name + "|" + right_child.name
            concatenated_value = left_child.hash_value + right_child.hash_value
            parent = Node(left_child, right_child, concatenated_name, concatenated_value)  # create parent node
            left_child.parent, right_child.parent = parent, parent  # update children' parent field
        else:  # case 2: parent has one child
            concatenated_name = left_child.name
            concatenated_value = left_child.value
            parent = Node(None, None, concatenated_name, concatenated_value)  # create parent node
            left_child.parent = parent  # update child's parent field

        flag = False
        for elem in self.nodes:  # loop checking the occurrence of parent on the nodes list
            if elem.name == parent.name:
                # check if parent isn't already on the list. If it is, remove it and append a new one
                self.nodes.remove(elem)
                self.nodes.insert(0, parent)
                flag = True

        if not flag:  # if no duplicates were found, insert the parent node at the beginning of the list
            self.nodes.insert(0, parent)

        return parent

    def build_tree(self, lst):
        """ Recursive method generating tree structure from given list of leaves """
        if len(lst) == 1:
            return lst[0]

        parents = []
        for i in range(0, len(lst), 2):  # loop iterating through next levels of the tree
            left_child = lst[i]
            if i + 1 < len(lst):  # if there is two children, continue
                right_child = lst[i+1]
            else:  # if there is only one child, append it to parents list and break the loop
                parents.append(self.create_parent(left_child, None))
                break
            parents.append(self.create_parent(left_child, right_child))
        return self.build_tree(parents)

    def get_root_hash(self):
        """ Returns the root (final) hash """
        return self.structure.hash_value

    def check_inclusion(self, elem):
        """ Method searching for presence of passed parameter in the Merkle tree """
        if len(elem) == 64 and int(elem, 16):  # passed parameter is a hash
            for i in range(len(self.nodes)):
                if elem == self.nodes[i].hash_value:
                    return True
            return False
        else:  # passed parameter is a string
            for i in range(len(self.nodes)):
                if elem == self.nodes[i].name:
                    return True
            return False

    def show(self, engine='treelib', save=False):
        """ Method printing tree structure, using treelib library """
        tree = treelib.Tree()
        for node in self.nodes:
            if node.name == self.structure.name:
                tree.create_node(node.name, node.name)  # root node
            else:
                tree.create_node(node.name, node.name, parent=node.parent.name)  # branch/leaf node

        if engine == 'graphviz':  # use graphviz frontend to generate the visualization
            now = datetime.now().strftime("%Y%m%d%H%M%S")
            tree_name = "tree-%s" % now
            tree.to_graphviz(filename=tree_name, shape='record')
            source = Source.from_file(tree_name)
            source.view()
            sleep(0.3)
            if not save:
                remove(tree_name + ".pdf")
            remove(tree_name)
        else:  # use treelib frontend to generate the visualization
            tree.show()
            if save:
                now = datetime.now().strftime("%Y%m%d%H%M%S")
                tree.save2file("tree-%s" % now)