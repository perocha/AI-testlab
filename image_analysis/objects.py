'''
Object class
'''
#pylint: disable=broad-except

# Import namespaces

class ObjectClass:
    '''Object class'''

    def __init__(self) -> None:
        '''Constructor'''
        try:
            # Initialize variables
            self.x_coord = 0
            self.y_coord = 0
            self.width = 0
            self.height = 0
            self.text = ""
            self.confidence = 0.0

        except Exception as ex:
            print(ex)

    def __del__(self):
        '''Class destructor'''
        return None
