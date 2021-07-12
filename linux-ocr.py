from pynput import mouse
from speak import speak
#! /usr/bin/env python3

import sys
import pytesseract
from PIL import Image

last_text = ''



# Draw the area to monitor

print('Drawing area to monitor...')

def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))

def on_click(x, y, button, pressed):
    global start_draw_x
    global start_draw_y
    global stop_draw_x
    global stop_draw_y    

    if pressed:
        start_draw_x = x
        start_draw_y = y        
    else:
        stop_draw_x = x
        stop_draw_y = y
        print(start_draw_x, start_draw_y, stop_draw_x, stop_draw_y)
        # Stop listener
        return False    


# Collect events until released
with mouse.Listener(on_click=on_click,) as listener:
    listener.join()


# End drawing area to monitor    





# Import ImageGrab if possible, might fail on Linux
# try:
#     from PIL import ImageGrab
#     use_grab = True
# except Exception as ex:
    # Some older versions of pillow don't support ImageGrab on Linux
    # In which case we will use XLib 
if ( sys.platform == 'linux' ):
    from Xlib import display, X   
    use_grab = False
else:
    raise ex


def screenGrab( rect ):
    """ Given a rectangle, return a PIL Image of that part of the screen.
        Handles a Linux installation with and older Pillow by falling-back
        to using XLib """
    global use_grab
    x, y, width, height = rect

    if ( use_grab ):
        image = PIL.ImageGrab.grab( bbox=[ x, y, x+width, y+height ] )
    else:
        # ImageGrab can be missing under Linux
        dsp  = display.Display()
        root = dsp.screen().root
        raw_image = root.get_image( x, y, width, height, X.ZPixmap, 0xffffffff )
        image = Image.frombuffer( "RGB", ( width, height ), raw_image.data, "raw", "BGRX", 0, 1 )
        # DEBUG image.save( '/tmp/screen_grab.png', 'PNG' )
    return image




x = start_draw_x
y = start_draw_y
width  = abs(start_draw_x - stop_draw_x)
height= abs(start_draw_y - stop_draw_y)    

# Area of screen to monitor
screen_rect = [ x, y, width, height ]  
print('Watching...')

### Loop forever, monitoring the user-specified rectangle of the screen
while ( True ): 
    image = screenGrab( screen_rect )              # Grab the area of the screen
    text  = pytesseract.image_to_string( image )   # OCR the image

    # IF the OCR found anything, write it to stdout.
    text = text.strip()
    if ( len( text ) > 0 ) and last_text != text:
        last_text = text
        speak( text )
