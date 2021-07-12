from subprocess import call

def speak(text_to_speak, speed=270):
    call(["espeak",f"-s{speed} -ven+18 -z",text_to_speak])
