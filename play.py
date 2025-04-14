import os
import pyautogui
import time
import json
from pynput import keyboard
from PIL import ImageGrab
import tkinter as tk
from tkinter import filedialog
from time import strftime, sleep
import threading
import sys

# Esc tuşu kontrolü için global bayrak
exit_requested = False

def on_press(key):
    global exit_requested
    try:
        if key == keyboard.Key.esc:
            print("\nEscape tuşuna basıldı. Programdan çıkılıyor...")
            exit_requested = True
            # Tüm thread'leri durdurmak için exit çağır
            os._exit(0)
    except:
        pass

# Esc dinleyici başlat
listener = keyboard.Listener(on_press=on_press)
listener.start()

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(title="Bir dosya seçin")

if not file_path:
    print("Bir dosya seçmediniz!")
    exit()

def load_json(file_path):
    with open(file_path, 'r') as event_file:
        return json.load(event_file)

def save_screenshot(filename):
    if filename.strip():
        timestamp = strftime("%Y-%m-%d_%H-%M-%S")
        if not os.path.exists("img"):
            os.makedirs("img")
        full_path = os.path.join("img", f"{timestamp}_{filename}.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(full_path)
        print(f"Fotoğraf kaydedildi: {full_path}")
    else:
        print("Fotoğraf ismi boş! Kaydedilmedi.")

def play(events):
    print("5 saniye sonra başlıyor...")
    time.sleep(5)

    start_time = time.time()
    filename_chars = []
    enterbasildimi = False

    for event in events:
        if exit_requested:
            print("Çıkış isteği alındı.")
            return

        elapsed_time = time.time() - start_time
        wait_time = event["time"] - elapsed_time

        if wait_time > 0:
            time.sleep(wait_time)
        
        if exit_requested:
            print("Çıkış isteği alındı.")
            return
                             
        match event["action"]:
            case 0:
                key = event.get("key")
                if key is None:
                    print("Geçersiz tuş basma olayı, key None.")
                    continue

                if key == "Key.enter":
                    if enterbasildimi:
                        filename = ''.join(filename_chars)
                        save_screenshot(filename)
                        filename_chars = []
                        enterbasildimi = False
                    else:
                        enterbasildimi = True
                elif enterbasildimi and len(key) == 1:
                    filename_chars.append(key)

                pyautogui.keyDown(key)
            
            case 1:
                key = event.get("key")
                if key is None:
                    print("Geçersiz tuş bırakma olayı, key None.")
                    continue

                pyautogui.keyUp(key)
            case 2:
                pyautogui.moveTo(event["coordinate"][0], event["coordinate"][1])
            case 3:
                pyautogui.click(event["coordinate"][0], event["coordinate"][1])
            case _:
                print("Bilinmeyen olay:", event)

if __name__ == "__main__":
    try:
        say = int(input("Program kaç defa çalışsın? "))
        for i in range(say):
            if exit_requested:
                break
            try:
                events = load_json(file_path)
                play(events)
            except Exception as e:
                print(f"Hata oluştu: {e}")
    except KeyboardInterrupt:
        print("Klavye kesintisi ile çıkıldı.")