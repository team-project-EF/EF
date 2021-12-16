from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import argparse
import imutils
import dlib
import cv2
import os
from django.core.files.storage import default_storage
from ..apps import AreyouidolConfig as cf


def crop(f_name):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(
        "AreYouIdol/PreProcessing/shape_predictor_68_face_landmarks.dat")
    fa = FaceAligner(predictor, desiredFaceWidth=128)

    input_file = os.path.join(cf.img_path, f_name)
    out_file = os.path.join(cf.crop_path, f_name)

    image = cv2.imread(input_file)
    image = imutils.resize(image, width=800)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    if not os.path.exists(cf.crop_path):
        os.mkdir(cf.crop_path)

    # show the original input image and detect faces in the grayscale
    # image
    rects = detector(gray, 2)
    for rect in rects:
        print(rect)
        # extract the ROI of the *original* face, then align the face
        # using facial landmarks
        try:
            (x, y, w, h) = rect_to_bb(rect)
            faceOrig = imutils.resize(
                image[y:y + h, x:x + w], width=128)
            faceAligned = fa.align(image, gray, rect)

            # display the output images
            
            print(cv2.imwrite(out_file, faceAligned))
            cv2.waitKey(0)
            print(out_file)
        except Exception as e:
            print(e.args)
            print(e)
            print("CANNOT SAVE")
            continue
