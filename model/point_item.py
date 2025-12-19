class PointItem:
    def __init__(self, depth: float, lateral: float):
        self.depth = depth
        self.lateral = lateral
        self.name = f"Point ({depth}, {lateral})"

    def get_depth(self):
        return self.depth
    
    def set_depth(self, depth):
        self.depth = depth

    def get_lateral(self):
        return self.lateral
    
    def set_lateral(self, lateral):
        self.lateral = lateral

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name