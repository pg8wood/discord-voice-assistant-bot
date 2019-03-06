from google.cloud import vision
from google.cloud.vision import types
import io
import os


class GoogleVisionClient:
    """
    Analyzes images using the Google Cloud Vision API.
    """


    def __init__(self):
        self.client = vision.ImageAnnotatorClient()


    def analyze_image(self, path):
        # Loads the image into memory
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        # Performs label detection on the image file
        response = self.client.label_detection(image=image)
        labels = response.label_annotations

        print('Labels:')
        for label in labels:
            print(label.description)


if __name__ == "__main__":
    client = GoogleVisionClient()
    client.analyze_image("/Users/patrickgatewood/Downloads/homer.jpg")

