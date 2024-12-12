class Node:
    def __init__(self, bbox_x=None, bbox_y=None, shape_x=None, shape_y=None, name=None, Fx=0.0, Fy=0.0, M=0.0):
        self.bbox_x = bbox_x
        self.bbox_y = bbox_y
        self.shape_x = shape_x
        self.shape_y = shape_y
        self.name = name
        self.Fx = Fx
        self.Fy = Fy
        self.M = M

    def __eq__(self, other):
        if isinstance(other, Node):
            return (self.bbox_x == other.bbox_x and self.bbox_y == other.bbox_y
                    and self.shape_x == other.shape_x and self.shape_y == other.shape_y
                    and self.name == other.name)
        return False

    def __repr__(self):
        return f"Node(name={self.name}, bbox_x={self.bbox_x}, bbox_y={self.bbox_y}, shape_x={self.shape_x}, shape_y={self.shape_y},Fx={self.Fx}, Fy={self.Fy}, M={self.M})"


class Frame:
    def __init__(self, node1=None, node2=None, obj_det_bbox=None, direction=None):
        self.node1 = node1
        self.node2 = node2
        self.obj_det_bbox = obj_det_bbox
        self.direction = direction

    def __repr__(self):
        return f"Frame(node_1={repr(self.node1)}, node_2={repr(self.node2)}, obj_det_bbox={self.obj_det_bbox}, direction={self.direction})"




class FixSupport:
    def __init__(self, node=None, Fx = 0, Fy = 0, Moment = 0, Direction = None):
        self.node = node
        self.Fx = Fx
        self.Fy = Fy
        self.Moment = Moment
        self.Direction = Direction

    def __repr__(self):
        return f"FixSupport(node={self.node}, Fx={self.Fx}, Fy={self.Fy}, Moment={self.Moment}, Direction = {self.Direction})"

class PinSupport:
    def __init__(self, node=None,Fx = 0, Fy = 0, Direction = None):
        self.node = node
        self.Fx = Fx
        self.Fy = Fy
        self.Direction = Direction

    def __repr__(self):
        return f"PinSupport(node={self.node}, Fx={self.Fx}, Fy={self.Fy}, Direction = {self.Direction})"

class RollerSupport:
    def __init__(self, node=None, F= 0, Direction = None):
        self.node = node
        self.F = F
        self.Direction = Direction

    def __repr__(self):
        return f"RollerSupport(node={self.node}, F={self.F}, Direction = {self.Direction})"


class Hinge:
    def __init__(self, node=None,Fx = 0, Fy = 0):
        self.node = node
        self.Fx = Fx
        self.Fy = Fy

    def __repr__(self):
        return f"Hinge(node={self.node}, Fx={self.Fx}, Fy={self.Fy})"
