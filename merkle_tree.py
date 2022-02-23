import treelib
import json
import os
import platform
from hashlib import sha256
from graphviz import Source
from os import remove
from datetime import datetime
from time import sleep

now = datetime.now().strftime("%Y%m%d%H%M%S")


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
        self.nodes_dict = dict()
        self.nodes_list = list()
        self.leaves_list = list()

        nodes = list()  # temporary list used in build_tree() function
        for elem in lst:
            node = Node(None, None, elem, elem)
            nodes.append(node)
            self.leaves_list.append(node.name)
        self.structure = self._build_tree(nodes)
        self._generate_data_structures()  # generate nodes_dict and nodes_list

    @staticmethod
    def _create_parent(_left_child, _right_child):
        """ Creates the parent node from given children and updates fields of children and parent """

        if _right_child is not None:  # case 1: parent has two children
            concatenated_name = _left_child.name + "|" + _right_child.name
            concatenated_value = _left_child.hash_value + _right_child.hash_value
            parent = Node(_left_child, _right_child, concatenated_name,
                          concatenated_value)  # create parent node
            _left_child.parent, _right_child.parent = parent, parent  # update children' parent field
        else:  # case 2: parent has one child
            concatenated_name = _left_child.name
            concatenated_value = _left_child.value
            parent = Node(None, None, concatenated_name, concatenated_value)  # create parent node
            _left_child.parent = parent  # update child's parent field
            if _left_child.left_child:
                # verify if parent node have children
                # (correct inappropriate parent-children bound in specific cases of trees)
                parent.left_child = _left_child.left_child
                parent.right_child = _left_child.right_child

        return parent

    def _build_tree(self, _lst):
        """ Recursive method generating tree structure from given list of leaves """

        if len(_lst) == 1:
            return _lst[0]

        parents = []
        for i in range(0, len(_lst), 2):  # loop iterating through next levels of the tree
            left_child = _lst[i]
            if i + 1 < len(_lst):  # if there is two children, continue
                right_child = _lst[i + 1]
            else:  # if there is only one child, append it to parents list and break the loop
                parents.append(self._create_parent(left_child, None))
                break
            parents.append(self._create_parent(left_child, right_child))
        return self._build_tree(parents)

    def _generate_data_structures(self):
        """ Generates nodes dictionary with tree structure, used by json methods """

        # TODO: optimise the tree not to generate useless node dictionaries,
        #  which are later removed from the main dict

        def add(_node):
            """ Add node to the dictionary """

            # create nested dictionaries for node's children, if present
            tmp_left_child = self.nodes_dict[_node.left_child.name] if _node.left_child is not None else None
            tmp_right_child = self.nodes_dict[_node.right_child.name] if _node.right_child is not None else None
            # add node dictionary with children data
            self.nodes_dict[_node.name] = {'name': _node.name,
                                           'value': _node.value,
                                           'hash_value': _node.hash_value,
                                           'left_child': tmp_left_child,
                                           'right_child': tmp_right_child}
            if _node not in self.nodes_list:  # add the node to the list, which is used by show() method
                self.nodes_list.insert(0, _node)

        def generator(_node):
            """ Recursive method that add node parameters as dictionary to nodes dictionary """

            if _node.left_child:  # traverse through left subtree
                generator(_node.left_child)
            else:  # recursion base case
                add(_node)
                return

            if _node.right_child:  # traverse through right subtree
                generator(_node.right_child)
            else:  # recursion base case
                add(_node)
                return

            add(_node)

        generator(self.structure)  # generate the nodes_dict

        # overwrite the dictionary to store only root with its structure
        self.nodes_dict = self.nodes_dict[self.structure.name]

    def get_root_hash(self):
        """ Returns the root (final) hash """

        return self.structure.hash_value

    def check_inclusion(self, elem):
        """ Check if passed node is in the tree """

        # TODO: rewrite the function to use the dfs, not the loop
        for node in self.nodes_list:
            if elem == node.name or elem == node.hash_value:
                return True
        return False

    def check_consistency(self, subtree):
        """ Check if passed subtree is part of main tree"""

        # TODO: rewrite the function to generate consistency proof
        for i in range(len(subtree.leaves_list)):
            main_leaf = self.leaves_list[i]
            sub_leaf = subtree.leaves_list[i]
            if main_leaf != sub_leaf:
                return False
        return True

    def dump(self):
        """ Dumps the nodes dictionary to .json file """

        tree_name = "tree-%s.json" % now
        file = open(tree_name, "w")
        json.dump(self.nodes_, file, indent=6)  # dump to json
        file.close()

    def show(self, engine='treelib', save=False):
        """ Method printing tree structure, using treelib library """

        tree = treelib.Tree()
        for node in self.nodes_list:
            if node.name == self.structure.name:
                tree.create_node(node.name, node.name)  # root node
            else:
                tree.create_node(node.name, node.name, parent=node.parent.name)  # branch/leaf node

        if engine == 'graphviz':  # use graphviz frontend to generate the visualization
            tree_name = "tree-%s" % now
            tree.to_graphviz(filename=tree_name, shape='record')
            source = Source.from_file(tree_name)

            if platform in ['linux', 'linux2']:                      # linux
                if os.fork():  # parent process
                    os.wait()  # wait for child process to finish
                    if not save:
                        remove(tree_name + ".pdf")
                    remove(tree_name)
                else:  # child process
                    source.view()
                    sleep(1)
            else:                                                     # windows
                source.view()
                remove(tree_name)
        else:  # use treelib frontend to generate the visualization
            tree.show()
            if save:
                tree.save2file("tree-%s" % now)

    def dfs(self):
        def _dfs(struct):
            if struct.left_child is not None:
                _dfs(struct.left_child)

            if struct.parent is not None:
                print(struct.name)
            if struct.parent is None:
                print(struct.name)

            if struct.right_child is not None:
                _dfs(struct.right_child)

        _dfs(self.structure)
