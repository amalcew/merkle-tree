from merkle_tree import MerkleTree, check_consistency
import hashlib


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
    tree = MerkleTree(arr)
    print("Final hash of %s: %s" % (tree.leaves, tree.get_final_hash()))

    print("\nLeaves dictionary:")
    for key, value in tree.node_dict.items():
        print("\t%s : %s" % (key, value))

    print("\nChildren dictionary:")
    for key, value in tree.child_nodes_dict.items():
        print("\t%s : %s" % (key, value))
    
    test_1 = 'brian'
    test_1_hash = hashlib.sha256(test_1.encode('utf-8')).hexdigest()  # returns : f3fe5a51a2be8c6dc715028858fcba82ee021be7687e4f95b45086b8ffb1a23f

    test_2 = 'alice'
    test_2_hash = hashlib.sha256(test_2.encode('utf-8')).hexdigest()  # returns : 2bd806c97f0e00af1a1fc3328fa763a9269723c8db8fac4f93af71db186d6e90
    
    print("\n\nInclusion test no.1\n\t- name : %s : %s" % (test_1, tree.check_inclusion(test_1)))  # returns : False
    print("\t- hash : %s : %s" % (test_1_hash, tree.check_inclusion(test_1_hash)))  # returns : False
    print("\nInclusion test no.2\n\t- name : %s : %s" % (test_2, tree.check_inclusion(test_2)))  # returns : True
    print("\t- hash : %s : %s" % (test_2_hash, tree.check_inclusion(test_2_hash)))  # returns : True

    # TODO: add argument parser to the main.py when all functions are completed


if __name__ == '__main__':
    main()
