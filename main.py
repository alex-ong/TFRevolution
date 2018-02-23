from Model.Model import Model
from Controller.Controller import Controller
from View.View import View
import asyncio
import tkinter
import time

GUI_REFRESH = 0.001 #a thousand fps.
async def run_tk(view, controller, interval=GUI_REFRESH):
    '''
    Runs the tkinter loop through the asyncio event loop.
    This allows us to use asyncio coroutines, which are good for e.g loading image thumbnails from URL 
    From: https://www.reddit.com/r/Python/comments/33ecpl/neat_discovery_how_to_combine_asyncio_and_tkinter/
    '''    
    try:
        timer = time.perf_counter()
        while True:
            # update gui
            newTime = time.perf_counter()
            delta = newTime - timer            
            
            view.update()      
             
            # update logic if required.
            controller.update(delta)
            
            await asyncio.sleep(interval)
            
            # keep track of deltaTimes for performance debugging
            # print(delta)
            timer = newTime
            
    except tkinter.TclError as e:        
        if "application has been destroyed" not in e.args[0]:
            raise 
        
if __name__ == '__main__':    
    m = Model()
    v = View()
    c = Controller(m,v)
    # run the program!
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_tk(v, c))
