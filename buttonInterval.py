"""
buttonInterval.py
ボタンを押した間隔を測ります。
    button.txt   前に押した時間を記録
    interval.txt ボタンを押した間隔を記録　単位は秒*10000
        ファィルには整数で10000倍した数値が保存されています。
ボタンを押さなくなったら変化がないので、同じ数値があれば、
動いていないと判断するかな。

2020/05/20  datetimeでやろうとしたが、うまく行かないので、timeでやりました。
            動画再生のプログラムに組み込むには、ちょっとブルートゥースを制御しにくい
            感じだったので、別プログラムとして動かして、ファィル私にしようかと思います。
2020/05/21  event-noは個体固有でなく、早い者勝ちなので、シャッターボタンを1つにする事。
2020/05/23  シャッターボタンを28秒以上押さないと、プログラム終了させる。
"""

import evdev
import time
import timeout_decorator
 
@timeout_decorator.timeout(28)
def checkButton():
    with open('button.txt', mode='w') as f:
        f.write('0.0' )
    # ls /dev/input でevent番号要確認 event-noは早いもの順なので、
    # 使うシャッターボタンのみ電源を入れて、らずぱいを起動すべし。
    device = evdev.InputDevice('/dev/input/event5')
    # print(InputDevice)
    try:
        print('-',end='', flush=True)
        interval_tmp = 0
        for event in device.read_loop():

            # event = device.read_loop()
            # print('1',end='', flush=True)
            if event.type == evdev.ecodes.EV_KEY:
                # print('2',end='', flush=True)
                if event.value == 1: # 0:KEYUP, 1:KEYDOWN 
                    # print(event.code)
                    if event.code == evdev.ecodes.KEY_VOLUMEUP:
                        # print('iOS')
                        now_time = time.time()
                        with open('button.txt','r') as f:
                            last_time_s = f.read()
                            # print(last_time_s)
                        last_time = float(last_time_s)
                        # print(last_time)
                        interval = interval_tmp + int((now_time-last_time)*10000)
                        if interval > 7000:
                            interval_tmp = 0
                            interval = int(interval)
                            # print(interval)
                            with open('interval.txt', mode='w') as f:
                                f.write(str(interval))
                        else:
                            # チャタリング防止として0.7以下の数値であれば、加算のみ行う
                            interval_tmp = interval
                        with open('button.txt', mode='w') as f:
                            f.write(str(now_time))
                        time.sleep(0.2)
                        break

                    if event.code == evdev.ecodes.KEY_VOLUMEDOWN:
                        # print('Android')
                        now_time = time.time()
                        with open('button.txt','r') as f:
                            last_time_s = f.read()
                            # print(last_time_s)
                        last_time = float(last_time_s)
                        # print(last_time)
                        interval = int((now_time-last_time)*10000)
                        # print(interval)
                        with open('button.txt', mode='w') as f:
                            f.write(str(now_time))
                        with open('interval.txt', mode='w') as f:
                            f.write(str(interval))
                        time.sleep(0.2)
                        break
    except OSError:
        print('ファイルがない')
        with open('button.txt', mode='w') as f:
            f.write('0.0' )
    # except:
    #     print('Retry...')
    #     time.sleep(1)

def main():
    while True:
        print('.',end='', flush=True)
        checkButton()
        time.sleep(0.1)

if __name__ == '__main__':
    try:
        main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        print("key入力がありましたので、プログラム停止" )
        
    except :
        print('timeout')
