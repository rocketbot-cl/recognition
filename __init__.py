import os
import sys
import subprocess
import cv2
from glob import glob

base_path = tmp_global_obj["basepath"]
cur_path = base_path + 'modules' + os.sep + 'recognition' + os.sep + 'libs' + os.sep
sys.path.append(cur_path)

import numpy as np
from pdf2image import convert_from_path, convert_from_bytes
        
module = GetParams("module")

try:
    if (module == "folder_recognition"):

        folderToCompare = GetParams("folderToCompare") + "/**/*"
        result = GetParams("folderToCompare") + "/result.ini"
        
        imageToSearch = GetParams("imageToSearch")

        separator = '/'
        imageName = (imageToSearch.split('/')[-1])
        imageExtension = (imageName.split('.')[-1])
        imageToSearchIn = None
        newPathImage = None

        if (imageExtension == "pdf"):
            image = convert_from_path(imageToSearch)
            newNameImage = imageToSearch.replace(imageExtension, "png")
            image[0].save(newNameImage, "PNG")
            
            a = imageToSearch.split('/')
            a[-1] = newNameImage.split('/')[-1]
            newPathImage = separator.join(a)
            imageToSearchIn = cv2.imread(newNameImage)
        else:
            imageToSearchIn = cv2.imread(imageToSearch)


        for fileToCompareWith in glob(folderToCompare, recursive=True):
            if(fileToCompareWith != result):

                imageToCompareWith = cv2.imread(fileToCompareWith)

                # Create our ORB detector and detect keypoints and descriptors
                sift = cv2.SIFT_create()

                # Find the key points and descriptors with ORB
                keypoints1, descriptors1 = sift.detectAndCompute(imageToSearchIn, None)
                keypoints2, descriptors2 = sift.detectAndCompute(imageToCompareWith, None)

                bf = cv2.BFMatcher()
                matches = bf.knnMatch (descriptors2, descriptors1,k=2)

                good_matches = []

                for m1, m2 in matches:
                    if (m1.distance < 0.6*m2.distance):
                        good_matches.append([m1])

                if ((len(good_matches) > 20)):
                    varWhereToSaveIn = GetParams("varWhereToSaveIn")
                    file = open(result, "r")
                    fileRead = file.read()
                    SetVar(varWhereToSaveIn, fileRead)
                    file.close()
                    # SIFT_matches = cv2.drawMatchesKnn(imageToCompareWith, keypoints2, imageToSearchIn, keypoints1, good_matches, None, flags=2)
                    # cv2.imwrite("/path/to/save/myresult.png", SIFT_matches)
                    if (newPathImage != None):
                        os.remove(newPathImage)
                    break

        if (newPathImage != None):
            os.remove(newPathImage)

except Exception as e:
    print("\x1B[" + "31;40mAn error occurred\u2193\x1B[" + "0m")
    PrintException()
    raise e