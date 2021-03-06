'''
Image class
'''
#pylint: disable=broad-except
#pylint: disable=consider-using-with

# Import namespaces
import os
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from class_face import Face
from class_object import Object

class ImageClass:
    '''Image class'''

    def __init__(self, filename) -> None:
        '''Constructor'''
        try:
            # Initialize variables
            self.filename = filename
            self.__file_handler = None

            # Initialize image analysis variables
            self.description = ""
            self.tags = {}
            self.objects = []
            self.faces = []
            self.text = []

            # Open the image file
            self.open_file()

        except Exception as ex:
            print(ex)

    def __del__(self):
        '''Class destructor'''
        # Make sure the file is closed
        self.__close_file ()

    def open_file (self):
        '''Open image file'''
        if self.filename != "":
            self.__file_handler = open(self.filename, mode="rb")
            return True

        # Error
        return False

    def __close_file (self):
        '''Close image file'''
        if self.__file_handler is not None:
            self.__file_handler.close()
        return True

    def get_image (self):
        '''Return the image stream'''
        return self.__file_handler

    def create_obj_image (self, folder):
        '''Create a new image with all the objects identified in the original image'''
        if len(self.objects) > 0:
            # Prepare image for drawing
            fig = plt.figure(figsize=(8, 8))
            plt.axis('off')
            image = Image.open(self.filename)
            for img_obj in self.objects:
                if isinstance(img_obj, Face):
                    annotation_string = f"{img_obj.gender} {img_obj.age}"
                elif isinstance (img_obj, Object):
                    annotation_string = f"{img_obj.text} {img_obj.confidence * 100:.1f}%"
                else:
                    annotation_string = ""
                draw = ImageDraw.Draw(image)
                color = 'cyan'

                # Draw object bounding box
                bounding_box = ((img_obj.get_x(), img_obj.get_y()), \
                    (img_obj.get_x() + img_obj.get_w(), img_obj.get_y() + img_obj.get_h()))
                draw.rectangle(bounding_box, outline=color, width=3)

                plt.annotate(annotation_string, (img_obj.get_x(), \
                    img_obj.get_y()), \
                    backgroundcolor=color)

            # Save annotated image
            plt.imshow(image)
            outputfile = f"{os.curdir}/{folder}/obj_{os.path.basename(self.filename)}"
            if __debug__:
                outputfile = f"obj_{os.path.basename(self.filename)}"
            fig.savefig(outputfile)
