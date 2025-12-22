class CystItem:
    def __init__(self, depth: float, lateral: float,radius: float):
        self.depth = depth
        self.lateral = lateral
        self.radius = radius
        self.name = f"Cyst (d={depth}, l={lateral}, r={radius})"

    def get_depth(self):
        return self.depth / 1000
    
    def set_depth(self, depth):
        self.depth = depth

    def get_lateral(self):
        return self.lateral / 1000
    
    def set_lateral(self, lateral):
        self.lateral = lateral

    def get_radius(self):
        return self.radius / 1000
    
    def set_radius(self, radius):
        self.radius = radius

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name