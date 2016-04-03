from componentSystem.components.component import Component
from utilities.resourceManager import LoadResFile

def CreateSkeleton(skeletonInfo):
    skeleton = Skeleton()

    def _depthFirstJointAddition(skeleton, jointTree, path=None):
        connections = []
        for jointName, jointInfo in jointTree.iteritems():
            jointConnections = []
            if "connections" in jointInfo:
                jointPath = path + "." + jointName if path else jointName
                jointConnections = _depthFirstJointAddition(skeleton, jointInfo["connections"], jointPath)
                jointConnections = [jointPath + "." + connectionName for connectionName in jointConnections]
                connections += jointConnections

            skeleton.addJoint(path, jointName, jointInfo.get("lengthFromParent", 0), jointInfo["jointType"], jointConnections)
        return connections or jointTree.keys()

    connections = _depthFirstJointAddition(skeleton, skeletonInfo["jointTree"])

class Skeleton():
    def __init__(self):
        self.joints = []

    def addJoint(self, parentPath, name, lengthFromParent, jointType, connections):
        print "adding", parentPath, name, lengthFromParent, jointType, connections
        self.joints.append(name)

class SkeletonComponent(Component):
    __requiredAttributes__ = ["skeletonPath"]

    def __init__(self, entityName, componentInfo):
        Component.__init__(self, entityName, componentInfo)
        skeletonInfo = LoadResFile(self.skeletonPath)
        skeleton = CreateSkeleton(skeletonInfo)
