# utils/get_user_input.py
import threading
import queue
import pygame

_input_queue = queue.Queue()

def _input_thread(prompt: str):
    try:
        user_input = input(prompt)
        _input_queue.put(user_input)
    except EOFError:
        _input_queue.put("")

def get_user_input(prompt: str = "") -> str:
    input_thread = threading.Thread(target=_input_thread, args=(prompt,), daemon=True)
    input_thread.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if not _input_queue.empty():
            return _input_queue.get()
