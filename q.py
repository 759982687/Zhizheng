import _thread
import time

def input_thread(a_list):
    input()
    a_list.append(True)

def do_stuff():
    a_list = []
    _thread.start_new_thread(input_thread, (a_list,))
    while not a_list:
        time.sleep(1)
        print('1')
    print(a_list)

do_stuff()


['😄','😂','❤️','😞','😭','✨','😌','😉','😢','😠']