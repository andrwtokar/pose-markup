import cv2
import numpy as np
from pose_markup.drawing_utils import draw_pose


def search_near_keypoint(keypoints, x, y):
    """Method for finding the closest keypoint to input coordinates (x, y)

    Args:
        keypoints (np.ndarray): keypoints to seach
        x (int): x-coordinate
        y (int): y-coordinate

    Returns:
        int: index of the nearest keypoint. Return None if the (x, y) do not cover the keypoint
    """
    min_dist = np.inf
    keypoint_ind = -1

    for ind, keypoint in enumerate(keypoints):
        dist = np.sqrt((keypoint[0] - x) ** 2 + (keypoint[1] - y) ** 2)
        if dist < min_dist and dist < 4:
            min_dist = dist
            keypoint_ind = ind

    if keypoint_ind == -1:
        return None

    return keypoint_ind


class MarkupImage:
    def __init__(self, image: np.ndarray, keypoints: np.ndarray) -> None:
        self.image = image
        self.keypoints = keypoints
        self.last_keypoint = []

    def run_and_quit(self, window_name: str, frame_num_info: str) -> bool:
        """The method implements the logic for data markup.

        Args:
            window_name (str): working window name 
            frame_num_info (str): information about the frame number in the video

        Returns:
            bool: processing completion flag 
        """
        def on_click(event, x, y, flags, param):
            # TODO: Возможно поиск ближайшей точки стоит делать не всегда, а только когда есть какой-то event
            near_keypoint = search_near_keypoint(self.keypoints, x, y)

            # TODO: Добавить возможность выставлять visubility в ноль.
            if event == cv2.EVENT_LBUTTONDOWN:
                self.last_keypoint.append(near_keypoint)
            if event == cv2.EVENT_LBUTTONUP:
                last_point = self.last_keypoint.pop()
                if last_point is not None:
                    self.keypoints[last_point][0] = x
                    self.keypoints[last_point][1] = y

            cv2.imshow(window_name, draw_pose(self.image, self.keypoints))

        cv2.namedWindow(window_name)
        cv2.setWindowTitle(window_name, f"{window_name} - {frame_num_info}")
        cv2.setMouseCallback(window_name, on_click)
        while True:
            cv2.imshow(window_name, draw_pose(self.image, self.keypoints))
            key = cv2.waitKey()

            if key == 13 or key == 32:
                break
            elif key == 27:
                return True

        return False

    def get_keypoints(self):
        return self.keypoints
