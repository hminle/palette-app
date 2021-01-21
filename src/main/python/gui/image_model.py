import copy
from PIL import Image

class ImageModel:

    def __init__(self):
        self.original_image = None # Lab
        self.current_image = None # Lab

    def load_image(self, input_path):
        self.original_image = Image.open(input_path)
        self.current_image = copy.deepcopy(self.original_image)

    def get_current_image(self):
        return copy.deepcopy(self.current_image)

    def get_original_image(self):
        return copy.deepcopy(self.original_image)

    def update_image(self, modified_image):
        self.current_image = modified_image

    def reset(self):
        self.current_image = copy.deepcopy(self.original_image)
