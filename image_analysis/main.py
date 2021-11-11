'''Main program to test Azure Computer Vision, image analysis'''
import os
from class_image import ImageClass
from computer_vision import ComputerVision

def main():
    '''Main function'''
    # Initialize Azure Computer Vision
    my_computer_vision = ComputerVision()

    image_folder = os.path.join(os.path.curdir, "images")
    for file_name in os.listdir(image_folder):
        print("\n######## Start with new image ########")
        print(f"Image file: {os.path.join(image_folder, file_name)}")
        filepath = os.path.join(image_folder, file_name)
        my_img_obj = ImageClass (filepath)

        my_computer_vision.image_analysis (my_img_obj)

        print (f"Image description: {my_img_obj.description}")

        print (f"Total tags identified: {len(my_img_obj.tags)}")
        for tags in my_img_obj.tags:
            print (f" - '{tags}' ({my_img_obj.tags.get(tags)*100:.2f}%)")

        print (f"Total objects identified: {len(my_img_obj.objects)}")
        for obj in my_img_obj.objects:
            if obj.type == "Face":
                print (f" - '{obj.age}' {obj.gender}")
            elif obj.type == "Object":
                print (f" - '{obj.text}' ({obj.confidence*100:.2f}%)")
            else:
                print ("Error")

        my_img_obj.create_obj_image ("objects")

    return False

if __name__ == "__main__":
    main()
