import numpy as np
import cv2
from PIL import Image
import sys
import pyocr
import pyocr.builders#pyocrを2列にする必要があるかはわからないが一応
import time
#import iogging ログ
# 処理前の時刻
t1 = time.time() 
image_file = "smkt.png"
img = cv2.imread(image_file)

# detect pink 
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower = np.array([0, 0, 0])    #真っ黒
upper = np.array([250, 250, 255])#(現状)青の文字のみが読み取れる範囲指定
img_mask = cv2.inRange(hsv, lower, upper)
img_color = cv2.bitwise_and(img, img, mask=img_mask)

# debug
cv2.imwrite("end.png", img_color)#黒文字になったのを保存。これで画像が完成。


white_pixels = (img == (0, 0, 0)).all(axis=-1)#背景の黒色を(0, 0, 0)、と指定
img[white_pixels] = (241,242,242)#ここで黒色(0, 0, 0)の範囲を背景の色(241,242,242)に、変更している。
cv2.imwrite("end.png", img)#おそらく、ここで変更された画像をセーブしている。

image_file = 'end.png'

#まず、ここで読み取った画像を指定する
img = cv2.imread(image_file)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower = np.array([0, 0, 0])    #色の情報。ここから、↓
upper = np.array([150, 200, 200])#ここまでの範囲を指定することで、青い文字以外を指定する。
img_mask = cv2.inRange(hsv, lower, upper)
img_color = cv2.bitwise_and(img, img, mask=img_mask)#おそらく、ここで背景（上の範囲指定、白背景と乗り物マークを含む）を黒くしている


cv2.imwrite("end.png", img_color)#ここで背景の黒い画像を保存して、
img = cv2.imread("end.png")#ここで背景の黒い画像を呼び出す。ここの処理がないと現状うまく画像ができない。


white_pixels = (img == (0, 0, 0)).all(axis=-1)#背景の黒色を(0, 0, 0)、と指定
img[white_pixels] = (241,242,242)#ここで黒色(0, 0, 0)の範囲を背景の色(241,242,242)に、変更している。
cv2.imwrite("end.png", img)#おそらく、ここで変更された画像をセーブしている。

#//ここまでで背景（青文字以外）を白色にする処理がされる//


# ここからは、うえの９行目～でやっている背景を黒くする処理と同じで、
image_file = 'end.png'#青文字のみを指定して、黒文字にしている
img = cv2.imread(image_file)

# detect pink 
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower = np.array([0, 0, 0])    #真っ黒
upper = np.array([150, 150, 250])#(現状)青の文字のみが読み取れる範囲指定
img_mask = cv2.inRange(hsv, lower, upper)
img_color = cv2.bitwise_and(img, img, mask=img_mask)

# debug
cv2.imwrite("end.png", img_color)#黒文字になったのを保存。これで画像が完成。



tools = pyocr.get_available_tools()#ここからはpyocrを用いた文字認識の処理となる。

if len(tools) == 0:#文字認識の環境ができていない場合は、ここで　No OCR tool found　の文字が出てくるようにする。
    print("No OCR tool found")
    sys.exit(1)

tool = tools[0]

img = cv2.imread("end.png", cv2.IMREAD_GRAYSCALE)


#座標の指定は x, y, width, Height
box_area = np.array( [[9, 127, 470, 99],   #START
                     [550, 120, 393, 95],  #END
                     [128, 227, 135, 37],  #経由　　の文字がある座標を指定。 
                    ])  #これをすることで文字認識の精度がかなり上がる。

for box in box_area:
    #イメージは OpenCV -> PIL に変換する←　よくわからないけど重要そうなメモ
    txt = tool.image_to_string(Image.fromarray(img[box[1]:box[1]+box[3], box[0]:box[0]+box[2]]), lang="jpn", builder=pyocr.builders.TextBuilder(tesseract_layout=7))
    #↑で、日本語で処理をするとか、いろいろと設定をしている
    print(txt)#ここで読み取り結果を表示するようになっている。

 
# 計測したい処理
for i in range(1000000):
    i ** 10
 
# 処理後の時刻
t2 = time.time()
 
# 経過時間を表示
elapsed_time = t2-t1
print(f"経過時間：{elapsed_time}")