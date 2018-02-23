from tkinter import *
import asyncio

async def run_tk(root, interval=0.05):
    '''
    Run a tkinter app in an asyncio event loop.
    '''
    try:
        while True:
            root.update()
            await asyncio.sleep(interval)
    except TclError as e:
        if "application has been destroyed" not in e.args[0]:
            raise


async def main():
    root = Tk()
    entry = Entry(root)
    entry.grid()
    
    Button(root, text='Connect').grid()
    
    await run_tk(root)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
