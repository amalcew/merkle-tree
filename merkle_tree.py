from hashlib import sha256


class Node:
    def __init__(self, _left_child, _right_child, _name, _value):
        self.parent = None
        self.left_child = _left_child
        self.right_child = _right_child
        self.name = _name
        self.value = _value
        self.hash_value = sha256(self.value.encode('utf-8')).hexdigest()


class MerkleTree:
    def __init__(self, lst):
        self.nodes = list()
        tmp = list()
        for elem in lst:
            node = Node(None, None, elem, elem)
            self.nodes.insert(-len(self.nodes), node)
            tmp.append(node)
        self.structure = self.build_tree(tmp)

    def create_parent(self, left_child, right_child):
        if right_child is not None:
            concatenated_name = left_child.name + "|" + right_child.name
            concatenated_value = left_child.hash_value + right_child.hash_value
            parent = Node(left_child, right_child, concatenated_name, concatenated_value)
            left_child.parent, right_child.parent = parent, parent
        else:
            concatenated_name = left_child.name
            concatenated_value = left_child.value
            parent = Node(None, None, concatenated_name, concatenated_value)
            left_child.parent = parent

        flag = False
        for elem in self.nodes:
            if elem.name == parent.name:
                self.nodes.remove(elem)
                self.nodes.insert(0, parent)
                flag = True
        if not flag:
            self.nodes.insert(0, parent)

        return parent

    def build_tree(self, lst):
        if len(lst) == 1:
            return lst[0]
        parents = []
        for i in range(0, len(lst), 2):
            left_child = lst[i]
            if i + 1 < len(lst):
                right_child = lst[i+1]
            else:
                parents.append(self.create_parent(left_child, None))
                break
            parents.append(self.create_parent(left_child, right_child))
        return self.build_tree(parents)

    def get_root_hash(self):
        return self.structure.hash_value
