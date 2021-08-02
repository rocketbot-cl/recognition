from pdf2image import convert_from_path
import unicodedata


def convertPdfToPng(path, bin_path):
    newPng = convert_from_path(path, poppler_path=bin_path)
    newPngPath = path.replace("pdf", "png")
    newPngPath = unicodedata.normalize("NFKD", newPngPath).encode("ascii", "ignore").decode("ascii")
    newPng[0].save(newPngPath, "PNG")
    return newPngPath
