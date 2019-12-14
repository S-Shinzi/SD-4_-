# -*- coding:utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
import tkinter as tki
from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
import numpy as np
import cv2
from PIL import Image, ImageTk
import sys
import pyocr
import pyocr.builders#pyocrを2列にする必要があるかはわからないが、精度が落ちると嫌なので一応書いておく
import time
import threading#カメラ関係、必須
import MySQLdb

def foon(event):
    connection = MySQLdb.connect(
            host = 'localhost',
            user = 'root',
            passwd = '',
            db = 'table_test',
            charset = 'utf8'
            )
    cursor = connection.cursor()

    # 一覧の表示
    cursor.execute("SELECT id, date, transfer_code, setsta_code, image, read_result, judge_result FROM kekka") 
    #ーーーーー↑↑↑kekkaを消してテーブル名を記入↑↑↑ーーーー
    
    for row in cursor:
        print(row)
    

    # ルートフレームの作成
    root = tk.Tk()
    root.geometry("700x227+0+20")
    # ツリービューの作成
    tree = ttk.Treeview(root)






    # 列インデックスの作成
    tree["columns"] = (1,2,3,4,5,6,7)
    # 表スタイルの設定(headingsはツリー形式ではない、通常の表形式)
    tree["show"] = "headings"
    # 各列の設定(インデックス,オプション(今回は幅を指定))
    tree.column(1,width=75)
    tree.column(2,width=75)
    tree.column(3,width=90)
    tree.column(4,width=90)
    tree.column(5,width=90)
    tree.column(6,width=90)
    tree.column(7,width=90)
    # 各列のヘッダー設定(インデックス,テキスト)
    tree.heading(1,text="ID")
    tree.heading(2,text="date")
    tree.heading(3,text="transfer_code")
    tree.heading(4,text="setsta_code")
    tree.heading(5,text="image")
    tree.heading(6,text="read_result")
    tree.heading(7,text="judge_result")


    # レコードの作成
    # 1番目の引数-配置場所（ツリー形式にしない表設定ではブランクとする）
    # 2番目の引数-end:表の配置順序を最下部に配置
    #             (行インデックス番号を指定することもできる)
    # 3番目の引数-values:レコードの値をタプルで指定する
    for row in cursor:
        tree.insert("","end",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
    tree.insert("","end",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
    tree.insert("","end",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
    tree.insert("","end",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
    tree.insert("","end",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
    tree.insert("","end",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
    tree.insert("","end",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
    tree.insert("","end",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
    tree.insert("","end",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
    tree.insert("","end",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
    tree.insert("","end",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
    tree.insert("","end",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
    tree.insert("","end",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
    tree.insert("","end",values=("X",row[1],row[2],row[3],row[4],row[5],row[6]))


    # ツリービューの配置
    tree.pack(fill="both")
    style.configure('Calendar.Treeview', rowheight=40)
    tree = ttk.Treeview(root, style='Calendar.Treeview')
    root.mainloop()


    # 保存を実行
    connection.commit()
    
    # 接続を閉じる
    connection.close()


#！！！最初に読んで下さい！！！
#現段階では、ウィンドウを消してもターミナルが消えず、カメラが起動したになってしまっています。
#VScode等で実行してしまった場合、VScodeのウィンドウを消さないとターミナル及びカメラが終了しないので
#起動する際はファイルを直接ダブルクリック等して起動することをお勧めします。


#import"文字読み取り"

root = tk.Tk()
root.title("定期")
root['background'] ='gray'
root.bind('<Escape>', lambda e: root.quit())
root.geometry("1000x600+0+20")
root.resizable(width=False, height=False)
#root.protocol('WM_DELETE_WINDOW', doSomething)  #ここに、右上X関係の処理のヒントがあります


lmain = tk.Label(root)
lmain.grid()


def on_closing():
    ret = messagebox.askyesno('確認', 'ウィンドウを閉じますか？')
    if ret == True:
        sys.exit()
    
root.protocol("WM_DELETE_WINDOW", on_closing)

def crozz(event):
    sys.exit()




def videoLoop(mirror=False):
    No=0
    cap = cv2.VideoCapture(No)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 0)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 0)

    while True:
        global frame
        ret, frame = cap.read()
        if mirror is True:
            frame = frame[:,::-1]

        # 表示用(補助線あり)とキャプチャ用の画像を分ける
        edframe = frame

        # 補助線を引く
        edframe = cv2.rectangle(edframe, (485,290), (1290,790),(0,0,255),10)

        # 指定した大きさにリサイズする。
        #edframe = cv2.resize(edframe,(291,245))

        # アスペクト比を固定して、幅が指定した値になるようリサイズする。
        def scale_to_width(img, width):
            scale = width / img.shape[1]
            return cv2.resize(img, dsize=None, fx=scale, fy=scale)


        edframe = scale_to_width(edframe, 291)

        image = cv2.cvtColor(edframe, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        panel = tk.Label(image=image)
        panel.image = image
        panel.grid(sticky=tk.W+tk.E+tk.N+tk.S)
        panel.place(x=325, y=35)

    return panel

def judgement(image_file):
    import OK_pasmo2
    import StationName_conv
    import judge
    import cv2

    cv2.imwrite('test.png', image_file)


    img=Image.fromarray(image_file)
    # 画像切り抜き img[top : bottom, left : right]
    frame_out = frame[290 : 790, 485 : 1290]
    # 切り抜いた画像を上下反転
    frame_out = cv2.rotate(frame_out, cv2.ROTATE_180)
    img_resize_lanczos = img.resize((290, 250), Image.LANCZOS)#サイズ変更と保存
    img = ImageTk.PhotoImage(img)
    # 画像を表示するためのキャンバスの作成（青で表示）
    canvas = tk.Canvas(bg = "blue", width=280, height=240)
    canvas.place(x=15, y=35) # 左上の座標を指定
    # キャンバスに画像を表示する。第一引数と第二引数は、x, yの座標
    canvas.create_image(0, 0, image=img, anchor=tk.NW)

    # 設置駅
    Set_Sta = ('OE', 9) #湘南台

    # 実施振替輸送（ex.JR1号振替→('JR', 1)）
    """
    JR東日本 : 'JR'
    都営地下鉄 : 'Toei'
    東京メトロ : 'TokyoMetro'
    東急電鉄 : 'Tokyu'
    京王電鉄 : 'Keio'
    相模鉄道 : 'Sotetu'
    横浜市営地下鉄 : 'YokohamaSubway'
    多摩都市モノレール : 'TamaMonorail'
    """
    Transfer = ('Tokyu', 1)

    # 定期券面画像
    """
    image_file = "C:/Users/user/Documents/pasmo/"
    image_file += "OE-09_JT-08"
    image_file += ".png"
    """


    ocrList = OK_pasmo2.PasumoOCR(image_file)

    txt2.insert(1.0, ocrList)

    Pass_Route = StationName_conv.CreatePassRoute(ocrList)

    Route_judge = judge.RouteJudge(Pass_Route, Transfer)

    Sta_judge = judge.StationJudge(Transfer, Set_Sta)

    txt3.insert(1.0,judge.Transport_judge(Route_judge, Sta_judge))



def dow():

    canvas01 = tk.Canvas(root, width=2800, height=2450)
    canvas01.create_rectangle(0, 0, 2800, 2450, fill='gray')
    canvas01.place(x=0, y=0)

    canvas01b = tk.Canvas(root, width=290, height=255)
    canvas01b.create_rectangle(0, 0, 949,333, fill='black')
    canvas01b.place(x=10, y=30)
    canvas01 = tk.Canvas(root, width=280, height=245)
    canvas01.create_rectangle(0, 0, 0, 0, fill='white')
    canvas01.place(x=15, y=35)


    canvas02b = tk.Canvas(root, width=302, height=255)
    canvas02b.create_rectangle(0, 0, 949,333, fill='black')
    canvas02b.place(x=320, y=30)
    canvas02 = tk.Canvas(root, width=292, height=245)
    canvas02.create_rectangle(0, 0, 0, 0, fill='white')
    canvas02.place(x=325, y=35)




    canvas03b = tk.Canvas(root, width=310, height=365)
    canvas03b.create_rectangle(0, 0, 310,365, fill='black')
    canvas03b.place(x=645, y=30)
    canvas03 = tk.Canvas(root, width=300, height=355)
    canvas03.create_rectangle(0, 0, 0, 0, fill='gray')
    canvas03.place(x=650, y=35)

    canvas02b = tk.Canvas(root, width=611, height=100)
    canvas02b.create_rectangle(0, 0, 949,333, fill='black')
    canvas02b.place(x=10, y=295)
    canvas02 = tk.Canvas(root, width=601, height=90)
    canvas02.create_rectangle(0, 0, 0, 0, fill='gray')
    canvas02.place(x=15, y=300)

    canvas05b = tk.Canvas(root, width=948, height=170)
    canvas05b.create_rectangle(0, 0, 949,199, fill='black')
    canvas05b.place(x=10, y=420)
    canvas02 = tk.Canvas(root, width=938, height=160)
    canvas02.create_rectangle(0, 0, 0, 0, fill='gray')
    canvas02.place(x=15, y=425)

    labela = tk.Label(root,text="振り替え情報")        #tk(乱数)をセット
    labela.place(x = 700,y = 80)  # rowspan=1 行感覚                            #tkを持ったlabelをウィンドウに表示

    labelb = tk.Label(root,text="設置駅")        #tk(乱数)をセット
    #labelb.grid(column=50, row=3,pady=10)                  #tkを持ったlabelをウィンドウに表示
    labelb.place(x = 700,y = 200)

    labelt = tk.Label(root,text="設定")        #tk(乱数)をセット                              #tkを持ったlabelをウィンドウに表示
    labelt.place(x = 700,y = 50)
    #label1 = tk.Label(root,text="label1 テキストが入れられます")        #tk(乱数)をセット
    #label1.grid()                                #tkを持ったlabelをウィンドウに表示
    #label1.place(x=602, y=80)

dow()

listn = ["AA","BB","CC"]
print(listn)

def delsan(event):
    del listn[0:3]
    print(listn)
    judgement(frame)
    #arai(event)

def popup(event):
    print("メッセージ、エラーが出ました") 
    txt3.insert('1.0', "メッセージ、エラーが出ました"+'\n')  
    messagebox.showerror("エラー", "ここにエラーメッセージを記入")
    #txt2.showinfo(title="Greetings", message="エラー!") 

class App(object):

    def __init__(self):
        self.root = tki.Tk()

    # create a Frame for the Text and Scrollbar
        txt_frm = tki.Frame(self.root, width=600, height=600)
        txt_frm.pack(fill="both", expand=True)
        # ensure a consistent GUI size
        txt_frm.grid_propagate(False)
        # implement stretchability
        txt_frm.grid_rowconfigure(0, weight=1)
        txt_frm.grid_columnconfigure(0, weight=1)

    # create a Text widget
        self.txt = tki.Text(txt_frm, borderwidth=3, relief="sunken")
        self.txt.config(font=("consolas", 12), undo=True, wrap='word')
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

    # create a Scrollbar and associate it with txt
        scrollb = tki.Scrollbar(txt_frm, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set



def win2(event):
    app = App()
    app.root.mainloop()

def teiki(event):
    """
    count = 0
    t1 = time.time() 
    image_file = "smkt.png"#まず、ここで読み取った画像を指定する
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
    box_area = np.array( [[72, 142, 348, 65],   #京王八王子
                        [614, 149, 279, 65],  #下北沢
                        [127, 229, 500, 39],  #明大前　　の文字がある座標を指定。 
                        ])  #これをすることで文字認識の精度がかなり上がる。

    box_area = ["AAA","BBB","CCC"]
    for box in box_area:#box_areaの数だけループする。指定したい場合は、レンジ？で指定する。
        #イメージは OpenCV -> PIL に変換する←　よくわからないけど重要そうなメモ
        txt = tool.image_to_string(Image.fromarray(img[box[1]:box[1]+box[3], box[0]:box[0]+box[2]]), lang="jpn", builder=pyocr.builders.TextBuilder(tesseract_layout=7))
        #↑で、日本語で処理をするとか、いろいろと設定をしている
        print(txt)#ここで読み取り結果を表示するようになっている。txtboxを試す
        count += 20 
        print(count)
        #label2 = tk.Label(root2,text=txt) "#   ここから３つはテスト用、消してもよし
        #label2.grid()                                #tkを持ったlabelをウィンドウに表示
        #label2.place(x=0, y= count + 20)
        txt2.insert('1.0', txt+'\n')
        listn.append(txt)

    # 計測したい処理
    for i in range(1000000):
        i ** 10
    
    # 処理後の時刻
    t2 = time.time()
    
    # 経過時間を表示
    elapsed_time = t2-t1
    print(f"経過時間：{elapsed_time}")
"""


def arai(event):
    print("実行")


    # 画像を表示するための準備
    img = Image.open('smkt.png')


    img_resize_lanczos = img.resize((290, 250), Image.LANCZOS)
    img_resize_lanczos.save('sumokita.png')
    img = Image.open('sumokita.png')#サイズ変更と保存

    img = ImageTk.PhotoImage(img)
    # 画像を表示するためのキャンバスの作成（青で表示）
    canvas = tk.Canvas(bg = "blue", width=280, height=240)
    canvas.place(x=15, y=35) # 左上の座標を指定
    # キャンバスに画像を表示する。第一引数と第二引数は、x, yの座標
    canvas.create_image(0, 0, image=img, anchor=tk.NW)

    teiki(event)# 画像を表示するための準備
    root.mainloop()#これがないとがぞうが表示されん。ウィンドウ作業完了の合図みたいなもんみたい


for i in range(1):                              #ボタンの数は１こ
              #winサイズと位置設定
    



        # ボタン、ウィンドウの設定
    button = tk.Button(root,text="判定")#ボタンの名前はダイスロール
    button2 = tk.Button(root,text="エラーテスト")

        # ウィジェットが左クリックされたときの関数を定義
    
    button.bind("<1>",delsan)  
    button2.bind("<1>",popup)
            
                #ボタンが押されることによってcallbackに飛ぶ
        # ボタンとテキストの配置
    button.place(x=40,y=2)    
    button2.place(x=10, y=400)                     #ウィンドウ内ボタンの位置



    combo = ttk.Combobox(root, state='readonly')
    combo2 = ttk.Combobox(root, state='readonly')
    # リストの値を設定
    combo["values"] = ("JR1号","JR2号","JR3号","JR4号","JR5号","JR6号","JR7号","JR8号","JR9号","JR10号",
    "都営地下鉄1号","都営地下鉄2号","都営地下鉄3号","都営地下鉄4号","都営地下鉄5号","都営地下鉄6号","都営地下鉄7号",
    "東京メトロ1号","東京メトロ2号","東京メトロ5号","東京メトロ9号","東京メトロ20号",
    "東急1号","東急2号","京王1号","相鉄","横浜市営地下鉄線","多摩モノレール")
    combo2["values"] = (
"OH01　新宿駅"
,"OH02　南新宿駅"
,"OH03　参宮橋駅"
,"OH04　代々木八幡駅"
,"OH05　代々木上原駅"
,"OH06　東北沢駅"
,"OH07　下北沢駅"
,"OH08　世田谷代田駅"
,"OH09　梅が丘駅"
,"OH10　豪徳寺駅"
,"OH11　経堂駅"
,"OH12　千歳船橋駅"
,"OH13　祖師ヶ谷大蔵駅"
,"OH14　成城学園前駅"
,"OH15　喜多見駅"
,"OH16　狛江駅"
,"OH17　和泉多摩川駅"
,"OH18　登戸駅"
,"OH19　向ヶ丘遊園駅"
,"OH20　生田駅"
,"OH21　読売ランド前駅"
,"OH22　百合ヶ丘駅"
,"OH23　新百合ヶ丘駅"
,"OH24　柿生駅"
,"OH25　鶴川駅"
,"OH26　玉川学園前"
,"OH27　町田駅"
,"OH28　相模大野駅"
,"OH29　小田急相模原駅"
,"OH30　相武台前駅"
,"OH31　座間駅"
,"OH32　海老名駅"
,"OH33　厚木駅"
,"OH34　本厚木駅"
,"OH35　愛甲石田駅"
,"OH36　伊勢原駅"
,"OH37　鶴巻温泉駅"
,"OH38　東海大学前駅"
,"OH39　秦野駅"
,"OH40　渋沢駅"
,"OH41　新松田駅"
,"OH42　開成駅"
,"OH43　栢山駅"
,"OH44　富水駅"
,"OH45　螢田駅"
,"OH46　足柄駅"
,"OH47　小田原駅"
,"OH48　箱根板橋駅"
,"OH49　風祭駅"
,"OH50　入生田駅"
,"OH51　箱根湯本駅"

,"OE01　東林間駅"
,"OE02　中央林間駅"
,"OE03　南林間駅"
,"OE04　鶴間駅"
,"OE05　大和駅"
,"OE06　桜ヶ丘駅"
,"OE07　高座渋谷駅"
,"OE08　長後駅"
,"OE09　湘南台駅"
,"OE10　六会日大前駅"
,"OE11　善行駅"
,"OE12　藤沢本町駅"
,"OE13　藤沢駅"
,"OE14　本鵠沼駅"
,"OE15　鵠沼海岸駅"
,"OE16　片瀬江ノ島駅"

,"OT01　五月台駅"
,"OT02　栗平駅"
,"OT03　黒川駅"
,"OT04　はるひ野駅"
,"OT05　小田急永山駅"
,"OT06　小田急多摩センター駅"
,"OT07　唐木田駅"

)
#pack
    combo.grid(column=50, row=0 )
    combo2.grid(column=50, row=1)
        # デフォルトの値を食費(index=0)に設定
    combo.current(0)
    combo2.current(0)
    # コンボボックスの配置
    combo.grid()
    combo.place(x=700, y=120)
    combo2.grid()
    combo2.place(x=700, y=240)
    # ボタンの作成（コールバックコマンドには、コンボボックスの値を取得しprintする処理を定義）
    button3 = tk.Button(text="ターミナルに表示",command=lambda:print(combo.get()+"\n",combo2.get()))#\nで改行,それぞれのcomboの値を表示
    button4 = tk.Button(root,text="ウィンドウ生成")
    button4.bind("<1>",foon) 
    # ボタンの配置
    button3.grid(column=50, row=20)
    button3.place(x=700, y=300)
    button4.grid(column=50, row=20)
    button4.place(x=820, y=300)


#width=935, height=150)

    root.title('Editor Test')

    text_widget = tk.Text(root, width=86, height=7)
    text_widget.grid()
    text_widget.place(x=15, y=300)
    #text_widget.pack(column=30, row=10, sticky=(tk.N, tk.S, tk.E, tk.W))


    # Frame
    frame1 = ttk.Frame(root, padding=3)
    frame1.rowconfigure(1, weight=1)
    frame1.columnconfigure(0, weight=1)
    frame1.grid()
    frame1.place(x=15, y=300)
    

    # Text
    f = Font(family='Helvetica', size=11)
    v1 = StringVar()
    txt2 = Text(frame1, width=72, height=5)
    txt2.configure(font=f)
    txt2.insert(1.0, "読み取り結果表示")
    txt2.grid(row=1, column=0)
    

    scrollbar = ttk.Scrollbar(
        frame1, 
        orient=VERTICAL, 
        command=txt2.yview)
    txt2['yscrollcommand'] = scrollbar.set
    scrollbar.grid(row=1,column=1,sticky=(N,S))
    




    #text_widget.pack(column=30, row=10, sticky=(tk.N, tk.S, tk.E, tk.W))


    # Frame
    frame2 = ttk.Frame(root, padding=3)
    frame2.rowconfigure(1, weight=1)
    frame2.columnconfigure(0, weight=1)
    frame2.grid()
    frame2.place(x=16, y=426)
    

    # Text
    f2 = Font(family='Helvetica', size=11)
    v1 = StringVar()
    txt3 = Text(frame2, width=114, height=9)
    txt3.configure(font=f2)
    txt3.insert(1.0, "エラー原因表示")
    txt3.grid(row=1, column=0)
    

    scrollbar = ttk.Scrollbar(
        frame2, 
        orient=VERTICAL, 
        command=txt3.yview)
    txt3['yscrollcommand'] = scrollbar.set
    scrollbar.grid(row=1,column=1,sticky=(N,S))


    a = tk.Label(root, text = "")
    a.grid()
    a.bind('<Key-c>', delsan)
    a.focus_set()

    #text_widgetD = tk.Text(root,width=42, height=19)
    #text_widgetD.place(x=324, y=34)
    #text_widget.pack(column=30, row=10, sticky=(tk.N, tk.S, tk.E, tk.W))



    thread = threading.Thread(target=videoLoop, args=())
    thread.start()



    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.mainloop()






root.mainloop()
sys.exit()