class Obstacle(object):
    """Represents an obstacle in the field"""
    def __init__(self, origin_x, origin_y, width, height):
        self.origin = (origin_x, origin_y)
        self.width = width
        self.height = height
        self.size = (self.width, self.height)
    
    def draw(self, costmap):
        """Draws itself to a costmap"""
        o = (int(self.origin[0]/costmap.resolution), int(self.origin[1]/costmap.resolution))
        s = (int(self.size[0]/costmap.resolution), int(self.size[1]/costmap.resolution))
        costmap[o[0]:o[0]+s[0], o[1]:o[1]+s[1]] = -1.0
    
