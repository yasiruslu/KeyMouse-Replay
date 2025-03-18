import os
import pyautogui
import time
import json
from pynput import keyboard
from time import strftime, sleep

print('Dosya yolunu giriniz:')
x = input().strip()  

# JSON okuma fonksiyonu
def load_json(file_path):
    with open(file_path, 'r') as event_file:
        return json.load(event_file)

# Fotoğraf kaydetme fonksiyonu
def save_screenshot(filename, file_path):
    if filename.strip():  # Eğer dosya ismi boş değilse
        timestamp = strftime("%Y-%m-%d_%H-%M-%S")
        full_path = os.path.join("img", f"{timestamp}_{filename}.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(full_path)
        print(f"Fotoğraf kaydedildi: {full_path}")
    else:
        print("Fotoğraf ismi boş! Kaydedilmedi.")

# Oynatma fonksiyonu
def play(events, file_path):
    print("5 saniye sonra başlıyor...")
    time.sleep(5)

    start_time = time.time()
    filename_chars = []
    enterbasildimi = False

    for event in events:
        elapsed_time = time.time() - start_time
        wait_time = event["time"] - elapsed_time

        if wait_time > 0:
            time.sleep(wait_time)

        match event["action"]:
            case 0:  # Tuşa basma
                key = event["key"]

                if key == "Key.enter":
                    if enterbasildimi:
                        filename = ''.join(filename_chars)  
                        save_screenshot(filename, file_path)
                        filename_chars = []
                        enterbasildimi = False
                    else:
                        enterbasildimi = True
                elif enterbasildimi and len(key) == 1:
                    filename_chars.append(key)

                pyautogui.keyDown(key)

            case 1:  # Tuşu bırakma
                pyautogui.keyUp(event["key"])
            case 2:  # Mouse hareketi
                pyautogui.moveTo(event["coordinate"][0], event["coordinate"][1])
            case 3:  # Mouse tıklaması
                pyautogui.click(event["coordinate"][0], event["coordinate"][1])
            case _:
                print("Bilinmeyen olay:", event)

if __name__ == "__main__":
    file_path = x  
    events = load_json(x)  
    play(events, file_path)