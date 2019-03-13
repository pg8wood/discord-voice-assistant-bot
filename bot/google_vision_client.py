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

    def detect_safe_search(self, path):
        """Detects unsafe features in the file."""
        from google.cloud import vision
        client = vision.ImageAnnotatorClient()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = client.safe_search_detection(image=image)
        safe = response.safe_search_annotation

        # Names of likelihood from google.cloud.vision.enums
        likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                           'LIKELY', 'VERY_LIKELY')
        print('Safe search:')

        print('adult: {}'.format(likelihood_name[safe.adult]))
        print('medical: {}'.format(likelihood_name[safe.medical]))
        print('spoofed: {}'.format(likelihood_name[safe.spoof]))
        print('violence: {}'.format(likelihood_name[safe.violence]))
        print('racy: {}'.format(likelihood_name[safe.racy]))

        return 'VERY_LIKELY' in likelihood_name[safe.adult]

    async def detect_safe_search_uri(self, uri):
        """Detects unsafe features in the file located in Google Cloud Storage or
        on the Web."""
        from google.cloud import vision
        client = vision.ImageAnnotatorClient()
        image = vision.types.Image()
        image.source.image_uri = uri

        response = await client.safe_search_detection(image=image)
        safe = response.safe_search_annotation

        # Names of likelihood from google.cloud.vision.enums
        likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                           'LIKELY', 'VERY_LIKELY')

        # Formats
        print('Safe search:')
        print('adult: {}'.format(likelihood_name[safe.adult]))
        print('medical: {}'.format(likelihood_name[safe.medical]))
        print('spoofed: {}'.format(likelihood_name[safe.spoof]))
        print('violence: {}'.format(likelihood_name[safe.violence]))
        print('racy: {}'.format(likelihood_name[safe.racy]))
        print(likelihood_name[safe.adult])
        return 'LIKELY' in likelihood_name[safe.adult]


if __name__ == "__main__":
    client = GoogleVisionClient()
    # client.analyze_image("/Users/PatrickGatewood/Downloads/test.jpg")
    # client.detect_safe_search("/Users/PatrickGatewood/Downloads/test.jpg")


