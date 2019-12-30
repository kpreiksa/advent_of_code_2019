import datetime

orbits = {}

class Node():
    def __init__(self, name, parent = None):
        self._name = name
        self._parent = parent
        self._children = [] # List of Nodes

    def __eq__(self, other):
        if (isinstance(other, Node)):
            return self.name == other.name
        else:
            return False

    @property
    def isRootNode(self):
        return self._parent == None

    def __repr__(self):
        if self._parent:
            return(f'Node: "{self._name}". Parent: {self._parent.name} Children: [{self._children}]')
        else:
            return(f'Root Node: "{self._name}" Children: [{self._children}]')

    # def findCommonParent(self, other):
    #     while self._parent != other._parent:
    #         self.

    @property
    def name(self):
        return self._name

    @property
    def children(self):
        return self._children

    @property
    def numChildren(self):
        if self._children:
            return len(self._children)
        else:
            return 0
    
    @property
    def depthFromRoot(self):
        if self.isRootNode:
            return 0
        else:
            return self._parent.depthFromRoot + 1

    def depthFromNode(self, otherNode):
        if self == otherNode:
            return 0
        else:
            return self._parent.depthFromNode(otherNode) + 1

    def pathToRoot(self):
        lst = []
        n = self
        while not n.isRootNode:
            n = n._parent
            lst.append(n)
        return lst
    
    @property
    def childrenDict(self):
        return {x.name: x for x in self._children}

    def findChild(self, childID):
        if self.numChildren == 0:
            return None
        if childID in self.childrenDict:
            return self.childrenDict[childID]
        else:
            for child in self.children:
                found_child = child.findChild(childID)
                if found_child:
                    return found_child


    def getChild(self, childID):
        if isinstance(childID, int):
            return self.children[childID]
        elif isinstance(childID, str):
            return self.childrenDict[childID]

    def addChild(self, child):
        childNode = Node(child, self)
        self._children.append(childNode)

    def addChildren(self, children):
        childrenNodes = [Node(child, self) for child in children]
        self._children.extend(childrenNodes)

    def populate(self, orbits):
        if self._name in orbits:
            children = orbits[self._name]
            if (isinstance(children, list)):
                self.addChildren(children)
            else:
                self.addChild(children)

            for child in self._children:
                child.populate(orbits)
        else:
            self._children = None

start_time = datetime.datetime.now()
f = open('input.txt')
lines = f.readlines()
total_orbits = 0
for line in lines:
    split_line = line.strip().split(')')
    if len(split_line) == 2:
        object_being_orbited = split_line[0]
        object_orbiting = split_line[1]
        if object_being_orbited in orbits:
            orbits[object_being_orbited].append(object_orbiting)
        else:
            orbits[object_being_orbited] = [object_orbiting]
    else:
        raise ValueError('Expected 2 objects')

root = Node('COM')
root.populate(orbits)

san_node = root.findChild('SAN')
you_node = root.findChild('YOU')

path_root_to_san = san_node.pathToRoot()
path_root_to_you = you_node.pathToRoot()

path_root_to_san.reverse()
path_root_to_you.reverse()

common_root = None

for index, item in enumerate(path_root_to_san):
    if item != path_root_to_you[index]:
        common_root = path_root_to_san[index-1]
        break

depth_you = you_node.depthFromNode(common_root)
depth_san = san_node.depthFromNode(common_root)

orb_transfers = depth_you + depth_san - 2 # - 2 because we are transfering from your parent to san's parent

print(orb_transfers)

end_time = datetime.datetime.now()
time_diff = end_time - start_time

print(f'Execution Time: {time_diff}')