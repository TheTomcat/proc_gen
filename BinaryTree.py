# BinaryTree.py

class Node(object):
    """
    Tree node: left and right child, and some sort of payload
    """
    def __init__(self, data):
        """
        Node constructor

        @param data node data object
        """
        self.left = None
        self.right = None
        self.parent = None
        self.data = data
    @classmethod
    def _newNode(cls, data, parent):
        n = Node(data)
        n.parent = parent
        return n
    def insert(self, data):
        """
        Insert new node with data

        @param data node data object to insert
        """
        if data < self.data:
            if self.left is None:
                self.left=Node._newNode(data, self)
            else:
                self.left.insert(data)
        elif data > self.data:
            if self.right is None:
                self.right=Node._newNode(data, self)
            else:
                self.right.insert(data)
    def lookup(self, data, parent=None):
        """
        Lookup node containing data

        @param data node data object to look up
        @param parent node's parent
        @returns node and node's parent if found or None, None
        """
        if data < self.data:
            if self.left is None:
                return None, None
            return self.left.lookup(data, self)
        elif data > self.data:
            if self.right is None:
                return None, None
            return self.right.lookup(data, self)
        else:
            return self, parent
    def delete(self, data):
        """
        Delete node containing data

        @param data node's content to delete
        """
        node, parent = self.lookup(data)
        if node is not None:
            children_count = node.children_count()
            if children_count==0:
                if parent:
                    if parent.left is node:
                        parent.left = None
                    else:
                        parent.right=None
                del node
            elif children_count == 1:
                if node.left:
                    n = node.left
                else:
                    n = node.right
                if parent:
                    if parent.left is node:
                        parent.left = n
                    else:
                        parent.right = n
                    n.parent = parent
                del node
            else:
                current_node = node
                successor = node.right
                while successor.left:
                    print(current_node.data, successor.data)
                    current_node, successor = successor, successor.left
                node.data = successor.data
                if current_node.left==successor:
                    current_node.left = successor.right
                else:
                    current_node.right = successor.right
                del successor # I DON'T KNOW IF THIS SHOULD BE HERE...?
    def children_count(self):
        """
        Returns the number of children
        @returns number of children: 0, 1, 2
        """
        cnt=0
        if self.left:
            cnt+=1
        if self.right:
            cnt+=1
        return cnt
    def tree_data(self):
        """
        Generator to get the tree node data
        """
        stack = []
        node = self
        while stack or node:
            if node:
                stack.append(node)
                node=node.left
            else:
                node = stack.pop()
                yield node.data
                node = node.right

if __name__ == "__main__":
    import random
    random.seed(1)
    G = [i for i in range(0,1000)]
    random.shuffle(G)
    N = Node(G[0])
    _ = [N.insert(i) for i in G[1:]]
    
