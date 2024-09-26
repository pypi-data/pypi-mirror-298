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
from ..utn_assets import sound_path
from ..common_variables import VERSION

def colour_text(text: str, message_type: str = '') -> str:
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

def limpiar_pantalla():
    """
    The function `limpiar_pantalla` clears the console screen and waits for user input to continue.
    """
    import os
    _ = input("\nPresiona Enter para continuar...")
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
    message = f'Hello from the UTN community. You are using the UTN_Heroes_Dataset version: {VERSION}'
    print(colour_text(message, 'Info'))
    
