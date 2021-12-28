import tkinter as tk
from typing import List

'''
a general window that by labels present what data is needed as input
'''
class EnterWindow:
    def __init__(self, title: str, labelStart: str, labels: List[str], btnTxt: str):
        self.strRetArr = []
        self.mainWindow = tk.Tk()
        self.mainWindow.title(title)    # set the title of window
        self.textArr = []
        label = tk.Label(self.mainWindow, text=labelStart)  # this is the supporting label that explains what to do
        label.pack()
        for labelStr in labels:
            label = tk.Label(self.mainWindow, text=labelStr)    # for each label reate a label and a text box
            label.pack()
            textbox = tk.Text(self.mainWindow, height=1, width=50)
            textbox.pack()
            self.textArr += [textbox]

        ButtonOk = tk.Button(self.mainWindow, text=btnTxt, command=self.pressButton) # add for button the proper action
        ButtonOk.pack()
        tk.mainloop()

    def pressButton(self):
        self.setTextArray()         # before closing set the text that in the window
        self.mainWindow.destroy()   # close the window
        self.mainWindow.quit()


    def setTextArray(self):
        """
        gather all the text from the textBox and set it to the array
        """
        self.strRetArr = []
        for textbox in self.textArr:
            self.strRetArr += [textbox.get("1.0", "end")]

    def getTextArray(self):
        return self.strRetArr
