import pytesseract
from PIL import Image,ImageFilter,ImageEnhance
import cv2
import PIL
'''
def pic_to_text():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    t=Image.open("txt.png")
    text = pytesseract.image_to_string(t, config='')
    print(text)


def cartonize():
    img=cv2.imread('dlrb.png')
    grayimg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    grayimg = cv2.medianBlur(grayimg, 5)
    edges = cv2.Laplacian(grayimg, cv2.CV_8U, ksize=5)
    r, mask = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)
    img2 = cv2.bitwise_and(img, img, mask=mask)
    img2 = cv2.medianBlur(img2, 5)

    cv2.imwrite("cartooned.jpg", mask)
'''
def imageEnhence():
    im=Image.open('dlrb.png')
    en = ImageEnhance.Color(im)
    en = ImageEnhance.Contrast(im)
    en = ImageEnhance.Brightness(im)
    en = ImageEnhance.Sharpness(im)  # result
    en.enhance(1.5).show("enhanced")

if __name__ == "__main__":
     imageEnhence()