'''
Image Analysis using Azure Computer Vision
'''
#pylint: disable=broad-except

# Import namespaces
import os
import sys
from dotenv import load_dotenv
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

def main():
    '''Main'''
    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')

        # Get image from arguments
        image_file = 'images/street.jpg'
        image_file = "C:/Users/perocha/OneDrive/MyCode/AI-testlab/image_analysis/images/street.jpg"

        if len(sys.argv) > 1:
            image_file = sys.argv[1]

        # Authenticate Computer Vision client
        credential = CognitiveServicesCredentials(cog_key)
        cv_client = ComputerVisionClient(cog_endpoint, credential)

        # Analyze image
        analyze_image (cv_client, image_file)

    except Exception as ex:
        print(ex)


def create_object_image(image_file, analysis):
    '''
    Create a new image with each identified object
    '''
    # Get objects in the image
    if len(analysis.objects) > 0:
        print("Objects in image:")

        # Prepare image for drawing
        fig = plt.figure(figsize=(8, 8))
        plt.axis('off')
        image = Image.open(image_file)
        draw = ImageDraw.Draw(image)
        color = 'cyan'
        for img_obj in analysis.objects:
            # Print object name
            print(f" -{img_obj.object_property} (confidence: {img_obj.confidence * 100:.2f}%)")

            # Draw object bounding box
            form = img_obj.rectangle
            bounding_box = ((form.x, form.y), (form.x + form.w, form.y + form.h))
            draw.rectangle(bounding_box, outline=color, width=3)
            annotation_string = f"{img_obj.object_property} {img_obj.confidence * 100:.1f}%"
            plt.annotate(annotation_string, (form.x, form.y), backgroundcolor=color)

        # Save annotated image
        plt.imshow(image)
        outputfile = 'objects.jpg'
        fig.savefig(outputfile)
        print('  Results saved in', outputfile)
    else:
        print ("No objects found")


def analyze_image(cv_client, image_file):
    '''
    Function to analyze a given image file
    '''
    print('Analyzing image: ', image_file)

    # Specify features to be retrieved
    features = [VisualFeatureTypes.description,
                VisualFeatureTypes.tags,
                VisualFeatureTypes.categories,
                VisualFeatureTypes.objects]

    # Get image analysis
    with open(image_file, mode="rb") as image_data:
        analysis = cv_client.analyze_image_in_stream(image_data , features)

    # Get image description
    for caption in analysis.description.captions:
        print(f"Description: '{caption.text}' (confidence: {caption.confidence * 100:.2f}%)")

    # Get image tags
    if len(analysis.tags) > 0:
        print("Tags: ")
        for tag in analysis.tags:
            print(f" -'{tag.name}' (confidence: {tag.confidence * 100:.2f}%)")

    # Get image categories (including landmarks)
    if len(analysis.categories) > 0:
        print("Categories:")
        landmarks = []
        for category in analysis.categories:
            # Print the category
            print(f" -'{category.name}' (confidence: {category.score * 100:.2f}%)")
            # Get landmarks in this category
            if category.detail.landmarks:
                print("Landmarks:")
                for landmark in category.detail.landmarks:
                    if landmark not in landmarks:
                        print(f" -'{landmark.name}' (confidence: {landmark.confidence * 100:.2f}%)")
                        landmarks.append(landmark)

    create_object_image (image_file, analysis)


if __name__ == "__main__":
    main()
