import cv2
import numpy as np
import os

def compare_images(img1_path, img2_path, threshold=0.1):
    """
    对比两张图片，返回是否存在视觉差异。
    threshold为阈值，表示相差像素比例，超过认为不同。
    """
    if not os.path.exists(img1_path) or not os.path.exists(img2_path):
        return False, "One of the images does not exist."

    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    if img1.shape != img2.shape:
        return True, "Image sizes differ."

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    diff_count = cv2.countNonZero(thresh)
    total = img1.shape[0] * img1.shape[1]

    diff_ratio = diff_count / total
    return diff_ratio > threshold, f"Diff ratio: {diff_ratio:.3f}"