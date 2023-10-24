import cv2
import numpy as np
from PIL import Image
import time

def get_circles(gray):
    # find circles in the image and sort by y coordinate
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 21, param1=50, param2=22, minRadius=22, maxRadius=28)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        circles = circles[:, circles[0, :, 1] < 830]
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

def is_line_crossing_circle(start_x, start_y, end_x, end_y, center_x, center_y, radius):
    # check if the line is crossing the circle
    # https://stackoverflow.com/questions/1073336/circle-line-segment-collision-detection-algorithm
    dx = np.int64(end_x - start_x)
    dy = np.int64(end_y - start_y)
    fx = np.int64(start_x - center_x)
    fy = np.int64(start_y - center_y)
    radius = np.int64(radius)

    a = dx**2 + dy**2
    b = 2 * (dx * fx + dy * fy)
    c = fx**2 + fy**2 - radius**2

    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return False

    discriminant = np.sqrt(discriminant)
    t1 = (-b - discriminant) / (2 * a)
    t2 = (-b + discriminant) / (2 * a)

    if not (0 <= t1 <= 1 or 0 <= t2 <= 1):
        return False

    return True

def is_line_crossing_circles(start_circle, end_circle, circles):

    for circle in circles[0, 1:]:
        if np.array_equal(circle, start_circle) or np.array_equal(circle, end_circle):
            continue
        
        center_x, center_y, radius = circle

        # check if the line is crossing the circle
        if is_line_crossing_circle(start_circle[0], start_circle[1], end_circle[0], end_circle[1], center_x, center_y, radius):
            return True

    return False

def get_target_circle(open_cv_image, circles):
    template = get_template_circle()
    matched_one = False

    # for each circle, check if it matches the template (with color)
    for circle in circles[0, 1:]:
        # get the color of the template
        template_color = open_cv_image[template[1], template[0]]
        # get the color of the circle
        circle_color = open_cv_image[circle[1], circle[0]]

        if not np.allclose(template_color, circle_color, atol=10):
            continue

        matched_one = True

        if is_line_crossing_circles(template, circle, circles):
            continue

        return circle

    if circles is None or not matched_one:
        return None
    else:
        return np.array([100, 600, 27])


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
        target_circle = get_target_circle(open_cv_image, circles)
        display_circles(open_cv_image, circles, target_circle)

    # convert color format back to RGB
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    # convert the image back to PIL format
    image = Image.fromarray(open_cv_image)

    return image, target_circle
