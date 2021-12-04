from django.db import connection
from hotel.models import Room


class Node:
    def __init__(self, data=None, children=None):
        self.data = data
        self.children = [] if children is None else children


def traverse_combs(out_list, root, stack=None):
    """
    Traverses all combinations from the given tree defined by the root node
    """
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
    """
    Finds all subsets (in form of a Tree) that sum to sum_val from given vals
    """
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
    """
    Given num_people and num_rooms, returns possible room combinations
    """
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
    """
    Returns the available rooms from room_list given desired room_comb
    """
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


def filter_rooms(hotel_id, start_date, end_date, num_people, num_rooms):
    """
    Given hotel, dates, num_pople and num_rooms; returns a room_list if possible
    """
    room_list = Room.objects.raw("SELECT * FROM room WHERE hotel_id = %s", [hotel_id])
    num_rooms = min(num_people, num_rooms)

    room_combs = get_room_combs(num_people, num_rooms)
    if room_combs:
        room_comb = room_combs[0]
    else:
        return []

    room_list_ = []
    with connection.cursor() as cursor:
        for room in room_list:
            cursor.execute(f"SELECT res_id FROM reserved_room WHERE room_id = %s", [room.id])
            res_id_tuple = cursor.fetchall()
            if res_id_tuple:
                cursor.execute(f"SELECT * FROM reservation WHERE id IN %s "
                               f"AND (CAST(%s AS DATE) <= start_date AND start_date < CAST(%s AS DATE)"
                               f" OR CAST(%s AS DATE) < end_date AND end_date <= CAST(%s AS DATE))",
                               [res_id_tuple, start_date, end_date, start_date, end_date])
                res_list = cursor.fetchall()
            else:
                res_list = ()
            if not res_list:
                room_list_.append(room)

    room_list_ = check_room_comb(room_comb, room_list_)
    return room_list_