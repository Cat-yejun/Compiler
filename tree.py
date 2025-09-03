class TreeNode: #트리의 노드 
    def __init__(self, data):
        self.data = data
        self.children = [] #자식을 담는 list


    def add_child(self, child): #자식을 추가하는 메소드
        self.children.append(child)


class Tree:
    def __init__(self, root):
        self.root = root

    def print_tree(self, node=None, level=0): #트리 출력
        if node is None:
            node = self.root
        
        if level > 0:
            print("   " * (level - 1) + "└──" + str(node.data))
        else:
            print(str(node.data))
        for child in node.children:
            self.print_tree(child, level + 1)

    def collect_tree(self, node=None, level=0):
        output = ""
        if node is None:
            node = self.root

        if level > 0:
            output += "   " * (level - 1) + "└──" + str(node.data) + "\n"
        else:
            output += str(node.data) + "\n"

        for child in node.children:
            output += self.collect_tree(child, level + 1)

        return output
