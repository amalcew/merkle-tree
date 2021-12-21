from merkle_tree import MerkleTree
from hashlib import sha256


def inclusion_test(tree):
    test1 = 'brian'
    test1_hash = sha256(test1.encode('utf-8')).hexdigest()  # returns : f3fe5a51a2be8c6dc715028858fcba82ee021be7687e4f95b45086b8ffb1a23f

    test2 = 'alice'
    test2_hash = sha256(test2.encode('utf-8')).hexdigest()  # returns : 2bd806c97f0e00af1a1fc3328fa763a9269723c8db8fac4f93af71db186d6e90

    test3 = 'alice|bob'

    test4 = 'alice|carol'

    test5 = 'alice|bob|carol|david'

    test6 = 'alice|david|bob|carol'

    print("Inclusion test no.1\n\t- name : %s : %s" % (test2, tree.check_inclusion(test2)))     # returns : True
    print("\t- hash : %s : %s" % (test2_hash, tree.check_inclusion(test2_hash)))                # returns : True
    print("\nInclusion test no.2\n\t- name : %s : %s" % (test1, tree.check_inclusion(test1)))   # returns : False
    print("\t- hash : %s : %s" % (test1_hash, tree.check_inclusion(test1_hash)))                # returns : False
    print("\nInclusion test no.3\n\t- name : %s : %s" % (test3, tree.check_inclusion(test3)))   # returns : True
    print("\nInclusion test no.4\n\t- name : %s : %s" % (test4, tree.check_inclusion(test4)))   # returns : False
    print("\nInclusion test no.5\n\t- name : %s : %s" % (test5, tree.check_inclusion(test5)))   # returns : True
    print("\nInclusion test no.6\n\t- name : %s : %s" % (test6, tree.check_inclusion(test6)))   # returns : False


def main():
    arr = ['alice', 'bob', 'carol', 'david', 'eve', 'fred', 'george', 'hans', 'isabel', 'jeff', 'klaus', 'leon', 'mark',
           'noel']
    partial_arr = arr[:5]
    tree = MerkleTree(partial_arr)
    print("Root hash: %s\n" % (tree.get_root_hash()))
    # inclusion_test(tree)
    tree.show(engine='graphviz')

    # TODO: write appropriate inclusion and consistency check functions, comment the code and make tests


if __name__ == '__main__':
    main()
