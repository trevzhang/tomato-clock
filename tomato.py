#!/Library/Developer/CommandLineTools/usr/bin/python3
# -*- coding: utf-8 -*-

# Pomodoro 番茄工作法 https://en.wikipedia.org/wiki/Pomodoro_Technique
# ====== 🍅 Tomato Clock =======
# ./tomato.py         # start a 25 minutes tomato clock + 5 minutes break
# ./tomato.py -t      # start a 25 minutes tomato clock
# ./tomato.py -t <n>  # start a <n> minutes tomato clock
# ./tomato.py -b      # take a 5 minutes break
# ./tomato.py -b <n>  # take a <n> minutes break
# ./tomato.py -h      # help


import sys
import time
import subprocess

WORK_MINUTES = 25
BREAK_MINUTES = 5
LANG = 'Ting-Ting'
CN = True

def main():
    try:
        if len(sys.argv) <= 1:
            if not CN:
                print(f'🍅 tomato {WORK_MINUTES} minutes. Ctrl+C to exit')
                tomato(WORK_MINUTES, 'It is time to take a break')
            else:
                print(f'🍅 开始 {WORK_MINUTES} 分钟的番茄钟. Ctrl+C 取消')
                tomato(WORK_MINUTES, '恭喜你完成了一个番茄钟')

            if not CN:
                print(f'🛀 break {BREAK_MINUTES} minutes. Ctrl+C to exit')
                tomato(BREAK_MINUTES, 'It is time to work')
            else:
                print(f'🛀 休息 {BREAK_MINUTES} minutes. Ctrl+C 取消')
                tomato(BREAK_MINUTES, '休息时间结束，继续专注吧')

        elif sys.argv[1] == '-t':
            minutes = int(sys.argv[2]) if len(sys.argv) > 2 else WORK_MINUTES
            if not CN:
                print(f'🍅 tomato {minutes} minutes. Ctrl+C to exit')
                tomato(minutes, 'It is time to take a break')
            else:
                print(f'🍅 开始 {minutes} 分钟的番茄钟. Ctrl+C 取消')
                tomato(minutes, '恭喜你完成了一个番茄钟')

        elif sys.argv[1] == '-b':
            minutes = int(sys.argv[2]) if len(sys.argv) > 2 else BREAK_MINUTES
            if not CN:
                print(f'🛀 break {minutes} minutes. Ctrl+C to exit')
                tomato(minutes, 'It is time to work')
            else:
                print(f'🛀 休息 {minutes} 分钟. Ctrl+C 取消')
                tomato(minutes, '休息时间结束，继续专注吧')

        elif sys.argv[1] == '-h':
            help()

        else:
            help()

    except KeyboardInterrupt:
        print('\n👋 goodbye')
    except Exception as ex:
        print(ex)
        exit(1)


def tomato(minutes, notify_msg):
    start_time = time.perf_counter()
    while True:
        diff_seconds = int(round(time.perf_counter() - start_time))
        left_seconds = minutes * 60 - diff_seconds
        if left_seconds <= 0:
            print('')
            break

        countdown = time.strftime("%M:%S ⏰", time.localtime(left_seconds))
        duration = min(minutes, 25)
        progressbar(diff_seconds, minutes * 60, duration, countdown)
        time.sleep(1)

    notify_me(notify_msg)


def progressbar(curr, total, duration=10, extra=''):
    fraction = curr / total
    filled = round(fraction * duration)
    print('\r', '🍅' * filled + '--' * (duration - filled), '[{:.0%}]'.format(fraction), extra, end='')


def notify_me(msg):
    '''
    # macos desktop notification
    terminal-notifier -> https://github.com/julienXX/terminal-notifier#download
    terminal-notifier -message <msg>

    # ubuntu desktop notification
    notify-send

    # voice notification
    say -v <lang> <msg>
    lang options:
    - Daniel:       British English
    - Ting-Ting:    Mandarin
    - Sin-ji:       Cantonese
    '''

    print(msg)
    try:
        if sys.platform == 'darwin':
            # macos desktop notification
            subprocess.run(['terminal-notifier', '-title', '🍅', '-message', msg])
            subprocess.run(['say', '-v', LANG, msg])
        elif sys.platform.startswith('linux'):
            # ubuntu desktop notification
            subprocess.Popen(["notify-send", '🍅', msg])
        else:
            # windows?
            # TODO: windows notification
            pass

    except:
        # skip the notification error
        pass


def help():
    appname = sys.argv[0]
    appname = appname if appname.endswith('.py') else 'tomato'  # tomato is pypi package
    print('====== 🍅 Tomato Clock =======')
    print(f'{appname}         # start a {WORK_MINUTES} minutes tomato clock + {BREAK_MINUTES} minutes break')
    print(f'{appname} -t      # start a {WORK_MINUTES} minutes tomato clock')
    print(f'{appname} -t <n>  # start a <n> minutes tomato clock')
    print(f'{appname} -b      # take a {BREAK_MINUTES} minutes break')
    print(f'{appname} -b <n>  # take a <n> minutes break')
    print(f'{appname} -h      # help')


if __name__ == "__main__":
    main()
