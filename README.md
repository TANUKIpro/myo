# myoの使い方
### はじめに  
- [公式サイト](https://support.getmyo.com/hc/en-us)は完全に沈黙しており、更新が止まっている。~~(会社が買収されたからね)~~  
- Myo production has officially ended as of Oct 12, 2018 and is no longer available for purchase.(訳:Myoの生産は、2018年10月12日に正式に終了し、購入できなくなりました。)  
- 悲しい  
- __ISSUES__ にも逐一追加していく予定であるが、日本語サイトが少なく生産が終了しているデバイスなので、問題が発生した時に解決に時間がかかるor解決できない。  
TANUKIとしてもこれは非常に由々しき問題であり、自身の無能さを呪うばかりである。  
<font color="Green">頑張りまっする。</font>  

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
    TANUKIがいい加減な分解をしたため、筋電の一つが正しく測定されていない。  
    ![EMG](/data/figure_1.png)  

### myo_raw.pyの解説
1. データを分ける  
白と黒の二種のmyoで送られてくる値が違う。以下で混同しないよう分けている。(といってもグラフの描画がわかんなくなんないようにしてるだけであるが)  
```python
def data_plot(data):
        data_np = np.array(data)
        x0 = data_np[:,0]
        x1 = data_np[:,1]
        x2 = data_np[:,2]
        x3 = data_np[:,3]
        x4 = data_np[:,4]
        x5 = data_np[:,5]
        x6 = data_np[:,6]
        x7 = data_np[:,7]
        
        t = data_np[:,8]
        
        #Black Myo
        """
        plt.plot(t, x5, "r-", label="EMG A", color='greenyellow')
        plt.plot(t, x6, "r-", label="EMG B", color='lightsalmon')
        plt.plot(t, x7, "r-", label="EMG C", color='lightpink')
        plt.plot(t, x0, "r-", label="EMG D", color='black')
        plt.plot(t, x1, "r-", label="EMG E", color='red')
        plt.plot(t, x2, "r-", label="EMG F", color='green')
        plt.plot(t, x3, "r-", label="EMG G", color='blue')
        plt.plot(t, x4, "r-", label="EMG H", color='sienna')
        """
        
        #White Myo
        plt.plot(t, x3, "r-", label="EMG A", color='blue')
        plt.plot(t, x4, "r-", label="EMG B", color='sienna')
        plt.plot(t, x5, "r-", label="EMG C", color='greenyellow')
        plt.plot(t, x6, "r-", label="EMG D", color='lightsalmon')
        plt.plot(t, x7, "r-", label="EMG E", color='lightpink')
        plt.plot(t, x0, "r-", label="EMG F", color='black')
        plt.plot(t, x1, "r-", label="EMG G", color='red')
        plt.plot(t, x2, "r-", label="EMG H", color='green')
        
        plt.xlabel("Time[sec]", fontsize=16)
        plt.ylabel("EMG", fontsize=16)
        
        plt.grid()
        plt.legend(loc=1, fontsize=16)
        plt.show()
        #plt.pause(0.001)
        #plt.cla()
```  

2. 本当はリアルタイム描画したい  
    __python__ の __matpotlib__ でリアルタイム描画できるらしいからやってみたけど、なんか上手く行かない。できる人いたら教えて。