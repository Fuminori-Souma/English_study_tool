import sys
import tkinter
import time
import re
import urllib.request
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class Frame(tkinter.Frame):

    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.master.title('音声ファイルをgetくん')
        self.master.geometry("400x300")

        # ラベルの設定
        text_1 = tkinter.Label(self, text=u'音声ファイルを取得したい単語を、下のテキストボックスに入力して下さい。')
        text_1.pack(pady='7')
        text_2 = tkinter.Label(self, text=u'※ 複数の単語を入力する場合は「,」で区切って下さい。')
        text_2.pack()

        # テキスト（エントリーの複数ver.）の設定
        self.ent_words = tkinter.Text(self, height=15)
        self.ent_words.pack(padx='30')

        # プッシュボタンの設定
        bttn_start = tkinter.Button(self, text = u'開始', command=self.start_get_file)
        bttn_start.bind("<Button-1>") #（Button-2でホイールクリック、3で右クリック）
        bttn_start.pack(pady='7')

    def checkAlnum(self, word):  # 入力された単語に不要な記号等が含まれていないかチェック
        alnum = re.compile(r'^[a-zA-Z]+$')  # 正規表現をコンパイル
        result = alnum.match(word) is not None  # matchで条件に合えばSRE_Match objectを、そうでなければNone(False)を返す
        return result

    def delete_symbols(self, word):  # 文字列に含まれた記号等を削除
        # return word.replace(',', '').replace('.', '').replace('-', '').replace(' ', '')
        return word.replace(',', '').replace(' ', '')

    def get_mp3(self, word, driver):  # weblioのページを開いてmp3ファイルを取得

        dir = 'C:/Users/fumin/OneDrive'  # 音声ファイルのダウンロード先

        # 単語検索用のテキストボックスに単語を入力して検索ボタンを押下
        driver.find_element_by_xpath("//*[@id=\"searchWord\"]").clear()  # テキストボックスを初期化
        driver.find_element_by_xpath("//*[@id=\"searchWord\"]").send_keys(word)
        driver.find_element_by_xpath("//*[@id=\"headFixBxTR\"]/input").click()
        time.sleep(5)

        # 音声ファイルが存在する（=「プレーヤー再生」が存在する）場合
        if not driver.find_elements_by_xpath("//*[@id=\"audioDownloadPlayUrl\"]/i") == []:

            # 「プレーヤー再生」を押してmp3ファイルを新しいウィンドウで開く
            driver.find_element_by_xpath("//*[@id=\"audioDownloadPlayUrl\"]/i").click()
            time.sleep(5)

            # 操作対象のウィンドウを、新しく開いたmp3ファイルに変更する
            handles = driver.window_handles
            driver.switch_to.window(handles[1])

            # mp3ファイルをダウンロードする
            urllib.request.urlretrieve(driver.current_url, (dir + '/' + word + '.mp3'))
            driver.close()

            # 操作対象のウィンドウを元のウィンドウに戻す
            driver.switch_to.window(handles[0])

            return 'OK'

        else:  # 音声ファイルが存在しない（=「プレーヤー再生」が存在しない）場合

            return 'NG'


    def start_get_file(self):

        reslist = {}  # 単語の音声ファイルが存在したか否か （空の辞書型で初期化）

        words = self.ent_words.get('1.0', 'end')  # テキストボックスに入力した単語リストを取得

        if self.checkAlnum(self.delete_symbols(words)):  # 正しく入力されている（英字及び「,」以外が入力されていない）場合

            ww = [x.strip() for x in words.split(',')]  # 入力の単語リストをカンマで区切ってlist型として格納

            # ブラウザを開く
            drv = webdriver.Chrome("C:/Users/fumin/pybraries/chromedriver_ver79/chromedriver")
            time.sleep(10)

            # 操作するページ（）を開く
            drv.get("https://ejje.weblio.jp/")
            time.sleep(10)

            j = 0  # NG単語(mp3ファイルが存在しない単語)の数

            for i in range(len(ww)):  # mp3ファイルを取得
                reslist[ww[i]] = self.get_mp3(ww[i], drv)

                if reslist[ww[i]] == 'NG':  # mp3ファイルが存在しない単語をNGリストに追加

                    j += 1

                    if j <= 1:  # １つ目のNG単語は文字列型として格納
                        nglist = ww[i]

                    elif j == 2:  # 2つ目のNG単語は1つ目とカンマ区切りで繋げてlist型に変換
                        nglist = (nglist + ',' + ww[i]).split(',')

                    else:  # 3つ目以降はlist型に順次追加
                        nglist.append(ww[i])

            drv.close()  # 単語取得処理が終了したらブラウザを閉じる

            if 'nglist' in locals():  # 音声ファイルが存在しなかった単語がある場合

                if j == 1:  # NG単語が１つだけの場合
                    messagebox.showinfo('', '下記を除いた、全単語の音声ファイルをダウンロードしました。\n\n' + nglist)
                else:  # NG単語が2つ以上の場合
                    messagebox.showinfo('', '下記を除いた、全単語の音声ファイルをダウンロードしました。\n\n' + ', '.join(nglist))
            else:
                messagebox.showinfo('', '入力された全単語の音声ファイルをダウンロードしました。')

        else:   # 正しく入力されていない（英字及び「,」以外が入力されている）場合
            messagebox.showinfo('', '英字及び「,」以外が入力されています。削除した後に再度実行して下さい。')


if __name__ == '__main__':

    # フレームの設定
    root = Frame()
    root.pack()
    root.mainloop()