class PointItem:
    def __init__(self, depth: float, lateral: float):
        self.depth = depth
        self.lateral = lateral
        self.name = f"Point ({depth}, {lateral})"