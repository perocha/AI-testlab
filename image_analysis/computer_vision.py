'''
ComputerVision class
'''
#pylint: disable=broad-except
#pylint: disable=no-member

# Import namespaces
import os
from dotenv import load_dotenv
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from objects import ObjectClass

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
                               VisualFeatureTypes.objects]

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
        # Analyse image stream
        try:
            self.__ia = self.__cv.analyze_image_in_stream (image_obj.get_image(), self.__features)
            caption = self.__ia.description.captions

            # Update image description with the first caption
            image_obj.description = caption[0].text

            # Get image tags
            for tag in self.__ia.tags:
                image_obj.tags[tag.name] = tag.confidence

            # Get image objects
            for obj in self.__ia.objects:
                temp_obj = ObjectClass()
                temp_obj.text = obj.object_property
                temp_obj.confidence = obj.confidence
                temp_obj.x_coord = obj.rectangle.x
                temp_obj.y_coord = obj.rectangle.y
                temp_obj.width = obj.rectangle.w
                temp_obj.height = obj.rectangle.h
                image_obj.objects.append (temp_obj)

            return True

        except Exception as ex:
            print (ex)
            return False
