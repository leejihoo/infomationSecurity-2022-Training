# Enigma Template Code for CNU Information Security 2022
# Resources from https://www.cryptomuseum.com/crypto/enigma

# This Enigma code implements Enigma I, which is utilized by 
# Wehrmacht and Luftwaffe, Nazi Germany. 
# This version of Enigma does not contain wheel settings, skipped for
# adjusting difficulty of the assignment.

from copy import deepcopy
from ctypes import ArgumentError

# Enigma Components
ETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

WHEELS = {
    "I" : {
        "wire": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "turn": 16,
        "max": 16
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "turn": 4,
        "max": 4
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "turn": 21,
        "max": 21
    }
}

# 반사판 26개의 알파벳이 2개씩 묶여 13개의 쌍을 이루고 서로 치환 된다.
UKW = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

# Enigma Settings
SETTINGS = {
    "UKW": None,
    "WHEELS": [],
    "WHEEL_POS": [],
    "ETW": ETW,
    "PLUGBOARD": []
}

def apply_settings(ukw, wheel, wheel_pos, plugboard):
    if not ukw in UKW:
        raise ArgumentError(f"UKW {ukw} does not exist!")
    SETTINGS["UKW"] = UKW[ukw]

    wheels = wheel.split(' ')
    for wh in wheels:
        if not wh in WHEELS:
            raise ArgumentError(f"WHEEL {wh} does not exist!")
        SETTINGS["WHEELS"].append(WHEELS[wh])

    wheel_poses = wheel_pos.split(' ')
    for wp in wheel_poses:
        if not wp in ETW:
            raise ArgumentError(f"WHEEL position must be in A-Z!")
        SETTINGS["WHEEL_POS"].append(ord(wp) - ord('A'))
    
    plugboard_setup = plugboard.split(' ')
    for ps in plugboard_setup:
        if not len(ps) == 2 or not ps.isupper():
            raise ArgumentError(f"Each plugboard setting must be sized in 2 and caplitalized; {ps} is invalid")
        SETTINGS["PLUGBOARD"].append(ps)

# Enigma Logics Start

# Plugboard
def pass_plugboard(input):
    for plug in SETTINGS["PLUGBOARD"]:
        if str.startswith(plug, input):
            return plug[1]
        elif str.endswith(plug, input):
            return plug[0]

    return input

# ETW
def pass_etw(input):
    return SETTINGS["ETW"][ord(input) - ord('A')]

# Wheels
def pass_wheels(input, reverse = True):
    # Implement Wheel Logics
    # Keep in mind that reflected signals pass wheels in reverse order
    input = ord(input) - ord('A')
    if(reverse):
        first = ord(SETTINGS["WHEELS"][0]["wire"][(SETTINGS["WHEEL_POS"][0]+input) % 26]) - ord('A')
        second = ord(SETTINGS["WHEELS"][1]["wire"][(SETTINGS["WHEEL_POS"][1]+first) % 26]) - ord('A')
        input = SETTINGS["WHEELS"][2]["wire"][(SETTINGS["WHEEL_POS"][2]+second) % 26]
    else:
        first = ord(SETTINGS["WHEELS"][2]["wire"][(SETTINGS["WHEEL_POS"][2]+input) % 26]) - ord('A')
        second = ord(SETTINGS["WHEELS"][1]["wire"][(SETTINGS["WHEEL_POS"][1]+first) % 26]) - ord('A')
        input = SETTINGS["WHEELS"][0]["wire"][(SETTINGS["WHEEL_POS"][0]+second) % 26]
    
    return input

# UKW
def pass_ukw(input):
    return SETTINGS["UKW"][ord(input) - ord('A')]

# Wheel Rotation
def rotate_wheels():
    # Implement Wheel Rotation Logics
    SETTINGS["WHEEL_POS"][2] += 1
    if(SETTINGS["WHEELS"][2]["turn"] > 0):
        SETTINGS["WHEELS"][2]["turn"] -= 1
    else:
        SETTINGS["WHEELS"][2]["turn"] = SETTINGS["WHEELS"][2]["max"]
        SETTINGS["WHEEL_POS"][1] += 1
        if(SETTINGS["WHEELS"][1]["turn"] > 0):
            SETTINGS["WHEELS"][1]["turn"] -= 1
        else:
            SETTINGS["WHEELS"][1]["turn"] = SETTINGS["WHEELS"][1]["max"]
            SETTINGS["WHEEL_POS"][0] += 1
            if(SETTINGS["WHEELS"][0]["turn"] > 0):
                SETTINGS["WHEELS"][0]["turn"] -= 1
            else:
                SETTINGS["WHEELS"][0]["turn"] = SETTINGS["WHEELS"][0]["max"]
    pass

# Enigma Exec Start
# 암호화 하고 싶은 문장넣기 
plaintext = input("Plaintext to Encode: ")
# 원하는 반사판 넣기 A B C 중 하나 선택
ukw_select = input("Set Reflector (A, B, C): ")
# 왼쪽에서 오른쪽 순서로 3개의 로터판 배치 ex) I II III, II I III, III II I
wheel_select = input("Set Wheel Sequence L->R (I, II, III): ")
wheel_pos_select = input("Set Wheel Position L->R (A~Z): ")
# 원하는 플러그인 만들기 ex) AB, AB DF (두 개의 알파벳을 쌍으로 만든다. 있어도되고 없어도 됨)
plugboard_setup = input("Plugboard Setup: ")

apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)

for ch in plaintext:
    rotate_wheels()

    encoded_ch = ch

    encoded_ch = pass_plugboard(encoded_ch)
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch)
    encoded_ch = pass_ukw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch, reverse = False)
    encoded_ch = pass_plugboard(encoded_ch)

    print(encoded_ch, end='')

