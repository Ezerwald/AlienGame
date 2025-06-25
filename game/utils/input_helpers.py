import threading
import queue
import pygame
import os
import platform

_input_queue = queue.Queue()

def _input_thread(prompt: str):
    try:
        user_input = input(prompt)
        _input_queue.put(user_input)
    except EOFError:
        _input_queue.put("")

def clear_terminal():
    # Cross-platform terminal clear
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def get_user_input(prompt: str = "") -> str:
    input_thread = threading.Thread(target=_input_thread, args=(prompt,), daemon=True)
    input_thread.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if not _input_queue.empty():
            user_input = _input_queue.get()
            clear_terminal()  # Clear screen after input is received
            return user_input
