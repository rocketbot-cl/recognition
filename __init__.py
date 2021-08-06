import os
import sys
import subprocess
import cv2
from glob import glob
import time
import platform

def import_lib(relative_path, name, class_name=None):
    """
    - relative_path: library path from the module's libs folder
    - name: library name
    - class_name: class name to be imported. As 'from name import class_name'
    """
   
    import importlib.util

    cur_path = base_path + 'modules' + os.sep + 'recognition' + os.sep + 'libs' + os.sep

    spec = importlib.util.spec_from_file_location(name, cur_path + relative_path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    if class_name is not None:
        return getattr(foo, class_name)
    return foo



def search_reference_in_image(original, references=[], image_region=None, init_zoom=0, max_zoom=1.0, samples=20,
                              rotate=True, angle=2, match_porcent=.8, path_references_base=""):
    """Busca referencia en una imagen y devuelve la imagen recortada y en memoria:
        -------------------------------------------------------------------------
        References = Array de path de imagenes de referencia.
        Image_region = Busca en una region de la imagen original. {x,x2,y,y2}
        init_zoom = Escala en la que inicia la imagen.
        max_zoom = Maxima escala en Float.
        samples = Cantidad de ejemplos y escalas que se sacan entre init_zoom y max_zoom.
        Rotate = Gira la imagen +- grados para hacer match.
        angle = maximo de grados a girar.
        match_porcent = Porcentaje de igualdad entre la referencia y la base para pasar el filtro.
        path_references_base = Path base de los path de referencias de imagenes.
        @return posicion, (width, height) imagen de referencia
    """
    import cv2
    import numpy as np
    import imutils
    print(references)
    try:
        for ref in references:
            first = True
            print(ref)
            template = cv2.cvtColor(cv2.imread(path_references_base + ref), cv2.COLOR_BGR2GRAY)
            img_original = cv2.imread(original)
            (tH, tW) = template.shape[:2]
            if image_region:
                img_original = img_original[image_region["y"]:image_region["y2"], image_region["x"]:image_region["x2"]]
            img = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
            cv2.imwrite("search_on.png", img)
            ok = False
            range_ = [1]
            for aa in range(0, 1):
                for scale in np.linspace(init_zoom, max_zoom, samples)[::-1]:
                    if rotate and not first:
                        range_ = np.arange(-angle, angle, 1)
                    # resize the image according to the scale, and keep track
                    resized = imutils.resize(img, width=int(img.shape[1] * scale))
                    if resized.shape[0] < tH or resized.shape[1] < tW:
                        # Se supero el maximo de resizes, se vuelve
                        break
                    for r in range_:
                        if rotate and not first:
                            print("Rotate...")
                            img_o = imutils.rotate(resized, r)
                            cv2.imwrite("rot.png", resized)
                        else:
                            img_o = resized
                        try:
                            res = cv2.matchTemplate(img_o, template, cv2.TM_CCOEFF_NORMED)
                            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                            loc = np.where(res >= match_porcent)
                            z = zip(*loc[::-1])
                            # if len(z) > 0:
                            for i in z:
                                print("estamos en el for")
                                top_left = max_loc
                                bottom_right = (top_left[0] + tW, top_left[1] + tH)
                                cv2.rectangle(img_o, top_left, bottom_right, (0, 0, 255), 2)
                                cv2.imwrite("SIMAGE.png", img_o)
                                # return i[0], (tH, tW), scale, (top_left, bottom_right)
                                return True
                        except Exception as e:
                            print(e)
                first = False
    except Exception as e:
        print(e)
    print("Me salgo")
    return False

base_path = tmp_global_obj["basepath"]
cur_path = base_path + 'modules' + os.sep + 'recognition' + os.sep + 'libs' + os.sep
sys.path.append(cur_path)

import numpy as np
from convertPdfToPng import convertPdfToPng
from  imageExtensionChecker import imageExtensionChecker

platform_name = platform.system()
path_to_poppler = None

if (platform_name == "Windows"):
    cv2 = import_lib('cv2/cv2.cp36-win32.pyd', 'cv2')
    path_to_poppler = base_path + 'modules' + os.sep + 'recognition' + os.sep + 'bin' + os.sep + 'bin' + os.sep


        
module = GetParams("module")

try:

    if (module == "folder_recognition"):

        folderToCompare = GetParams("folderToCompare") + "/**/*"
        folderToCompare = folderToCompare.replace("/", os.sep)
        partialResult = GetParams("folderToCompare") + os.sep +"result.ini"

        result = None
        positiveMatch = None
        
        imageToSearch = GetParams("imageToSearch")
        imageToSearch = imageToSearch.replace("/", os.sep)

        separator = '/'
        imageName = (imageToSearch.split(os.sep)[-1])
        imageToSearchIn = None
        newPathImage = None
        converted = False
        
        if not (imageExtensionChecker(imageName)):
            newPathImage = convertPdfToPng(imageToSearch, path_to_poppler)
            imageToSearchIn = cv2.imread(newPathImage)
            converted = True
        else:
            imageToSearchIn = cv2.imread(imageToSearch)


        for eachFolderToCompare in glob(folderToCompare, recursive=True):
            result = eachFolderToCompare.replace("/", os.sep) + os.sep +"result.ini"
            eachFolderToCompare = eachFolderToCompare.replace("/", os.sep) + os.sep +"**" + os.sep + "*"
            for fileToCompareWith in glob(eachFolderToCompare, recursive=True):
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
                    
                    # SIFT_matches = cv2.drawMatchesKnn(imageToCompareWith, keypoints2, imageToSearchIn, keypoints1, good_matches, None, flags=2)
                    # cv2.imwrite("/home/keileb/myresult.png", SIFT_matches)

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
                            newPathImage = None
                            positiveMatch = 1
                        break
            if (positiveMatch == 1):
                break

        if (newPathImage != None):
            os.remove(newPathImage)

    if (module == "exact_match"):

        folderToCompare = GetParams("folderToCompare") + "/**/*"
        partialResult = GetParams("folderToCompare") + "/result.ini"
        result = None
        positiveMatch = None
        
        imageToSearch = GetParams("imageToSearch")

        separator = '/'
        imageName = (imageToSearch.split('/')[-1])
        imageToSearchIn = None
        newPathImage = None
        finalPathImage = None
        converted = False

        if not (imageExtensionChecker(imageName)):
            newPathImage = convertPdfToPng(imageToSearch, path_to_poppler)
            imageToSearchIn = cv2.imread(newPathImage)
            finalPathImage = newPathImage
            converted = True
        else:
            imageToSearchIn = cv2.imread(imageToSearch)
            finalPathImage = imageToSearch


        for eachFolderToCompare in glob(folderToCompare, recursive=True):
            result = eachFolderToCompare + "/result.ini"
            eachFolderToCompare = eachFolderToCompare + "/**/*"
            for fileToCompareWith in glob(eachFolderToCompare, recursive=True):
                if not (fileToCompareWith.endswith("ini")):

                    # imageToCompareWith = cv2.imread(fileToCompareWith)

                    # grey_img = cv2.cvtColor(imageToSearchIn, cv2.COLOR_BGR2GRAY)
                    # template = cv2.cvtColor(imageToCompareWith, cv2.COLOR_BGR2GRAY)

                    # res = cv2.matchTemplate(grey_img, template, cv2.TM_CCOEFF_NORMED)
                    a = []
                    a.append(fileToCompareWith)
                    if (search_reference_in_image(finalPathImage, a) == True):
                        varWhereToSaveIn = GetParams("varWhereToSaveIn")
                        file = open(result, "r")
                        fileRead = file.read()
                        SetVar(varWhereToSaveIn, fileRead)
                        file.close()
                        positiveMatch = 1

                        if (finalPathImage != None):
                            if converted:
                                os.remove(finalPathImage)
                                converted = False
                            finalPathImage = None
                            break

            if (positiveMatch == 1):
                break
        

        if converted:
            os.remove(finalPathImage)
            converted = False

except Exception as e:
    print("\x1B[" + "31;40mAn error occurred\u2193\x1B[" + "0m")
    PrintException()
    raise e


