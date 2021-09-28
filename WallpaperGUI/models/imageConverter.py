from PIL import Image

tempImageFile = '/home/Daxxn/Code/Python/Projects/WallpaperManager/WallpaperGUI/tempImage.png'

def convertImage(path: str, size: tuple[int, int] = None):
   image = Image.open(path)
   if size != None:
      if image.size[0] > size[0] or image.size[1] > size[1]:
         resizeAmount = resizeCalc(image.size, size)
         image = image.resize((round(image.size[0] * resizeAmount), round(image.size[1] * resizeAmount)))
   image.save(tempImageFile)
   return tempImageFile

def resizeCalc(imageSize: tuple[int, int], size: tuple[int, int], resizeAmount=0.99):
   if resizeAmount < 0.1:
      return resizeAmount
   if imageSize[0] * resizeAmount > size[0] or imageSize[1] * resizeAmount > size[1]:
      resizeAmount -= 0.01
      return resizeCalc(imageSize, size, round(resizeAmount, 2))
   else:
      return resizeAmount