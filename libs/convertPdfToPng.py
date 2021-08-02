from pdf2image import convert_from_path
import unicodedata

def convertPdfToPng(path):
    newPng = convert_from_path(path)
    newPngPath = path.replace("pdf", "png")
    newPngPath = unicodedata.normalize("NFKD", newPngPath).encode("ascii", "ignore").decode("ascii")
    newPng[0].save(newPngPath, "PNG")
    return newPngPath
