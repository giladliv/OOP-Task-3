import tkinter as tk
from typing import List


class EnterWindow:
    def __init__(self, title: str, labelStart: str, labels: List[str], btnTxt: str):
        self.strRetArr = []
        self.mainWindow = tk.Tk()
        self.mainWindow.title(title)
        self.textArr = []
        label = tk.Label(self.mainWindow, text=labelStart)
        label.pack()
        for labelStr in labels:
            label = tk.Label(self.mainWindow, text=labelStr)
            label.pack()
            textbox = tk.Text(self.mainWindow, height=1, width=50)
            textbox.pack()
            self.textArr += [textbox]

        ButtonOk = tk.Button(self.mainWindow, text=btnTxt, command=self.pressButton)
        ButtonOk.pack()
        tk.mainloop()

    def pressButton(self):
        self.setTextArray()
        self.mainWindow.destroy()
        self.mainWindow.quit()


    def setTextArray(self):
        self.strRetArr = []
        for textbox in self.textArr:
            self.strRetArr += [textbox.get("1.0", "end")]

    def getTextArray(self):
        return self.strRetArr



#window = EnterWindow("Enter Edge", ["src", "dest", "w"], "press to enter")
#print(window.getTextArray())