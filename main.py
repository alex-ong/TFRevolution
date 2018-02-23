from Model.Model import Model
from View.View import View
from Controller.Controller import Controller
from tkinter import *
import sys
import asyncio


async def run_tk(view, controller, interval=0.001):
    '''
    Run a tkinter app in an asyncio event loop.
    '''
    try:
        while True:            
            view.update() #update gui
            controller.update() #update controller
            await asyncio.sleep(interval)
    except TclError as e:
        if "application has been destroyed" not in e.args[0]:
            raise


async def main():
    m = Model()
    v = View()
    c = Controller(m, v)
            
    await run_tk(v, c)


if __name__ == "__main__":    
    asyncio.get_event_loop().run_until_complete(main())
