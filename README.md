# myoの使い方
### はじめに  
- [公式サイト](https://support.getmyo.com/hc/en-us)は完全に沈黙しており、更新が止まっている。  
- Myo production has officially ended as of Oct 12, 2018 and is no longer available for purchase.  
- __ISSUES__ にも逐一追加していく予定であるが、日本語サイトが少なく生産が終了しているデバイスなので、問題が発生した時に解決に時間がかかるor解決できない。    

### 用意するもの  
- Myo D5
- ドングル(Bluetooth受信用)  
<font color="Red">注意：専用の水色のドングルじゃないと受信できない。一緒についてくるやつ</font>
- WindowsPC
- LinuxPC(Ubuntu16 or 18)  
![myo](/data/myo.png)

### 手順
1. Myoにユーザーを登録する  
    - __WindowsPC__ で、[ココ](https://support.getmyo.com/hc/en-us/articles/360018409792)から __Myo Connect for Windows 1.0.1__ をダウンロード、実行する。  
    - 実行ファイルを開き、手順をすすめる。この時、ドングルとMyoをPCに接続しMyoの  
    ファームウェアアップデートとMyoの名前をつけるように指示されるので、それに従う。  
    - キャリブレーション等の細かい設定をすることもできるが、それについてはしなくていい。

2. Myoから筋電を取得する  
    - __UbuntuPC__ に切り替え、このリポジトリにあるmyo_raw.pyを実行する。  
    `$python myo_raw.py`
    - パーミッションエラーが出る場合、以下のコマンドを実行して、権限をつけてやる。  
    `$sudo chmod 777 /dev/ttyACM0`  
    ※ttyACM0はosが割り当てたドングルのデバイス番号なので、他にUSBが刺さってたら値が違うかもしれない。抜き差ししてttyACMの何番なのか確かめるのがいいかも。
     
3. 筋電のデータ
    - 筋電のデータは、myoとの通信が確立した時点から、Ctrl+cでプログラムが終了するまでのあいだ、リストに格納される。
    - 格納されたデータは、プログラム終了後グラフとして表示される。以下は測定結果の一例である。  
    いい加減な分解をしたため、筋電の一つが正しく測定されていない。  
    ![EMG](/data/figure_1.png)  

[元のコード](https://github.com/dzhu/myo-raw)は、PyGameを使った謎GUIがあったが消した。
