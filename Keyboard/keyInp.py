from pynput.keyboard import Key, Listener, KeyCode
import sys
import time
import pyautogui
import psutil

def on_press(key):
    print(str(key))
    app_name = "dota2.exe"
    
    #CTRL+L
    if key == KeyCode.from_char('\x0c') and app_name in (i.name() for i in psutil.process_iter()):
        time.sleep(1)
        pyautogui.write('Whopper, Whopper, Whopper, Whopper Junior , double, triple Whopper Flame grilled taste with perfect toppers I rule this daaay Lettuce , mayo , pickle , ketchup ‼️ It\'s okay if I don\'t want that Impossible or bacon Whopper Any Whopper my waaay Youuu ruuule you\'re seizing the day At Beee Kaaay, have it your waaay YOU RULE!\n')
    
    #CTRL+K
    elif key == KeyCode.from_char('\x0b') and app_name in (i.name() for i in psutil.process_iter()):
        time.sleep(1)
        pyautogui.write('My Grandfather smoked his whole life. I was about 10 years old when my mother said to him, \'If you ever want to see your grandchildren graduate, you have to stop immediately.\'. Tears welled up in his eyes when he realized what exactly was at stake. He gave it up immediately. Three years later he died of lung cancer. It was really sad and destroyed me. My mother said to me- \'Don\'t ever smoke. Please don\'t put your family through what your Grandfather put us through.\' I agreed. At 28, I have never touched a cigarette. I must say, I feel a very slight sense of regret for never having done it, because your gameplay gave me cancer anyway.\n')

    #CTRL+M
    elif key == KeyCode.from_char('\r') and app_name in (i.name() for i in psutil.process_iter()):
        time.sleep(1)
        pyautogui.write('Hi Divine 1 player here, just want to vent my frustration about recent TI results. ** all peruvians, and death to Thunder Predator! Who\'s with me\n', interval=0.001)
    
    #CTRL+P
    elif key == KeyCode.from_char('\x10') and app_name in (i.name() for i in psutil.process_iter()):
        time.sleep(1)
        pyautogui.press('\\')
        pyautogui.write('disconnect\n', interval=0.001)

def on_release(key):

    #print(str(key))
    if key == Key.esc:
        sys.exit()
        # Stop listener
        return False

with open("Keys.txt", "w") as file:
    for key in Key:
        file.write(str(key) + "\n")
with open("Processes.txt", "w") as file:
    for i in psutil.process_iter():
        file.write(i.name() + "\n")

time.sleep(2)
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()