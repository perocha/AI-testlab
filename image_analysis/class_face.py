'''
Face class
'''
from class_image_objects import ImageObject

class Face (ImageObject):
    '''Face class from ImageObject base class'''

    def __init__(self) -> None:
        '''Constructor'''
        # Make sure we inherit the parent __init__ function
        ImageObject.__init__(self)

        # Initialize variables
        self.type = "Face"
        self.age = 0
        self.gender = ""

    def get_age (self):
        '''Return the age of the face'''
        return self.age

    def get_gender (self):
        '''Return the gender of the face'''
        return self.gender
