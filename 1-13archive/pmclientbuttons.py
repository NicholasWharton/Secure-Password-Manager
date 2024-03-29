# Nicholas Wharton
# Secure Password Manager
# Client GUI Buttons Trigger Functions
# 1/13/2024

def button1Set(buttonVar, twoVar, window):
    buttonVar.set(True)
    twoVar.set(True)
    window.destroy()

def button2Set(buttonVar, twoVar, window):
    buttonVar.set(True)
    twoVar.set(False)
    window.destroy()

def button3Set(exitVar, buttonVar, window):
    buttonVar.set(True)
    exitVar.set(True)
    window.destroy()

def processInfo(buttonVar):
    buttonVar.set(True)

def button4Set(exitVar, buttonVar, window):
    buttonVar.set(True)
    exitVar.set(True)

def sub(val, buttonVar, window):
    window.destroy()
    buttonVar.set(val)

def processInfo5(buttonVar, window):
    buttonVar.set(True)

def noButton(buttonVar, val, window, exitVar):
    buttonVar.set(val)
    exitVar.set(True)
    window.destroy()
