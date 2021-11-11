'''
Image object class
'''

class ImageObject:
    '''Image object class'''

    def __init__(self) -> None:
        '''Constructor'''
        # Initialize variables
        self.x_coord = 0
        self.y_coord = 0
        self.width = 0
        self.height = 0

    def __del__(self):
        '''Class destructor'''
        return None

    def get_x (self):
        '''Return x coordinate of the object'''
        return self.x_coord

    def get_y (self):
        '''Return y coordinate of the object'''
        return self.y_coord

    def get_w (self):
        '''Return the width of the object'''
        return self.width

    def get_h (self):
        '''Return the height of the object'''
        return self.height
