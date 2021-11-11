'''Main program to test Azure Computer Vision, image analysis'''
import os
from class_image import ImageClass
from computer_vision import ComputerVision

def main():
    '''Main function'''
    # Initialize Azure Computer Vision
    my_computer_vision = ComputerVision()

    image_folder = os.path.join(os.path.curdir, "images")
    if __debug__:
        image_folder = "C:/Users/perocha/OneDrive/MyCode/AI-testlab/image_analysis/images"

    for file_name in os.listdir(image_folder):
        # Open a new image
        print("\n######## Start with new image ########")
        print(f"Image file: {os.path.join(image_folder, file_name)}")
        filepath = os.path.join(image_folder, file_name)
        my_img_obj = ImageClass (filepath)

        # Execute image analysis
        my_computer_vision.image_analysis (my_img_obj)

        # Execute text extraction from the image
        my_computer_vision.get_text_ocr (my_img_obj)

        # Print the description
        print (f"Image description: {my_img_obj.description}")

        # Print all tags identified
        print (f"Total tags identified: {len(my_img_obj.tags)}")
        for tags in my_img_obj.tags:
            print (f" - '{tags}' ({my_img_obj.tags.get(tags)*100:.2f}%)")

        # Print the details of all identified objects or faces
        print (f"Total objects identified: {len(my_img_obj.objects)}")
        for obj in my_img_obj.objects:
            if obj.type == "Face":
                print (f" - '{obj.age}' {obj.gender}")
            elif obj.type == "Object":
                print (f" - '{obj.text}' ({obj.confidence*100:.2f}%)")
            else:
                print ("Error")

        # Create a new image with a box surrounding every identified object or face
        my_img_obj.create_obj_image ("objects")

        # Print text identified in the image (if any)
        if len(my_img_obj.text) > 0:
            print("Text extracted from image:")
            for line in my_img_obj.text:
                print(f"{line}")

    return False

if __name__ == "__main__":
    main()
