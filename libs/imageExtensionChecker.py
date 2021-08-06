def imageExtensionChecker(filename):
    filenameExtension = filename.split(".")[-1]
    filenameExtension = filenameExtension.lower()
    if (filenameExtension == "pdf"):
        return False
    # return True
    elif (filenameExtension in ("png", "jpg", "jpeg")):
        return True
