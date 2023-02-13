from merkle_tree import MerkleTree
from tests.inclusion_proof import check_inclusion
from tests.consistency_proof import check_consistency


def main():
    arr = ['alice', 'bob', 'carol', 'david', 'eve', 'fred', 'george', 'hans', 'isabel', 'jeff', 'klaus', 'leon', 'mark',
           'noel']
    tree = MerkleTree(arr)
    correct_subtree = MerkleTree(arr[:4])
    incorrect_subtree = MerkleTree(arr[1:5])
    existing_element = 'fred'
    nonexisting_element = 'daniel'
    print("Root hash: %s\n" % (tree.get_root_hash()))
    print("Inclusion proof of element existing in the tree: %s" % (check_inclusion(tree, existing_element)))
    print("Inclusion proof of element nonexisting in the tree: %s" % (check_inclusion(tree, nonexisting_element)))
    print("Consistency proof of correct prevoius tree: %s" % (check_consistency(correct_subtree, tree)))
    print("Consistency proof of incorrect prevoius tree: %s" % (check_consistency(incorrect_subtree, tree)))


if __name__ == '__main__':
    main()
