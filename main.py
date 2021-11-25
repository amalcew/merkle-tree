import hashlib
import sys


class MerkleTreeNode:
    def __init__(self, value):
        self.left_parent = None
        self.right_parent = None
        # self.name = None
        self.value = value
        self.hash_value = hashlib.sha256(value.encode('utf-8')).hexdigest()


def build_tree(leaves):
    nodes = []
    for leaf in leaves:
        nodes.append(MerkleTreeNode(leaf))

    for i in range(len(nodes)):
        tmp_array = []
        for j in range(0, len(nodes), 2):
            parent1 = nodes[j]
            if j+1 < len(nodes):
                parent2 = nodes[j+1]
            else:
                tmp_array.append(parent1)
                break

            concatenated_hash = parent1.hash_value + parent2.hash_value
            child_node = MerkleTreeNode(concatenated_hash)

            # TODO: add printing the concatenated parents hash and saving them into the data structure.
            #  it is necessary if we want to display the full process of the algorithm

            tmp_array.append(child_node)
        nodes = tmp_array
    return nodes[0].hash_value


def main():
    arr = ['alice', 'bob', 'carol', 'david', 'eve']
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
    print("Hash of %s: %s" % (arr, build_tree(arr)))

    # TODO: add argument parser to the main.py when all functions are completed


if __name__ == '__main__':
    main()
