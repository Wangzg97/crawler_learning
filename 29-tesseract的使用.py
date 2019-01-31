import pytesseract
from PIL import Image

img = Image.open('yzm2.png')
code = pytesseract.image_to_string(img)  # 此处更改过image_to_string源码中的tesseract_cmd变量
print(code)
