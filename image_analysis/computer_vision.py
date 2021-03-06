'''
ComputerVision class
'''
#pylint: disable=broad-except
#pylint: disable=no-member

# Import namespaces
import os
import time
from dotenv import load_dotenv
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from class_object import Object
from class_face import Face

class ComputerVision:
    '''Computer Vision class'''

    def __init__(self) -> None:
        '''Class constructor'''
        print ("ComputerVision::Initiating Computer Vision")
        try:
            # Get Azure configuration settings
            load_dotenv()
            cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
            cog_key = os.getenv('COG_SERVICE_KEY')

            # Authenticate Computer Vision client
            credential = CognitiveServicesCredentials(cog_key)
            self.__cv = ComputerVisionClient(cog_endpoint, credential)

            # Specify features to be retrieved
            self.__features = [VisualFeatureTypes.description,
                               VisualFeatureTypes.tags,
                               VisualFeatureTypes.categories,
                               VisualFeatureTypes.objects,
                               VisualFeatureTypes.faces]

            # Initiave analysis handler
            self.__ia = None

        except Exception as ex:
            print(ex)

    def __del__(self) -> None:
        '''Class destructor'''
        return True

    def image_analysis (self, image_obj):
        '''
        Execute image analysis of a given image stream
        '''
        try:
            # Analyse image stream
            image_obj.open_file()
            self.__ia = self.__cv.analyze_image_in_stream (image_obj.get_image(), self.__features)

            # Update image description with the first caption
            caption = self.__ia.description.captions
            image_obj.description = caption[0].text

            # Get image tags
            for tag in self.__ia.tags:
                image_obj.tags[tag.name] = tag.confidence

            # Get image objects
            for obj in self.__ia.objects:
                temp_obj = Object()
                temp_obj.text = obj.object_property
                temp_obj.confidence = obj.confidence
                temp_obj.x_coord = obj.rectangle.x
                temp_obj.y_coord = obj.rectangle.y
                temp_obj.width = obj.rectangle.w
                temp_obj.height = obj.rectangle.h
                image_obj.objects.append (temp_obj)

            for face in self.__ia.faces:
                temp_face = Face()
                temp_face.age = face.age
                temp_face.gender = face.gender
                temp_face.x_coord = face.face_rectangle.left
                temp_face.y_coord = face.face_rectangle.top
                temp_face.width = face.face_rectangle.width
                temp_face.height = face.face_rectangle.height
                image_obj.objects.append (temp_face)

            return True

        except Exception as ex:
            print (ex)
            return False

    def get_text_ocr (self, image_obj):
        '''
        Execute image analysis to get text
        '''
        try:
            # Use OCR API to read text in image
            image_obj.open_file()
            ocr_results = self.__cv.recognize_printed_text_in_stream(image_obj.get_image())

            # Make sure the image object doesn't have any previous text
            if len(image_obj.text) > 0:
                image_obj.text = []
            # Process the text line by line
            for region in ocr_results.regions:
                for line in region.lines:
                    # Start a new line
                    line_string = ""

                    # Read the words in the line of text
                    for word in line.words:
                        line_string += word.text + " "

                    # Once a new line is generated, add it to the image object
                    image_obj.text.append (line_string)

            return True

        except Exception as ex:
            print (ex)
            return False

    def read_text_from_image (self, image_obj):
        '''
        Read text from image
        '''
        try:
            # Use Read API to read text in image
            image_obj.open_file()
            read_op = self.__cv.read_in_stream(image_obj.get_image(), raw=True)

            # Get the async operation ID so we can check for the results
            operation_location = read_op.headers["Operation-Location"]
            operation_id = operation_location.split("/")[-1]

            # Wait for the asynchronous operation to complete
            while True:
                read_results = self.__cv.get_read_result(operation_id)
                if read_results.status not in [OperationStatusCodes.running, \
                    OperationStatusCodes.not_started]:
                    break
                time.sleep(1)

            # If the operation was successfuly, process the text line by line
            if read_results.status == OperationStatusCodes.succeeded:
                # First delete the existing text, if any
                if len(image_obj.text) > 0:
                    image_obj.text = []
                # Get the results
                for page in read_results.analyze_result.read_results:
                    for line in page.lines:
                        # Add the line to the image object
                        image_obj.text.append (line.text)

            return True

        except Exception as ex:
            print (ex)
            return False
