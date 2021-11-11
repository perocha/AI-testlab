'''
Face class
'''
from class_image_objects import ImageObject

class Object (ImageObject):
    '''Face class from ImageObject base class'''

    def __init__(self) -> None:
        '''Constructor'''
        # Make sure we inherit the parent __init__ function
        ImageObject.__init__(self)

        # Initialize variables
        self.type = "Object"
        self.text = ""
        self.confidence = 0.0

    def get_text (self):
        '''Return the text description of the object'''
        return self.text

    def get_confidence (self):
        '''Return the confidence of the object identification'''
        return self.confidence
