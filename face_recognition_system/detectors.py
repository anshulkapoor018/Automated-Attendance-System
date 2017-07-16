import cv2

class FaceDetector(object):

    def __init__(self, xml_path):
        # Create classifier object
        self.classifier = cv2.CascadeClassifier(xml_path)

    def detect(self, image, biggest_only=True):

        is_color = len(image) == 3
        if is_color:
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            image_gray = image
        # The algorithm checks for faces of different sizes,
        # the scale_factor is how much difference is between each size
        # that you want to check.
        # A bigger scale_factor means bigger jumps so it will perform
        # faster but less accuratelly, it is recommended 1.2 or 1.3
        scale_factor = 1.2

        # Treshold to detect a face, it needs a minimum of min_neighbors
        # neighbor pixels to return a detected a face on that pixel
        min_neighbors = 5

        # Sets the min_size of the face we want to detect. Default is 20x20
        min_size = (30, 30)

        # Change to True if we want to detect only one face
        flags = cv2.CASCADE_FIND_BIGGEST_OBJECT | \
            cv2.CASCADE_DO_ROUGH_SEARCH if biggest_only else \
            cv2.CASCADE_SCALE_IMAGE

        face_coord = self.classifier.detectMultiScale(
            image_gray,
            scaleFactor=scale_factor,
            minNeighbors=min_neighbors,
            minSize=min_size,
            flags=flags
        )

        return face_coord




