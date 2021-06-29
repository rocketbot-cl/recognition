# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"
    
    pip install <package> -t .

"""
import os
import sys
import requests
import subprocess
from glob import glob


base_path = tmp_global_obj["basepath"]
cur_path = base_path + 'modules' + os.sep + 'ocrWithAI' + os.sep + 'libs' + os.sep
sys.path.append(cur_path)

from pdf2image import convert_from_path, convert_from_bytes

module = GetParams("module")

try:
    if (module == "classify_folder"):
    
        API_URL = 'http://0.0.0.0:5000'

        folderToClassify = GetParams("folderToClassify") + "/**/*"


        for fileToClassify in glob(folderToClassify, recursive=True):
            separator = '/'
            fileName = (fileToClassify.split('/')[-1])
            fileExtension = (fileName.split('.')[-1])

            if (fileExtension == "pdf"):
                image = convert_from_path(fileToClassify)
                # For documents more than 1 page
                # count = 0
                # for page in image:
                #     newNameFile = fileToClassify.replace("." + fileExtension, f"[{count}].jpg")
                #     (page.save(str(newNameFile), "JPEG"))
                #     count += 1
                newNameFile = fileToClassify.replace(fileExtension, "png")
                image[0].save(newNameFile, "PNG")
                
                a = fileToClassify.split('/')
                a[-1] = newNameFile.split('/')[-1]
                newPathFile = separator.join(a)
                newFile = open(newPathFile, 'rb')
                onlyTheName = newNameFile.split('/')[-1]

                response = requests.post('{}/files/{}'.format(API_URL, onlyTheName), data=newFile)
                realResponse = eval(response.content.decode(encoding='latin-1'))
                listaPalabras = GetParams("wordList")
                wordList = open(listaPalabras, "r")

                w = []
                w = wordList.readlines()

                wordListWithoutN = []
                for cadaPalabra in w:
                    wordListWithoutN.append(cadaPalabra.strip())

                countWords = 0
                for eachWord in realResponse:
                    for eachWordClassify in wordListWithoutN:
                        if ((eachWord.find(eachWordClassify) == 0) and (eachWordClassify != "")):
                            countWords += 1

                half = len(wordListWithoutN)/2
                folderToSave = GetParams("folderToSave")
                if (countWords > half):
                    if not os.path.exists(folderToSave):
                        os.makedirs(folderToSave)
                    os.rename(newPathFile, f"{folderToSave}/{onlyTheName}")
            
            elif (fileExtension == "png" or fileExtension == "jpg"):

                newFile = open(fileToClassify, 'rb')
                response = requests.post('{}/files/{}'.format(API_URL, fileName), data=newFile)
                realResponse = eval(response.content.decode(encoding='latin-1'))
                listaPalabras = GetParams("wordList")
                wordList = open(listaPalabras, "r")

                w = []
                w = wordList.readlines()

                wordListWithoutN = []
                for cadaPalabra in w:
                    wordListWithoutN.append(cadaPalabra.strip())

                countWords = 0
                for eachWord in realResponse:
                    for eachWordClassify in wordListWithoutN:
                        if ((eachWord.find(eachWordClassify) == 0) and (eachWordClassify != "")):
                            countWords += 1

                # Is this good?
                half = len(wordListWithoutN)/2
                folderToSave = GetParams("folderToSave")
                if (countWords > half):
                    if not os.path.exists(folderToSave):
                        os.makedirs(folderToSave)
                    os.rename(fileToClassify, f"{folderToSave}/{fileName}")

except Exception as e:
    print("\x1B[" + "31;40mAn error occurred\u2193\x1B[" + "0m")
    PrintException()
    raise e