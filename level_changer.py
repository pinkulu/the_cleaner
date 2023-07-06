import tkinter as tk
from os import path
import json
import math

levels = {
    1: (162.3625946044922, 178.3443603515625, 217.66067504882813),
    2: (-1011.767578125, 725.152099609375, 267.6816101074219),
    3: (-464.43634033203127, 553.7214965820313, 85.67933654785156),
    4: (-555.169921875, 1994.755126953125, 2217.8916015625),
    5: (-779.4521484375, 1241.153564453125, -1026.638671875),
    6: (-741.6983032226563, 812.0296020507813, -750.4246215820313),
    7: (-521.1273803710938, 942.5263061523438, -739.1165161132813)
}


def read_save():
    file = path.join(path.expanduser('~'), "AppData", "LocalLow", "Dystopia Corp", "The Cleaner", "Save.dat")
    with open(file, "rb") as f:
        data = f.read()
        data = data.decode("utf-8")
        data = json.loads(data)
    print(data)
    return data


def get_level():
    data = read_save()
    position = data["data"]["position"]

    closest_level = None
    min_distance = float('inf')

    for level, pos in levels.items():
        distance = math.sqrt(
            (position["x"] - pos[0]) ** 2 + (position["y"] - pos[1]) ** 2 + (position["z"] - pos[2]) ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_level = level

    return closest_level


def set_level(lvl):
    file = path.join(path.expanduser('~'), "AppData", "LocalLow", "Dystopia Corp", "The Cleaner", "Save.dat")
    with open(file, "rb") as f:
        data = f.read()
        data = data.decode("utf-8")
        data = json.loads(data)
    position = data["data"]["position"]

    if lvl in levels:
        pos = levels[lvl]
        position["x"] = pos[0]
        position["y"] = pos[1]
        position["z"] = pos[2]
    else:
        return 0

    data["data"]["position"] = position
    data = json.dumps(data)
    data = data.encode("utf-8")
    with open(file, "wb") as f:
        f.write(data)
    lvl_label.config(text="Level: " + str(get_level()))


root = tk.Tk()
root.title("The Cleaner Level Changer")
root.geometry("300x300")

lvl_label = tk.Label(root, text="Level: " + str(get_level()))
lvl_label.pack()

for i in range(1, len(levels) + 1):
    tk.Button(root, text="Level " + str(i), command=lambda i=i: set_level(i)).pack()

root.mainloop()
