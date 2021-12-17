class Frontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def isEmpty(self):
        return len(self.frontier) == 0

    def contains(self, node):
        for frontier_node in self.frontier:
            if frontier_node == node:
                return frontier_node
        return False

    def remove(self):
        if not self.isEmpty():
            best_node = self.frontier[0]
            current_level = best_node.level
            for node in self.frontier:
                if node.level < current_level:
                    best_node = node
                    current_level = best_node.level
            self.frontier.remove(best_node)
            return best_node
        raise Exception("Empty frontier")
