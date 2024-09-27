# Copyright (C) 2024 <UTN FRA>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame.mixer as mixer
import time
from ..utn_assets import sound_path, desafio_1, desafio_2
from ..common_variables import VERSION

def crear_enunciado_desafio_1():
    """
    The function `crear_enunciado_desafio_1` reads the content from a file named `desafio_1` and writes
    it to a new file named `Desafio_01.md`.
    """
    content = ''
    with open(desafio_1, 'r', encoding='utf-8') as file:
        content = file.read()
    with open('./Desafio_01.md', 'w', encoding='utf-8') as file:
        file.write(content)

def crear_enunciado_desafio_2():
    """
    This Python function reads the content of a file named `desafio_2` and writes it to a new file named
    `Desafio_02.md`.
    """
    content = ''
    with open(desafio_2, 'r', encoding='utf-8') as file:
        content = file.read()
    with open('./Desafio_02.md', 'w', encoding='utf-8') as file:
        file.write(content)

def color_text(text: str, message_type: str = '') -> str:
    """
    The function `color_text` takes a text input and a message type, and returns the text formatted
    with color based on the message type.
    
    :param text: The `text` parameter in the `color_text` function is the string that you want to
    colorize based on the `message_type`. It is the main content that will be displayed with the
    specified color and message type
    :type text: str
    :param message_type: The `message_type` parameter in the `color_text` function is used to specify
    the type of message being displayed. It has a default value of an empty string, which means if no
    message type is provided when calling the function, it will default to a general system message
    :type message_type: str
    """
    _b_red: str = '\033[41m'
    _b_green: str = '\033[42m'
    _b_blue: str = '\033[44m'
    _f_white: str = '\033[37m'
    _no_color: str = '\033[0m'
    message_type = message_type.strip().capitalize()
    match message_type:
        case 'Error':
            text =  f'{_b_red}{_f_white}> Error: {text}{_no_color}'
        case 'Success':
            text = f'{_b_green}{_f_white}> Success: {text}{_no_color}'
        case 'Info':
            text = f'{_b_blue}{_f_white}> Information: {text}{_no_color}'
        case _:
            text =  f'{_b_red}{_f_white}> System: {text}{_no_color}'

    return text

def clear_console():
    """
    The function `clear_console` clears the console screen and prompts the user to press Enter to
    continue.
    """
    import os
    _ = input(color_text("\nPresiona Enter para continuar..."))
    os.system('cls' if os.name in ['nt', 'dos'] else 'clear')

def play_sound():
    """
    The `play_sound` function initializes the mixer, loads a sound file, sets the volume to 0.4, and
    plays the sound.
    """
    mixer.init()
    mixer.music.load(sound_path)
    mixer.music.set_volume(0.4)
    mixer.music.play()
    time.sleep(0.4)

def saludo():
    """
    The function `saludo()` prints a greeting message with information about the UTN community and
    dataset version.
    """
    play_sound()
    message = f'Hello from the UTN community. You are using the UTN_Heroes_Dataset version: {VERSION}'
    print(color_text(message, 'Info'))
    
