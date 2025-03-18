from time import time, sleep
import json
from pynput import mouse, keyboard

mouse_listener = None
start_time = None
events = []
pressed_keys = set()  # Basılı tuşları sadece bir kez kaydeder

def save_json():
    """Kaydedilen olayları JSON dosyasına yazar"""
    with open('events.json', 'w') as event:
        json.dump(events, event, indent=4)

def on_press(key):
    global pressed_keys
       
    # Eğer tuş zaten basılıysa, tekrar kaydetme
    if key in pressed_keys:
        return

    pressed_keys.add(key)  # Tuşu basılı olarak işaretle

    try:
        save_event(current_time=round(time(), 2), action=0, key=key.char)
        print(f'Alphanumeric key {key.char} pressed')
    except AttributeError:
        save_event(current_time=round(time(), 2), action=0, key=str(key))
        print(f'Special key {key} pressed')

def on_release(key):
    global pressed_keys

    if key in pressed_keys:
        pressed_keys.remove(key)

    try:
        print(f'{key} released')
        if key == keyboard.Key.esc:
            mouse_listener.stop()
            save_json()
            print('Program durduruldu')
            return False
        save_event(current_time=round(time(), 2), action=1, key=key.char)
    except:
        save_event(current_time=round(time(), 2), action=1, key=str(key))

def on_click(x, y, button, pressed):
    if pressed:
        save_event(current_time=round(time(), 2), action=3, coordinate=[x, y])
        print(f'Clicked at {(x, y)}')

class ActionTypes:
    KEYPRESS = 0  # Tuşa basma olayını temsil 

    KEYRELEASE = 1  # Tuşu bırakmayı temsil eder
    MOUSECLICK = 3  # Fare tıklama olayını temsil eder

def save_event(current_time, action, key='', coordinate=[]):
    elapsed_time = current_time - start_time
    theduration = round(elapsed_time, 2)
    if action == ActionTypes.KEYPRESS:
        info = {'time': theduration, 'action': ActionTypes.KEYPRESS, 'key': key}
    elif action == ActionTypes.KEYRELEASE:
        info = {'time': theduration, 'action': ActionTypes.KEYRELEASE, 'key': key}
    elif action == ActionTypes.MOUSECLICK:
        info = {'time': theduration, 'action': ActionTypes.MOUSECLICK, 'coordinate': coordinate}
    
    events.append(info)

def run():
    global start_time
    input('Başlamak İçin ENTER, Bitirmek için ESC Tuşuna Basınız ...')

    print("\n10 saniye bekleniyor...")
    sleep(10)  # 10 saniye bekle

    start_time = round(time(), 10)
    events.append({'time': 0, 'action': 'Kayıt Başladı'})

    global mouse_listener

    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    mouse_listener = mouse.Listener(on_click=on_click)

    keyboard_listener.start()
    mouse_listener.start()
    
    keyboard_listener.join()
    mouse_listener.join()

    print(events)

if __name__ == '__main__':
    run()
