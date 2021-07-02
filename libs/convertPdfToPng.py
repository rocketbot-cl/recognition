from pdf2image import convert_from_path

def convertPdfToPng(path):
    newPng = convert_from_path(path)
    newPngPath = path.replace("pdf", "png")
    newPng[0].save(newPngPath, "PNG")
    return newPngPath
