"""
シャターボタンを押すインターバルを記録し続ける
buttonInterval.py
と協調して動作。

スクワットを応援してくれるアプリ
SquatHelp.py

適度な間隔でスクワットをしていると
10回数えて、1ッセト
これを3セット応援してくれるかんじ。
応援=数える。

2020/05/23　start


"""
import subprocess
import time

subprocess.Popen('python3 ~/Bluetooth/buttonInterval.py',shell=True)

# スイッチの間隔を秒で取り出します。
def readInterval():
    with open('interval.txt','r') as f:
        read_data_s = f.read()
    read_data = int(read_data_s)
    return read_data

def speakPrint(say_word):
    print(say_word)
    subprocess.run('sh ~/julius/jsay_mei.sh ' + say_word,shell=True)
    return

def squat(squat_n):
    yell = ['もう一息','頑張れ','あと少し']
    interval_lt = readInterval()
    interval = interval_lt
    interval_same_n =0 # 同じインターバルが複数回続いたらプログラム終了へ
    for i in range(squat_n):
        while interval == interval_lt:
            interval = readInterval()
            interval_same_n += 1
            # print(interval,interval_same_n,' ',end='', flush=True)
            print('.',end='', flush=True)
            time.sleep(0.3)
            if interval_same_n > 100: # 同じインターバルが100回続くと、プログラム終了
                return 'タイムアウト'
        interval_same_n = 0
        interval_lt = interval
        say_word = str(i+1) + '回'
        if i in [5,7,8]:
            if interval % 2 == 0:
                say_word = yell[interval_lt % 3 ]
        speakPrint(say_word)
    return '正常'

def main():
    speakPrint('スクワットスタート')
    squat_n = 10

    if squat(squat_n) == 'タイムアウト':return       
    speakPrint('ここでちょっと休憩')
    time.sleep(4)

    speakPrint('はい、2セット目')
    if squat(squat_n) == 'タイムアウト':return   
    speakPrint('休憩しましょう')
    time.sleep(4)

    speakPrint('最後、3セット目')
    if squat(squat_n) == 'タイムアウト':return   

    end_yell = ['はい、がんばりました。終了です。','よくできました。終了です。','これで、終了です。次回もがんばりましょう','次もやりましょう']
    interval = readInterval()
    say_word = end_yell[interval % 4 ]
    speakPrint(say_word)


if __name__ == '__main__':
    # try:
    main()
    print()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    # except KeyboardInterrupt:
    #     print("key入力がありましたので、プログラム停止" )
    # except ValueError as e:
    #     print(e)
