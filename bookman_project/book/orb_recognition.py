import numpy as np
import cv2


def extract_descriptors(image):
    # Convert the image to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Initialize the ORB detector
    orb = cv2.ORB_create()

    # Detect keypoints and compute the descriptors
    keypoints, descriptors = orb.detectAndCompute(image, None)

    # Convert keypoints to a list of points
    return descriptors


def compare_descriptors(descriptor1, descriptor2):
    # Initialize the FLANN matcher
    FLANN_INDEX_LSH = 6
    index_params = dict(algorithm=FLANN_INDEX_LSH,
                        table_number=6,
                        key_size=12,
                        multi_probe_level=1)
    search_params = dict(checks=50)
    matcher = cv2.FlannBasedMatcher(index_params, search_params)

    # Match the two sets of descriptors
    matches = matcher.knnMatch(descriptor1, descriptor2, k=2)

    # Keep only the good matches
    good_matches = []
    for match in matches:
        if len(match) >= 2:
            m, n = match
            if m.distance < 0.7*n.distance:
                good_matches.append(m)

    # Return the number of good matches
    return len(good_matches)
