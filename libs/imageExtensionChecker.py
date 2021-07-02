def imageExtensionChecker(filename):
    filenameExtension = filename.split(".")[-1]
    if (filenameExtension == "pdf"):
        return False
    elif (filenameExtension == "png" or filenameExtension == "jpg"):
        return True
