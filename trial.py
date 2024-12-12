from trial_classes import *


solvable_frame_groups = [[Frame(node1=Node(name="A", bbox_x=172, bbox_y=292, shape_x=0, shape_y=0),
                                node2=Node(name="B", bbox_x=358, bbox_y=292, shape_x=4, shape_y=0),
                                obj_det_bbox=None, direction=None)],
                         [Frame(node1=Node(name="B", bbox_x=358, bbox_y=292, shape_x=4, shape_y=0),
                                node2=Node(name="C", bbox_x=529, bbox_y=294.0, shape_x=8, shape_y=0),
                                obj_det_bbox=None, direction=None),
                          Frame(node1=Node(name="C", bbox_x=529, bbox_y=294.0, shape_x=8, shape_y=0),
                                node2=Node(name="D", bbox_x=699, bbox_y=295.0, shape_x=12, shape_y=0),
                                obj_det_bbox=None, direction=None)]]


element2start = [Frame(node1=Node(name="B", bbox_x=358, bbox_y=292, shape_x=4, shape_y=0,Fx=0.0, Fy=0.0, M=0.0),
                       node2=Node(name="C", bbox_x=529, bbox_y=294.0, shape_x=8, shape_y=0,Fx=0.0, Fy=0.0, M=0.0),
                       obj_det_bbox=None, direction=None),
                 Frame(node1=Node(name="C", bbox_x=529, bbox_y=294.0, shape_x=8, shape_y=0,Fx=0.0, Fy=0.0, M=0.0),
                       node2=Node(name="D", bbox_x=699, bbox_y=295.0, shape_x=12, shape_y=0,Fx=0.0, Fy=0.0, M=0.0),
                       obj_det_bbox=None, direction=None)]

fix_support_instances = [FixSupport(node=Node(name="A", bbox_x=172, bbox_y=292, shape_x=0,
                                              shape_y=0,Fx=0.0, Fy=0.0, M=0.0), Fx=0, Fy=0, Moment=0, Direction = "Normal")]

pin_support_instances = []

roller_support_instances = [RollerSupport(node=Node(name="D", bbox_x=699, bbox_y=295.0,
                                                    shape_x=12, shape_y=0,Fx=0.0, Fy=0.0, M=0.0), F=0, Direction = "Vertical")]
hinge_instances = [Hinge(node=Node(name="B", bbox_x=358, bbox_y=292, shape_x=4, shape_y=0,Fx=0.0, Fy=0.0, M=0.0), Fx=0, Fy=0)]

def return_support_at_node(node_info):
    for support in fix_support_instances:
        if support.node.shape_x == node_info.shape_x and support.node.shape_y == node_info.shape_y:
            return support
    for support in pin_support_instances:
        if support.node.shape_x == node_info.shape_x and support.node.shape_y == node_info.shape_y:
            return support
    for support in roller_support_instances:
        if support.node.shape_x == node_info.shape_x and support.node.shape_y == node_info.shape_y:
            return support
    for hinge_info in hinge_instances:
        if hinge_info.node.shape_x == node_info.shape_x and hinge_info.node.shape_y == node_info.shape_y:
            return hinge_info


def find_unique_nodes(fg):
    unique_nodes = []
    common_nodes = []
    for el in fg:
        if el.node1 not in unique_nodes:
            unique_nodes.append(el.node1)
        else:
            common_nodes.append(el.node1)

        if el.node2 not in unique_nodes:
            unique_nodes.append(el.node2)
        else:
            common_nodes.append(el.node2)
        for i in common_nodes:
            unique_nodes.remove(i)
    return unique_nodes, common_nodes
def find_connected_elements2node(sorted_nodes):
    connected_elements = []
    for node in sorted_nodes:
        # Check frames
        support_info = return_support_at_node(node)
        if support_info:
            connected_elements.append(support_info)
    return connected_elements


def create_part_name(frame_group):
    un, cn = find_unique_nodes(frame_group)
    nl = un + cn
    sorted_nl = sorted(nl, key=lambda node: (node.shape_y, node.shape_x))
    return "".join(node.name for node in sorted_nl), sorted_nl


def create_solution(e2s, svg):
    if len(svg) == 1:
        part_name, sorted_node_list = create_part_name(e2s)
        # fill later
    else:
        # first page
        part_name, sorted_node_list = create_part_name(e2s)
        connected_elements = find_connected_elements2node(sorted_node_list)
        print(sorted_node_list)
        print("-------------")
        print(connected_elements)


create_solution(element2start, solvable_frame_groups)
