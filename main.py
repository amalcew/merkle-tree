import hashlib
import sys


class MerkleTreeNode:
    def __init__(self, value, name):
        self.left_parent = None
        self.right_parent = None
        self.name = name
        self.value = value
        self.hash_value = hashlib.sha256(value.encode('utf-8')).hexdigest()


def build_tree(leaves):
    nodes = []
    global included
    included = {}
    k = 0
    for leaf in leaves:
        node = MerkleTreeNode(leaf, leaf)
        nodes.append(node)
        included[node.name] = node.hash_value

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
            # print("%s : %s" % (parent1.name, parent1.hash_value))
            # print("%s : %s" % (parent2.name, parent2.hash_value))

            concatenated_hash = parent1.hash_value + parent2.hash_value
            concatenated_name = parent1.name + "|" + parent2.name
            child_node = MerkleTreeNode(concatenated_hash, concatenated_name)

            # print("\tconcatenation of %s and %s : %s | hash : %s\n" % (parent1.name, parent2.name, concatenated_hash, child_node.hash_value))

            tmp_array.append(child_node)
        nodes = tmp_array
    return nodes[0].hash_value


def check_inclusion(elem):
    if len(elem) == 64 and int(elem, 16):
        if elem in included.values():
            return True
        else:
            return False
    else:
        if elem in included.keys():
            return True
        else:
            return False


def check_consistency(leaves1, leaves2):
    # swap trees, if first given tree is not the smallest
    if len(leaves1) > len(leaves2):
        leaves1, leaves2 = leaves2, leaves1

    # check if tree1 is subset of tree2
    for i in range(len(leaves1)):
        if leaves1[i] is not leaves2[i]:
            return False

    # create trees
    tree1 = build_tree(leaves1)
    tree1_dict = included
    tree2 = build_tree(leaves2)
    tree2_dict = included



def main():
    arr = ['alice', 'bob', 'carol', 'david', 'eve']
    arr2 = ['alice', 'bob', 'carol', 'david']
    """ Above array creates this tree:
        alice   bob     carol   david
            \   /           \   /
          alice|bob       carol|david
               \              /
                 \           /
             alice|bob|carol|david         eve
                       \                   /
                         \                /
                       alice|bob|carol|david|eve
    """
    """print("Hash of %s: %s" % (arr, build_tree(arr)))

    test_1 = 'brian'
    test_1_hash = hashlib.sha256(test_1.encode('utf-8')).hexdigest()  # returns : f3fe5a51a2be8c6dc715028858fcba82ee021be7687e4f95b45086b8ffb1a23f

    test_2 = 'alice'
    test_2_hash = hashlib.sha256(test_2.encode('utf-8')).hexdigest()  # returns : 2bd806c97f0e00af1a1fc3328fa763a9269723c8db8fac4f93af71db186d6e90

    print("\n\nInclusion test no.1\n\t- name : %s : %s" % (test_1, check_inclusion(test_1)))  # returns : False
    print("\t- hash : %s : %s" % (test_1_hash, check_inclusion(test_1_hash)))  # returns : False
    print("\nInclusion test no.2\n\t- name : %s : %s" % (test_2, check_inclusion(test_2)))  # returns : True
    print("\t- hash : %s : %s" % (test_2_hash, check_inclusion(test_2_hash)))  # returns : True

    # TODO: add argument parser to the main.py when all functions are completed
    """

    check_consistency(arr, arr2)

if __name__ == '__main__':
    main()
