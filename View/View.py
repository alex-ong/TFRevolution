import tkinter as tk
from tkinter import Label, Button

class View(tk.Frame):
            
    def __init__(self):        
        root = tk.Tk()        
        root.config(bg='blue')
        super().__init__(root)                
        root.focus_force()             
        root.wm_title("UNSW Revue Statics")
        Label(self, text='Print').pack()
        Label(self, text='Print').pack()
        Label(self, text='Print').pack()
        Label(self, text='Print').pack()
        Label(self, text='Print').pack()
        
        self.pack()
        
        self.root = root


if __name__ == '__main__':
    v = View()
    v.master.mainloop()