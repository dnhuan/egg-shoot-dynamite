import cv2
import numpy as np
from PIL import Image
import time

def get_circles(gray):
    # find circles in the image and sort by y coordinate
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=22, maxRadius=30)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        circles = circles[:, circles[0, :, 1] < 820]
        # sort by y coordinate
        circles[0, :] = circles[0, circles[0, :, 1].argsort()][::-1]


    return circles

def get_template_circle():
    return np.array([350, 840, 27])

def display_circles(open_cv_image, circles, target_circle=None):
    first_circle = get_template_circle()
    # draw the first circle in the image
    cv2.circle(open_cv_image, (first_circle[0], first_circle[1]), first_circle[2], (0, 255, 0), 2)
    cv2.circle(open_cv_image, (first_circle[0], first_circle[1]), 2, (0, 0, 255), 3)
    cv2.putText(open_cv_image, "Template", (first_circle[0], first_circle[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # draw circles in the image
    for _, circle in enumerate(circles[0, 1:]):
        cv2.circle(open_cv_image, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
        cv2.circle(open_cv_image, (circle[0], circle[1]), 2, (0, 0, 255), 3)
        # cv2.putText(open_cv_image, str(i), (circle[0], circle[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # draw the target circle in the image
    if target_circle is not None:
        cv2.circle(open_cv_image, (target_circle[0], target_circle[1]), target_circle[2], (0, 0, 255), 2)
        cv2.circle(open_cv_image, (target_circle[0], target_circle[1]), 2, (0, 0, 255), 3)
        cv2.putText(open_cv_image, "Target", (target_circle[0], target_circle[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # save the image with time in filename to folder "tmp"
    cv2.imwrite(f"tmp/{time.time()}.png", open_cv_image)

def get_template_matching_circle(open_cv_image, circles):
    template = get_template_circle()

    # for each circle, check if it matches the template (with color)
    for circle in circles[0, 1:]:
        # get the color of the template
        template_color = open_cv_image[template[1], template[0]]
        # get the color of the circle
        circle_color = open_cv_image[circle[1], circle[0]]
        # if the colors are the same, return the circle
        if np.array_equal(template_color, circle_color):
            return circle
        
    return None


def process_image(image):
    target_circle = None
    # Convert PIL Image to OpenCV Image (numpy array)
    open_cv_image = np.array(image)
    open_cv_image = open_cv_image[:, :, ::-1].copy() 

    # find and draw circles in the image
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    circles = get_circles(gray)
    if circles is not None:
        target_circle = get_template_matching_circle(open_cv_image, circles)
        display_circles(open_cv_image, circles, target_circle)

    # convert color format back to RGB
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    # convert the image back to PIL format
    image = Image.fromarray(open_cv_image)

    return image, target_circle
