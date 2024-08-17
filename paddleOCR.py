### Необходимо скачать библиотеку paddleocr и модель 
### !pip install "paddleocr>=2.0.1"
### !python -m pip install paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple
import time
import os
import re

import pandas as pd
from paddleocr import PaddleOCR, draw_ocr
import cv2, re

ocr = PaddleOCR(use_angle_cls=True, lang='en')

pattern_1 = r'\d+:\d+:\d+:\d+'
pattern_2 = r'[A-Za-z0-9]+ [A-Za-z0-9]+ \d+:\d+:\d+:\d+'
pattern_3 = r'([A-Za-z]+)(\d+:\d+:\d+:\d+)'
pattern_4 = r'([^\s]+)\s+([A-Za-z0-9]+):(\d+:\d+:\d+:\d+)'
pattern_5 = r'([A-Za-z0-9]+):(\d+:\d+:\d+:\d+)'
pattern_6 = r'(\d+:\d+:\d+:\d+)\([A-Za-z0-9]+\)'

txt_pattern = r'3em'

def text_extraction(img_path):
  t_1 = time.time()
  result = ocr.ocr(img_path, cls=True)

  for idx in range(len(result)):
    res = result[idx]
  set_cad_num = set()
  result = result[0]
  if result is not None:
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]

    for i in range(len(txts)):
        if re.match(pattern_1, txts[i]) or re.match(pattern_2, txts[i]) or re.match(pattern_3, txts[i]) or re.match(pattern_4, txts[i]) or re.match(pattern_5, txts[i]) or re.match(pattern_6, txts[i]):
            cadastre_row = txts[i]
            if re.match(txt_pattern, cadastre_row):
              set_cad_num = set()
              set_scores = set()
            elif re.match(pattern_1, cadastre_row):      
              if len(cadastre_row) <=18:
                if scores[i] > 0.9:
                  cadastre_number = txts[i]
                  score = scores[i] 
                  set_cad_num.add(cadastre_number)
                  set_scores.add(score)


  t_2 = time.time()
  print("Processing time", t_2 - t_1)
  return set_cad_num, set_scores

img_path = 'avito_images_size_x_3/image_1.png'
x = text_extraction(img_path)
print(x)