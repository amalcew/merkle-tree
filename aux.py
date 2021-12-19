from hashlib import sha256


def extract_parents(dic, mode):
    """ Return dictionary of left or right parents depending on mode.\n
    Mode 0 returns left parents, mode 1 returns right parents """
    tmp_dic = dict()
    k = 0
    if mode == 0 or mode == 1:
        for key, value in dic.items():
            if k % 2 == mode:
                tmp_dic[key] = value
            k += 1
        return tmp_dic
    else:
        raise ValueError("Incorrect mode parameter given")


def get_hash_value(string):
    return sha256(string.encode('utf-8')).hexdigest()
