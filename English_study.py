import sys
import tkinter
from tkinter import messagebox
from mutagen.mp3 import MP3 as mp3
from tkinter import *
import pygame
import time
import json
import random
from PIL import Image, ImageTk


def ques_start_next(event): # 問題を開始/もう一度音声を再生/次の問題を開始

    if bttn_repnxt['text'] == '音声を再生':

        global word1
        global word2
        global rep_word # 実際に発音された単語
        global id

        text_res["text"] = '' # 前回の問題への答えをリセット

        group = ps
        words = random.choice(list(wordlist['Wordlist'][group]))

        id = 'id' + str(quorder[qunum - renum])

        word1 = (wordlist['Wordlist'][group][id]['word1'])
        word2 = (wordlist['Wordlist'][group][id]['word2'])
        rep_word = wordlist['Wordlist'][group][id][random.choice(list(wordlist['Wordlist'][group][words]))]

        rep_mp3(rep_word)  # 音声ファイルを再生

        # オブジェクト状態の変更
        text_w1["text"] = word1
        text_w2["text"] = word2
        text_ques1["text"] = '発音されたのは…'
        text_ques2["text"] = 'どっち？'
        bttn_repnxt['text'] = 'もう1度再生'
        text_adc.place_forget()

    elif bttn_repnxt['text'] == 'もう1度再生':

        rep_mp3(rep_word)  # 音声ファイルを再生

    else:  # '次の問題を開始'

        # オブジェクト状態を変更
        bttn_repnxt['text'] = '音声を再生'
        text_res.place_forget()

        # 次の問題を開始 （音声ファイルを再生）
        ques_start_next(event)


def rep_mp3(tgt_word):  # 音声を再生

    filename = 'C:/Users/fumin/OneDrive/デスクトップ/English_words/' + tgt_word + '.mp3'  # 再生したいmp3ファイル
    pygame.mixer.init()
    pygame.mixer.music.load(filename)  # 音源を読み込み
    mp3_length = mp3(filename).info.length  # 音源の長さ取得
    pygame.mixer.music.play(1)  # 再生開始。1の部分を変えるとn回再生(その場合は次の行の秒数も×nすること)
    time.sleep(mp3_length + 0.25)  # 再生開始後、音源の長さだけ待つ(0.25待つのは誤差解消)
    pygame.mixer.music.stop()  # 音源の長さ待ったら再生停止


def enlarge_word(event):  # マウスポインタを置いたwordを大きく表示

    if str(event.widget["text"]) == word1:
        text_w1["font"] = ("", 12)   # 文字を大きく表示
        text_w1["cursor"] = "hand2"  # マウスポインタを人差し指型に変更
    else:
        text_w2["font"] = ("", 12)   # 文字を大きく表示
        text_w2["cursor"] = "hand2"  # マウスポインタを人差し指型に変更


def undo_word(event):  # マウスポインタから外れたwordを元のサイズに戻す

    if str(event.widget["text"]) == word1:
        text_w1["font"] = ("", 10)  # 文字を最初のサイズで表示
    else:
        text_w2["font"] = ("", 10)  # 文字を最初のサイズで表示


def choose_word(event):  # ユーザが選択したwordが正解かどうか判定

    global oknum
    global renum

    if bttn_repnxt['text'] == 'もう1度再生':

        # 正解と注意書きを表示
        text_res.place(x=175, y=130)
        text_adc.place(x=130, y=160)

        if str(event.widget["text"]) == word1:  # 左側の単語を選択した場合

            if rep_word == word1:
                text_res["text"] = '正解!!'
            else:
                text_res["text"] = '不正解…'

        else:  # 右側の単語を選択した場合

            if rep_word == word2:
                text_res["text"] = '正解!!'
            else:
                text_res["text"] = '不正解…'

        if text_res["text"] == '正解!!':

            oknum = oknum + 1  # 正解数を加算
            text_res["foreground"] = 'blue'
        else:
            text_res["foreground"] = 'red'

        renum -= 1  # 残りの問題数を減算

        # オブジェクト状態を変更
        text_scr['text'] = 'スコア： ' + str(oknum) + '/' + str(qunum)
        text_rest['text'] = '残り： ' + str(renum)
        text_ques1["text"] = ''
        text_ques2["text"] = ''
        bttn_repnxt["text"] = '次の問題を開始'

        if renum == 0:  # 全問題が終わった場合
            bttn_repnxt.place_forget()
            text_end.place(x=110, y=320)

    elif bttn_repnxt['text'] == '次の問題を開始':  # 次の問題の音声を再生

        if str(event.widget["text"]) == word1:

            rep_mp3(wordlist['Wordlist'][ps][id]['word1'])
        else:
            rep_mp3(wordlist['Wordlist'][ps][id]['word2'])


def create_radioboutton(row, column, pdx, num, value):  # タイトル画面のラジオボタンを生成

    rdbtn[num] = tkinter.Radiobutton(frame, value=value, command=rb_clicked, variable=var, text=u'')
    rdbtn[num].grid(row=row, column=column, padx=0, ipadx=pdx, pady=yinvl)


def create_picture(row='df', column='df', pdx='df', num='df'):  # タイトル画面の発音記号(画像)を生成

    if row == 'df' and column == 'df'and pdx == 'df'and num == 'df':  # タイトル画面の場合

        cv[rbnum] = Canvas(width=70, height=20)
        cv[rbnum].create_image(1, 1, image=pngfile[rbnum], anchor=NW)
        cv[rbnum].place(x=195, y=25)

    else:  # ゲーム開始画面の場合
        cv[num] = Canvas(frame, width=70, height=20)
        cv[num].create_image(1, 1, image=pngfile[num], anchor=NW)
        cv[num].grid(row=row, column=column, ipadx=pdx, pady=yinvl)


def rb_clicked():  # 勉強する発音記号を選択

    global rbnum
    global ps

    rbnum = int(var.get())  # 選択したラジオボタン(=発音記号)の番号を格納
    ps = list(wordlist['Wordlist'])[rbnum]  # 選択した発音記号を選択


def switch_mode(event):  # ゲームを開始 / タイトル画面に戻る

    global qunum    # 全問題の数
    global oknum    # 正解した問題の数
    global renum    # 残りの問題の数
    global quorder  # 問題出題の順番

    if bttn_swmode['text'] == 'ゲーム開始':

        # 最初の画面にあったオブジェクトを非表示
        frame.place_forget()
        text_title.place_forget()
        text_ques3.place_forget()

        # ゲーム用のオブジェクトを表示
        bttn_repnxt.place(x=155, y=70)
        text_scr.place(x=200, y=250)
        text_rest.place(x=130, y=250)
        text_w1.place(x=128, y=190)
        text_w2.place(x=228, y=190)
        text_ps.place(x=135, y=28)
        text_ques1.place(x=160, y=130)
        text_ques2.place(x=175, y=160)
        create_picture()

        # 各種設定
        oknum = 0
        qunum = len(wordlist['Wordlist'][ps])
        renum = qunum
        text_scr['text'] = 'スコア： ' + str(oknum) + '/' + str(qunum)
        text_rest['text'] = '残り： ' + str(renum)
        quorder = random.sample(range(1, qunum + 1), k=qunum)
        bttn_swmode['text'] = 'タイトルに戻る'
        text_w1["text"] = ''
        text_w2["text"] = ''
        text_ques1["text"] = ''
        text_ques2["text"] = ''
        bttn_repnxt['text'] = '音声を再生'

    else:  # タイトル画面に戻る

        if renum == 0 or (renum != 0 and messagebox.askyesno('確認', 'まだ問題が残っています。タイトル画面に戻りますか？')):

            # if messagebox.askyesno('確認', 'まだ問題が残っています。タイトル画面に戻りますか？'):

            # ゲーム画面にあったオブジェクトを非表示
            bttn_repnxt.place_forget()
            text_scr.place_forget()
            text_rest.place_forget()
            text_w1.place_forget()
            text_w2.place_forget()
            text_ps.place_forget()
            text_ques1.place_forget()
            text_ques2.place_forget()
            text_end.place_forget()
            text_res.place_forget()
            text_adc.place_forget()
            cv[rbnum].place_forget()

            # タイトル画面用のオブジェクトを表示
            frame.place(x=90, y=90)
            text_title.place(x=110, y=30)
            text_ques3.place(x=90, y=65)
            bttn_swmode['text'] = 'ゲーム開始'


# 画面の表示
root = tkinter.Tk()
root.title(u"発音くん")
root.geometry("400x420")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Frame
frame = tkinter.Frame(root)
frame.place(x=90, y=90)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

# ラベルの設定
text_w1 = tkinter.Label(text=u'', font=("", 10))
text_w1.bind("<Enter>", enlarge_word)
text_w1.bind("<Leave>", undo_word)
text_w1.bind("<Button-1>", choose_word)
text_w2 = tkinter.Label(text=u'', font=("", 10))
text_w2.bind("<Enter>", enlarge_word)
text_w2.bind("<Leave>", undo_word)
text_w2.bind("<Button-1>", choose_word)
text_ques1 = tkinter.Label(text=u'')
text_ques2 = tkinter.Label(text=u'')
text_ques3 = tkinter.Label(text=u'発音記号を選択し、ゲームを開始して下さい。')
text_ques3.place(x=90, y=65)
text_ps = tkinter.Label(text=u'発音記号：')
text_adc = tkinter.Label(text=u'※ 各単語クリックで音声再生')
text_res = tkinter.Label(text=u'')
text_scr = tkinter.Label(text=u'')
text_rest = tkinter.Label(text=u'')
text_title = tkinter.Label(text=u'発音くん(仮)', font=(u'ＭＳ 明朝', 20))
text_title.place(x=110, y=30)
text_end = tkinter.Label(text=u'この発音記号でのゲームは終了です。')
text_end["foreground"] = 'green'

# プッシュボタンの設定
bttn_repnxt = tkinter.Button(text=u'音声を再生', width=11)
bttn_repnxt.bind("<Button-1>", ques_start_next)  # （Button-2でホイールクリック、3で右クリック）
bttn_swmode = tkinter.Button(text=u'ゲーム開始', width=10)
bttn_swmode.bind("<Button-1>", switch_mode)  # （Button-2でホイールクリック、3で右クリック）
bttn_swmode.place(x=157, y=380)

# ラジオボタンの配置に使用するパラメータの設定
xinvl = 30
yinvl = 0
var = StringVar()
var.set('0')  # ラジオボタンを「チェックしていない状態」に設定
f = open("C:/Users/fumin/OneDrive/デスクトップ/Wordlist.json", 'r')
wordlist = json.load(f)
oknum = 0
rb_clicked()  # 初期状態で選択しているラジオボタン

# 画像情報及びラジオボタン情報を格納する変数の初期化
pngfile = [''] * len(wordlist['Wordlist'])
cv = [''] * len(wordlist['Wordlist'])
rdbtn = [''] * len(wordlist['Wordlist'])

# ラジオボタン/発音記号の設定
for i in range(int(len(wordlist['Wordlist'])/2)):

    ipadx = 10

    pngfile[i*2] = PhotoImage(file="C:/Users/fumin/OneDrive/画像/" + list(wordlist['Wordlist'])[i * 2] + ".PNG")
    pngfile[i*2+1] = PhotoImage(file="C:/Users/fumin/OneDrive/画像/" + list(wordlist['Wordlist'])[i * 2 + 1] + ".PNG")

    create_radioboutton(i+1, 1, 0, i*2, i*2)
    create_picture(i+1, 2, ipadx, i*2)
    create_radioboutton(i+1, 3, 0, i*2+1, i*2+1)
    create_picture(i+1, 4, ipadx, i*2+1)

root.mainloop()
