class Obstacle(object):
    """Represents an obstacle in the field"""
    def __init__(self, origin_x, origin_y, width, height):
        self.origin = (origin_x, origin_y)
        self.width = width
        self.height = height
        self.size = (self.width, self.height)
    
