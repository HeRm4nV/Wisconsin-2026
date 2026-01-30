#!/usr/bin/env python3.11
# coding=utf-8

"""
tested in Python 3.11
"""
# ==============================
# Wisconsin Experiment Script
# Python Version: 3.11
# ==============================

# ==============================
# Imports
# ==============================
import pygame, sys, serial, zipfile
from random import shuffle, randint
from pathlib import Path
from datetime import datetime
from tempfile import TemporaryDirectory

from time import strftime, gmtime
from pygame.locals import (
    FULLSCREEN,
    USEREVENT,
    KEYUP,
    K_SPACE,
    K_RETURN,
    K_ESCAPE,
    QUIT,
    Color,
    K_c,
    K_v,
    K_b,
    K_n,
    K_p
)

# ==============================
# Global Paths & Configuration
# ==============================

# Debug flag:
# - If True: print information and save intermediate files
# - If False: silent execution, minimal output
debug = False

# Base directory of the script
BASE_DIR = Path(__file__).resolve().parent

# Data directory where debug files and logs will be stored
DATA_DIR = BASE_DIR / "data"

DEBUG_DIR = BASE_DIR / "debug_data"
DEBUG_DIR.mkdir(exist_ok=True)

FullScreenShow = True  # Automatically start in fullscreen mode
test_name = "Wisconsin Task"
date_name = strftime("%Y-%m-%d_%H-%M-%S", gmtime())

# Port address and triggers
lpt_address = 0xD100
trigger_latency = 5
start_trigger = 254
stop_trigger = 255

trigger_helper = {
    "fixation": 1,
    "1": 11,
    "2": 12,
    "3": 21,
    "4": 22,
    "correct_response": 100,
    "incorrect_response": 200,
    "no_response": 250,
    "start_block_1": 51,
    "start_block_2": 52,
    "neutral_stimulus": 30
}

# Global Variables

base_images_loaded = False
base_images_list = []
type_orders = ["number", "figure", "color"]

# ==============================
# Experiment Metadata
# ==============================

EXPERIMENT_NAME = "Wisconsin_Experiment"
EXPERIMENT_VERSION = "0.1"
PYTHON_VERSION = "3.11"

# Timestamp used for file naming and session identification
SESSION_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# ==============================
# Deck Configuration
# ==============================

DECK_SIZE = 60
TOTAL_BLOCKS = 4
TRIALS_PER_BLOCK = 105
SERIES_DISTRIBUTION = {
    6: 5,   # five series of size 6
    7: 5,   # five series of size 7
    8: 5    # five series of size 8
}

# ==============================
# Define deck sizes per block
# ==============================
deck_sizes_per_block = [
    [60, 45],          # Block 1
    [15, 60, 30],      # Block 2
    [30, 60, 15],      # Block 3
    [45, 60]           # Block 4
]

# ==============================
# Exceptions
# ==============================

class TextRectException(Exception):
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message
    
# ==============================
# Image Loading
# ==============================

def load_images_from_folder(folder_path):
    """
    Loads all image files from a given folder.

    Parameters:
        folder_path (Path): Absolute path to the image folder

    Returns:
        list: List of Path objects pointing to image files
    """
    if not folder_path.exists():
        raise FileNotFoundError(f"Image folder not found: {folder_path}")

    images = [p for p in folder_path.iterdir() if p.is_file()]

    if debug:
        print(f"[DEBUG] Loaded {len(images)} images from {folder_path}")

    return images

# Base image directories
single_cards_dir = BASE_DIR / "media" / "images" / "Single"
double_cards_dir = BASE_DIR / "media" / "images" / "Double"
static_cards_dir = BASE_DIR / "media" / "images" / "Static"

# Load images
single_images_list = load_images_from_folder(single_cards_dir)
double_images_list = load_images_from_folder(double_cards_dir)
static_images_list = load_images_from_folder(static_cards_dir)

# Shuffle only dynamic decks
shuffle(single_images_list)
shuffle(double_images_list)

# ==============================
# Deck Control
# ==============================

class DeckCursor:
    """
    Cursor for managing the decks of Cards and Doubles.
    Handles pools of Cards and Doubles for a block.
    """
    def __init__(self, singles_list, doubles_list):
        self.original_singles = singles_list.copy()      # 24 cards
        self.original_doubles = doubles_list.copy()  # 36 doubles

        # Current pool for this block
        self.singles_pool = self.original_singles.copy()
        self.doubles_pool = self.original_doubles.copy()

    def next_card(self, card_type):
        """
        Return the next card from the pool.
        """
        if card_type == "Singles":
            if not self.singles_pool:
                raise RuntimeError("No more Singles available")
            return self.singles_pool.pop(0)
        elif card_type == "Doubles":
            if not self.doubles_pool:
                raise RuntimeError("No more Doubles available")
            return self.doubles_pool.pop(0)
        else:
            raise ValueError(f"Unknown card type: {card_type}")

# ==============================
# Deck Creation
# ==============================

def build_deck_plan(series_sizes, deck_sizes):
    # ==============================
    # Build deck consumption plan
    # ==============================
    deck_plan = []

    current_series_index = 0
    remaining_in_series = series_sizes[0]

    for deck_index, deck_size in enumerate(deck_sizes):
        remaining_in_deck = deck_size
        series_usage = []

        from_series = current_series_index

        # ==============================
        # Consume this deck across series
        # ==============================
        while remaining_in_deck > 0:
            use_now = min(remaining_in_series, remaining_in_deck)

            series_usage.append({
                "series_index": current_series_index,
                "used_slots": use_now
            })

            remaining_in_series -= use_now
            remaining_in_deck -= use_now

            # ==============================
            # Move to next series if needed
            # ==============================
            if remaining_in_series == 0:
                current_series_index += 1
                if current_series_index < len(series_sizes):
                    remaining_in_series = series_sizes[current_series_index]

        to_series = series_usage[-1]["series_index"]

        deck_plan.append({
            "deck_index": deck_index,
            "deck_size": deck_size,
            "from_series": from_series,
            "to_series": to_series,
            "series_usage": series_usage
        })

    # ==============================
    # Final validation
    # ==============================
    total_used = sum(
        usage["used_slots"]
        for deck in deck_plan
        for usage in deck["series_usage"]
    )

    if total_used != sum(series_sizes):
        raise RuntimeError("Deck plan does not fully cover series sizes")

    return deck_plan

# ==============================
# EEG / Trigger Functions
# ==============================

def init_lpt(address):
    """Creates and tests a parallel port connection."""
    try:
        from ctypes import windll
        global io
        io = windll.dlportio  # requires dlportio.dll
        print('Parallel port opened')
    except Exception:
        print("Parallel port could not be opened")

    try:
        io.DlPortWritePortUchar(address, 0)
        print('Parallel port initialized to zero')
    except Exception:
        print('Failed to send initial zero trigger')

def send_trigger(trigger, address, latency):
    """Sends a trigger to the parallel port."""
    try:
        io.DlPortWritePortUchar(address, trigger)
        pygame.time.delay(latency)
        io.DlPortWritePortUchar(address, 0)
        print(f'Trigger {trigger} sent')
    except Exception:
        print(f'Failed to send trigger {trigger}')

def init_com(address="COM3"):
    """Initializes a serial port connection."""
    global ser
    try:
        ser = serial.Serial()
        ser.port = address
        ser.baudrate = 115200
        ser.open()
        print('Serial port opened')
    except Exception:
        print('Serial port could not be opened')

def send_triggert(trigger):
    """Sends a trigger via serial port."""
    try:
        ser.write((trigger).to_bytes(1, 'little'))
        print(f'Trigger {trigger} sent')
    except Exception:
        print(f'Failed to send trigger {trigger}')

def sleepy_trigger(trigger, latency=100):
    send_triggert(trigger)
    pygame.time.wait(latency)

def close_com():
    """Closes the serial port."""
    try:
        ser.close()
        print('Serial port closed')
    except Exception:
        print('Serial port could not be closed')

# ==============================
# Text & Screen Functions
# ==============================

def select_slide(slide_name, variables=None):
    """
    Returns the text content for a given instruction slide.
    """

    if variables is None:
        variables = {"blockNumber": 0, "practice": False}

    basic_slides = {
        'welcome': [
            u"Bienvenido/a, a este experimento!!!",
            " ",
            u"Se te indicará paso a paso que hacer."
        ],
        'instructions': [
            u"¡Bienvenida/o! Este experimento consta de cuatro bloques con",
            u"descansos de 2 a 3 minutos entre ellos. Durante las pausas aparecerá el",
            u"mensaje “Fin del bloque X”, y deberás esperar la indicación para continuar.",
            "",
            u"En cada ensayo, deberás emparejar la carta central con una de las",
            u"cuatro cartas de referencia ubicadas en la parte superior. La selección",
            u"se basa en una regla que puede ser color, forma o número, la cual no",
            u"se indicará y puede cambiar sin previo aviso.",
            "",
            u"Tras cada respuesta, recibirás retroalimentación de “Correcto” o",
            u"“Incorrecto”, que deberás usar para inferir la regla vigente.",
            "",
            u"Para responder, presiona la tecla correspondiente según la posición",
            u"de la carta de referencia de izquierda a derecha:",
            u"C (triángulo rojo), V (dos estrellas verdes),",
            u"B (tres cruces amarillas) y N (cuatro círculos azules).",
            "",
            u"Responde lo más rápido posible."
        ],
        'Break': [
            u"Fin del bloque " + str(variables["blockNumber"]) + ".",
            " ",
            u"Tómate de 2 a 3 minutos para descansar.",
            " ",
            u"Cuando estés lista/o para continuar presiona la barra espaciadora."
        ],
        'farewell': [
            u"La tarea ha finalizado.",
            "",
            u"Muchas gracias por su colaboración!!"
        ]
    }

    return basic_slides[slide_name]

def setfonts():
    """Initializes font objects."""
    global bigchar, char, charnext
    pygame.font.init()
    font_path = BASE_DIR / "media" / "Arial_Rounded_MT_Bold.ttf"
    bigchar = pygame.font.Font(font_path, 96)
    char = pygame.font.Font(font_path, 32)
    charnext = pygame.font.Font(font_path, 24)

def paragraph(text, key=None, no_foot=False, color=None, limit_time=0,
              row=None, is_clean=True):
    """Displays text as a formatted paragraph on screen."""

    if is_clean:
        screen.fill(background)

    if isinstance(text, str):
        text = [text]

    if row is None:
        row = center[1] - 20 * len(text)

    if color is None:
        color = char_color

    if debug:
        print(text)

    for line in text:
        phrase = char.render(line, True, color)
        phrasebox = phrase.get_rect(centerx=center[0], top=row)
        screen.blit(phrase, phrasebox)
        row += 40

    if key is not None:
        if key == K_SPACE:
            foot = u"Para continuar presione la tecla Espacio..."
        elif key == K_RETURN:
            foot = u"Para continuar presione la tecla ENTER..."
    else:
        foot = u"Responda con la fila superior de teclas de numéricas"

    if no_foot:
        foot = ""

    nextpage = charnext.render(foot, True, charnext_color)
    nextbox = nextpage.get_rect(left=15, bottom=resolution[1] - 15)
    screen.blit(nextpage, nextbox)
    pygame.display.flip()

    if key is not None or limit_time != 0:
        wait(key, limit_time)

# ==============================
# Program Control Functions
# ==============================

def init():
    """Initializes pygame display and core variables."""
    setfonts()

    global screen, resolution, center, background
    global char_color, charnext_color, fix, fixbox

    pygame.init()
    pygame.display.init()
    pygame.display.set_caption(test_name)
    pygame.mouse.set_visible(False)

    if FullScreenShow:
        resolution = (pygame.display.Info().current_w,
                      pygame.display.Info().current_h)
        screen = pygame.display.set_mode(resolution, FULLSCREEN)
    else:
        try:
            resolution = pygame.display.list_modes()[3]
        except Exception:
            resolution = (1280, 720)
        screen = pygame.display.set_mode(resolution)

    center = (resolution[0] // 2, resolution[1] // 2)
    background = Color('lightgray')
    char_color = Color('black')
    charnext_color = Color('black')

    fix = char.render('+', True, char_color)
    fixbox = fix.get_rect(center=center)

    screen.fill(background)
    pygame.display.flip()

def blackscreen(blacktime=0):
    """Clears the screen."""
    screen.fill(background)
    pygame.display.flip()
    pygame.time.delay(blacktime)

def ends():
    """Ends the experiment safely."""
    blackscreen()
    dot = char.render('.', True, char_color)
    dotbox = dot.get_rect(left=15, bottom=resolution[1] - 15)
    screen.blit(dot, dotbox)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == KEYUP and event.key == K_ESCAPE:
                pygame_exit()

def pygame_exit():
    pygame.quit()
    sys.exit()

# ==============================
# Protocol Handler Functions
# ==============================

def draw_cross(color, center, size, thickness=16):
    x, y = center
    half = size // 2
    pygame.draw.line(screen, color, (x - half, y - half), (x + half, y + half), thickness)
    pygame.draw.line(screen, color, (x - half, y + half), (x + half, y - half), thickness)


def draw_check(color, center, size, thickness=16):
    x, y = center
    pygame.draw.line(
        screen, color,
        (x - size // 2, y),
        (x - size // 6, y + size // 2),
        thickness
    )
    pygame.draw.line(
        screen, color,
        (x - size // 6, y + size // 2),
        (x + size // 2, y - size // 2),
        thickness
    )

def wait(key, limit_time):
    """Waits for a key press or a timeout."""

    TIME_OUT_WAIT = USEREVENT + 1

    if limit_time != 0:
        pygame.time.set_timer(TIME_OUT_WAIT, limit_time, loops=1)

    start_time = pygame.time.get_ticks()
    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame_exit()

            elif event.type == KEYUP:
                if event.key == key:
                    waiting = False

            elif event.type == TIME_OUT_WAIT and limit_time != 0:
                waiting = False

    pygame.time.set_timer(TIME_OUT_WAIT, 0)
    pygame.event.clear()  # CLEAR EVENTS

    return pygame.time.get_ticks() - start_time

def wait_answer(image, series_type):
    """Waits for a response from the user and returns the answer details."""

    answer_keys = {
        K_c: 0,
        K_v: 1,
        K_b: 2,
        K_n: 3
    }

    correct_answer = type_orders.index(series_type)
    selected_answer = None
    rt = None
    waiting = True
    start_time = pygame.time.get_ticks()

    
    print(static_images_list)
    
    print(series_type)
    print(correct_answer)
    print("--------------------")

    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame_exit()

            elif event.type == KEYUP:
                if event.key in answer_keys:
                    selected_answer = answer_keys[event.key]
                    rt = pygame.time.get_ticks() - start_time

                    if static_images_list[answer_keys[event.key]].parts[-1].split('.')[0].split('_')[correct_answer] == image.parts[-1].split(".")[0].split('_')[correct_answer]:
                        is_correct = True
                    else:
                        is_correct = False

                    waiting = False

    return {'selected_answer': selected_answer,
            'is_correct': is_correct,
            'rt': rt,}

def show_image_trial(image, scale):
    global base_images_loaded, base_images_list
    screen.fill(background)
    try:
        picture = pygame.image.load(image)
        if not base_images_loaded:
            for actual_image in static_images_list:
                base_images_list.append(pygame.image.load(actual_image))
            base_images_loaded = True
    except pygame.error as e:
        print(f"Error al cargar imagen {image}: {e}") if debug else None
        return
    
    image_real_size = picture.get_size()
    percentage = scale / image_real_size[0]
    picture = pygame.transform.scale(picture, [int(scale), int(image_real_size[1]*percentage)])

    center = [int(resolution[0] / 2), int(resolution[1] / 4)*3]

    # show all 4 base images in the top part of the screen
    for count, base_image in enumerate(base_images_list):
        base_image_scaled = pygame.transform.scale(base_image, [int(scale), int(image_real_size[1]*percentage)])
        base_center = [int(resolution[0] / 8 + count * (resolution[0] / 4)), int(resolution[1] / 8)*2]
        screen.blit(base_image_scaled, [base_center[0] - base_image_scaled.get_size()[0]/2, base_center[1] - base_image_scaled.get_size()[1]/2])

    screen.blit(picture, [x - picture.get_size()[count]/2 for count, x in enumerate(center)])
    pygame.display.flip()

def show_images(image_list, uid=None, dfile=None, block=None, series_types=None):

    phase_change = USEREVENT + 2

    done = False
    image_count = -1
    serie_count = 0

    starting_block = True

    screen.fill(background)
    screen.blit(fix, fixbox)
    pygame.display.update(fixbox)
    pygame.display.flip()
    pygame.time.set_timer(phase_change, 600, loops=1)

    answers_list = []

    actual_phase = 2

    while not done:
        for event in pygame.event.get():
            if event.type == KEYUP and event.key == K_ESCAPE and debug:
                pygame_exit()

            elif event.type == KEYUP and event.key == K_p and debug:
                done = True

            elif event.type == phase_change:
                if actual_phase == 1: # Fixation Phase
                    screen.fill(background)
                    screen.blit(fix, fixbox)
                    pygame.display.update(fixbox)
                    pygame.display.flip()
                    sleepy_trigger(1, trigger_latency)
                    if starting_block:
                        pygame.time.set_timer(phase_change, 600, loops=1)
                        starting_block = False
                    else:
                        pygame.time.set_timer(phase_change, randint(1500, 2000), loops=1)
                    actual_phase = 2
                elif actual_phase == 2: # Target Card Presentation Phase
                    image_count += 1
                    if image_list[serie_count]["serie_size"] <= image_count:
                        image_count = 0
                        serie_count += 1
                        if serie_count >= len(image_list):
                            done = True
                            break
                    
                    show_image_trial(image_list[serie_count]["order"][image_count], 300)
                    sleepy_trigger(trigger_helper["1"], trigger_latency)  # Exposure image trigger first
                    actual_phase = 3
                    print(serie_count, image_count)
                elif actual_phase == 3: # Wait for answer phase
                    answer = wait_answer(image_list[serie_count]["order"][image_count], series_types[serie_count])
                    answers_list.append([image_list[serie_count]["order"][image_count], answer, series_types[serie_count]])

                    # Lanzamiento de trigger según la respuesta
                    if answer['is_correct']:
                        sleepy_trigger(trigger_helper["correct_response"], trigger_latency)
                    else:
                        sleepy_trigger(trigger_helper["incorrect_response"], trigger_latency)
                    
                    screen.fill(background)
                    
                    if answer['is_correct']:
                        draw_check((0, 200, 0), center, 120)
                    else:
                        draw_cross((200, 0, 0), center, 120)

                    pygame.display.flip()
                    pygame.time.set_timer(phase_change, 1500, loops=1)
                    actual_phase = 1

    pygame.time.set_timer(phase_change, 0)

    pygame.event.clear()                    # CLEAR EVENTS

    # acá se almacenará la answers_list en el archivo dfile
    if dfile is not None:
        for answer in answers_list:
            # Unir la lista con guiones en lugar de comas
            dfile.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (uid,
                                                    (Path(answer[0][0]).relative_to(script_path)).parts[-1].split('.')[0],
                                                    block,
                                                    answer[1]['rt'],
                                                    (Path(answer[0][0]).relative_to(script_path)).parts[2],
                                                    answer[0][1],
                                                    "Cara" if block == 1 else "Palabra",
                                                    answer[1]['selected_answer'],
                                                    int(answer[1]['is_correct']) if answer[1]['is_correct'] is not None else ""
                                                 ))
            #("Sujeto", "IdImagen", "Bloque", "TReaccion", "TipoImagen", "Palabra", "TipoRespuesta", "Respuesta", "Acierto"))
        dfile.flush()
    else:
        print("Error al cargar el archivo de datos")

# ==============================
# Block / Series Generation
# ==============================

def initialize_series(series_stacks, cut, deck_cursor):
    """
    Initialize series for a given cut using DeckCursor.
    1) Reserve only the proportional singles and doubles needed for this cut.
    2) Add 2 mandatory singles to empty series within cut.
    3) Mix remaining singles with doubles and fill the series.
    4) Return leftover singles and doubles for the next mazo.

    Args:
        series_stacks (list of dict): Series data structures.
        cut (dict): Current deck cut plan with from_series, to_series, and deck_size.
        deck_cursor (DeckCursor): Cursor managing singles and doubles for the block.

    Returns:
        leftover_singles (list), leftover_doubles (list): cards not used in this mazo
    """
    from_series = cut["from_series"]
    to_series = cut["to_series"]
    deck_size_to_use = cut["deck_size"]  # how many cards we will actually use in this cut

    # ==============================
    # Step 0: Determine proportional singles and doubles for this cut
    # ==============================
    total_singles_in_cursor = len(deck_cursor.singles_pool)
    total_doubles_in_cursor = len(deck_cursor.doubles_pool)
    total_cards_in_cursor = total_singles_in_cursor + total_doubles_in_cursor

    if deck_size_to_use > total_cards_in_cursor:
        raise RuntimeError(
            f"Deck size to use ({deck_size_to_use}) exceeds available cards ({total_cards_in_cursor})"
        )

    # Calculate proportional singles and doubles
    singles_to_use = round(deck_size_to_use * total_singles_in_cursor / total_cards_in_cursor)
    doubles_to_use = deck_size_to_use - singles_to_use

    # Take only the needed cards for this cut
    current_singles = deck_cursor.singles_pool[:singles_to_use]
    deck_cursor.singles_pool = deck_cursor.singles_pool[singles_to_use:]  # leftovers

    current_doubles = deck_cursor.doubles_pool[:doubles_to_use]
    deck_cursor.doubles_pool = deck_cursor.doubles_pool[doubles_to_use:]  # leftovers

    # ==============================
    # Step 1: Add 2 mandatory singles to each empty series in the cut
    # ==============================
    for serie_index in range(from_series, to_series + 1):
        serie = series_stacks[serie_index]
        if not serie["initialized"]:
            for _ in range(2):
                if not current_singles:
                    raise RuntimeError("Not enough Singles for mandatory 2 per series")
                serie["order"].append(current_singles.pop(0))
            serie["initialized"] = True

    # ==============================
    # Step 2: Mix remaining singles with doubles and fill series
    # ==============================
    deck_pool = current_singles + current_doubles
    shuffle(deck_pool)

    for serie_index in range(from_series, to_series + 1):
        serie = series_stacks[serie_index]
        slots_left = serie["serie_size"] - len(serie["order"])
        if slots_left > 0:
            to_add = deck_pool[:slots_left]
            serie["order"].extend(to_add)
            deck_pool = deck_pool[slots_left:]

    # ==============================
    # Step 3: Return leftover cards for next mazo
    # These are the cards that were reserved at the start but not used
    # in this cut (deck_cursor pools already reduced)
    # ==============================
    leftover_singles = deck_cursor.singles_pool
    leftover_doubles = deck_cursor.doubles_pool

    return leftover_singles, leftover_doubles

def block_creation():

    # Final array of series stacks for all blocks
    list_of_all_blocks_series_stacks = []

    # ==============================
    # Validate deck sizes
    # ==============================
    for block_index, deck_sizes in enumerate(deck_sizes_per_block):
        if sum(deck_sizes) != 105:
            raise RuntimeError(
                f"Invalid deck sizes in block {block_index + 1}: "
                f"sum is {sum(deck_sizes)}, expected 105"
            )

    # ==============================
    # Generate series sizes per block
    # ==============================
    series_sizes_per_block = []
    for _ in range(4):
        sizes = [6] * 5 + [7] * 5 + [8] * 5
        shuffle(sizes)
        series_sizes_per_block.append(sizes)

    # ==============================
    # Build deck cut plans per block
    # ==============================
    all_blocks_deck_plans = []
    for block_index in range(4):
        deck_plan = build_deck_plan(
            series_sizes=series_sizes_per_block[block_index],
            deck_sizes=deck_sizes_per_block[block_index]
        )
        all_blocks_deck_plans.append(deck_plan)

    # ==============================
    # Process blocks: build series stacks with multiple mazos
    # ==============================
    leftover_singles = []
    leftover_doubles = []

    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # ==============================
        # Write debug_blocks_structure.txt inside temp folder
        # ==============================
        structure_file_path = temp_path / "debug_blocks_structure.txt"
        with open(structure_file_path, "w", encoding="utf-8") as f:
            f.write("Global Blocks Structure\n\n")
            for block_index in range(4):
                f.write(f"Estructura del bloque {block_index + 1}\n\n")
                series_sizes = series_sizes_per_block[block_index]
                deck_plan = all_blocks_deck_plans[block_index]

                for serie_index, serie_size in enumerate(series_sizes):
                    f.write(f"Serie {serie_index + 1}: Tamaño {serie_size}\n")

                f.write("Distribución de mazos:\n")
                for cut in deck_plan:
                    f.write(
                        f"  Mazo {cut['deck_index'] + 1} "
                        f"(tamaño {cut['deck_size']}): "
                        f"series {cut['from_series'] + 1} "
                        f"a {cut['to_series'] + 1}\n"
                    )
                    for usage in cut["series_usage"]:
                        used_slots = usage["used_slots"]
                        if used_slots > 0:
                            f.write(
                                f"    Serie {usage['series_index'] + 1}: "
                                f"usa {used_slots} slots\n"
                            )
                f.write("\n")

        # ==============================
        # Process each block
        # ==============================
        for block_index in range(4):
            series_sizes = series_sizes_per_block[block_index]
            deck_plan = all_blocks_deck_plans[block_index]

            # Initialize empty series stacks
            series_stacks = [
                {"serie_index": i, "serie_size": size, "order": [], "initialized": False}
                for i, size in enumerate(series_sizes)
            ]

            # Process each deck cut (mazo)
            for cut in deck_plan:
                if leftover_singles or leftover_doubles:
                    deck_cursor = DeckCursor(leftover_singles, leftover_doubles)
                    leftover_singles = []
                    leftover_doubles = []
                else:
                    deck_cursor = DeckCursor(single_images_list, double_images_list)

                leftover_singles, leftover_doubles = initialize_series(
                    series_stacks, cut, deck_cursor
                )

                # Debug print
                if debug:
                    print(f"[DEBUG] Bloque {block_index + 1}, Mazo {cut['deck_index'] + 1} procesado.")

            # Write debug file for this block inside temp folder
            block_file_path = temp_path / f"debug_block_{block_index + 1}.txt"
            with open(block_file_path, "w", encoding="utf-8") as f:
                f.write(f"Estructura final del bloque {block_index + 1}\n\n")
                for serie in series_stacks:
                    f.write(f"Serie {serie['serie_index'] + 1} (tamaño {serie['serie_size']}):\n")
                    for img in serie["order"]:
                        f.write(f"  {img}\n")
                    f.write("\n")

            list_of_all_blocks_series_stacks.append(series_stacks)

        # ==============================
        # Create ZIP in DEBUG_DIR
        # ==============================
        zip_name = DEBUG_DIR / f"debug_blocks_{date_name}.zip"
        create_debug_zip(temp_path, zip_name)

        return list_of_all_blocks_series_stacks
    
def generate_series_types_for_block():
    """
    Generate the ordered list of series types for a block.

    Rules:
    - There are 3 types: "number", "color", "figure".
    - Each block has 15 series total (5 iterations of the 3 types).
    - Each iteration shuffles the 3 types.
    - The first element of a new iteration cannot be equal to
      the last element already added to the global list.

    Returns:
        list[str]: A list of 15 elements with balanced and ordered types.
    """
    base_types = ["number", "color", "figure"]
    final_types = []

    for _ in range(5):
        current_types = base_types.copy()
        shuffle(current_types)

        # Ensure no boundary repetition with previous block
        if final_types:
            while current_types[0] == final_types[-1]:
                shuffle(current_types)

        final_types.extend(current_types)

    return final_types

# ==============================
# Debug Validation
# ==============================

def create_debug_zip(debug_base_dir, zip_name, debug=True):

    debug_base_dir = Path(debug_base_dir)
    zip_path = debug_base_dir / zip_name

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in debug_base_dir.glob("*.txt"):
            zipf.write(file_path, arcname=file_path.name)
            if debug:
                print(f"[DEBUG] Added {file_path.name} to {zip_name}")

    if debug:
        print(f"[DEBUG] Debug ZIP created at: {zip_path}")

# ==============================
# Main
# ==============================

def main():

    init()

    # if not media folders exist, exit
    if not single_cards_dir.exists() or not double_cards_dir.exists():
        print("Media folders not found. Please ensure the 'media/images/Single' and 'media/images/Double' directories exist.")
        return

    # Block series stacks generation and debug files
    block_stacks = block_creation()
    
    send_triggert(start_trigger)

    paragraph(select_slide('instructions'), key = K_SPACE, no_foot = False)

    for block_number, block in enumerate(block_stacks):
        series_types = generate_series_types_for_block()
        show_images(block, uid="TestSubject", dfile=None, block=block_number + 1, series_types=series_types)

        # if not the last block, show break screen
        if block_number < len(block_stacks) - 1:
            paragraph(select_slide('break', variables={"blockNumber": block_number, "practice": False}), key = K_SPACE, no_foot = False)

    paragraph(select_slide('farewell'), key = None, no_foot = True)
    close_com()
    ends()


if __name__ == "__main__":
    main()