class Node:
    def __init__(self, data=None, children=None):
        self.data = data
        self.children = [] if children is None else children


def traverse_combs(out_list, root, stack=None):
    if root == None:
        return

    stack = [] if stack is None else stack

    # append this node to the path array
    stack.append(root.data)
    if not root.children:
        # print out all of its
        # root - to - leaf
        comb = stack.copy()
        comb.remove(0)
        comb.sort()
        out_list.append(comb)

    # otherwise try both subtrees
    for child in root.children:
        traverse_combs(out_list, child, stack)

    stack.pop()


def find_subsets(sum_val, vals, in_val=0):

    if sum_val < vals[0]:
        return

    root_node = Node(in_val)
    for t in vals:
        if t < sum_val:
            node = find_subsets(sum_val - t, vals, t)
        elif t == sum_val:
            node = Node(t)
        else:
            node = None
        if node is not None:
            root_node.children.append(node)

    return root_node


def get_room_combs(num_people, num_rooms, types=(1, 2)):
    types = list(types)
    types.sort()
    types = tuple(types)

    if num_people / num_rooms > types[-1]:
        return []

    comb_tree = find_subsets(num_people, vals=types)
    comb_list = []
    traverse_combs(comb_list, comb_tree)
    comb_list = [list(x) for x in set(tuple(x) for x in comb_list)]
    comb_list = [c for c in comb_list if len(c) == num_rooms]

    return comb_list


def check_room_comb(room_comb, room_list):
    room_comb_ = room_comb.copy()
    room_list_ = []
    for room in room_list:
        room_cap = room.num_people
        if room_cap in room_comb_:
            room_comb_.remove(room_cap)
            room_list_.append(room)
    if room_comb_:
        return []
    else:
        return room_list_
