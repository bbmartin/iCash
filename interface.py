import pygame, engine

# Initializes the font module of pygame
pygame.font.init()

# Constants used for quick editing

## Title of the game
GAME_TITLE = "ICA$H"

## Dimensions of the game screen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

## File path to the font file
## Source of font: https://www.1001fonts.com/press-start-font.html
FONT_FILE_PATH = "lib\\press_start_regular.ttf"

## Colors used in the game
BLACK = (0, 0, 0)
GREEN = (30, 197, 3)
RED = (204, 0, 0)

## (Font) sizes of game elements
SMALL_SIZE = 20
INPUT_SIZE = 35
MEDIUM_SIZE = 50
LARGE_SIZE = 80
TITLE_SIZE = 100
GAME_OVER_SIZE = 70
FINAL_SCORE_SIZE = 40

## Offset used in positioning
POS_OFFSET = 50
INPUT_OFFSET = 30

## Scenes or stages of the game
START = "START"
MODES = "MODES"
SET_TIMER = "SET_TIMER"
PLAY = "PLAY"
GAME_OVER = "GAME_OVER"
SAVE = "SAVE"

## Modes of the PLAY SCENE
RANDOM_WORDS = "RANDOM_WORDS"
ANAGRAMS = "ANAGRAMS"

## Positions of most of the game elements
TITLE_POS = "UPPER_HALF"
START_BTN_POS = "LOWER_HALF"
RND_WRDS_BTN_POS = "UPPER_HALF"
ANAGRAM_BTN_POS = "LOWER_HALF"
DIVIDER_POS = "CENTER"
HELP_POS_1 = "UPPER_MIDDLE"
SET_TIMER_SELECT_POS = "CENTER"
HELP_POS_2 = "LOWER_MIDDLE"
CHAR_SEQ_DISPLAY_POS = "UPPER_HALF"
PLAYER_INPUT_POS = "LOWER_HALF"
SCORE_DISPLAY_POS = "LOWER_MIDDLE"
RETRIES_DISPLAY_POS = "UPPER_RIGHT"
TIME_DISPLAY_POS = "UPPER_MIDDLE"
NEW_GAME_POS = "UPPER_MIDDLE"
GAME_OVER_DISPLAY_POS = "UPPER_HALF"
FINAL_SCORE_POS = "LOWER_HALF"
EXIT_GAME_POS = "LOWER_MIDDLE"
SAVE_STATE_POS = "CENTER"
YES_BTN_POS = "LOWER_LEFT"
NO_BTN_POS = "LOWER_RIGHT"

## Text of the  game elements used in game
START_BTN_TXT = "START"
MODES_HELP_TXT = "SELECT A GAME MODE."
RND_WRDS_BTN_TXT = "RANDOM WORDS"
DIVIDER_TXT = "---------------"
ANAGRAM_BTN_TXT = "ANAGRAMS"
SET_TIMER_HELP_TXT_1 = "CLICK TO CHANGE."
SET_TIMER_SELECT_TXT = ["NO TIME", "1 MIN.", "3 MIN.", "5 MIN.", "7 MIN.", "10 MIN."]
SET_TIMER_HELP_TXT_2 = "PRESS [ENTER] TO CONFIRM."
NEW_GAME_TXT = "PRESS [N] FOR NEW GAME."
GAME_OVER_DISPLAY_TXT = "GAME OVER"
FINAL_SCORE_TXT = "YOU SCORED "
NO_MONEY_TXT = "YOU GOT NOTHING!"
EXIT_GAME_TXT = "CLICK TO EXIT GAME."
SAVE_STATE_TXT = "SAVE STATE?"
YES_BTN_TXT = "YES"
NO_BTN_TXT = "NO"

class Display:
    """ A class used to represent a game object that displays text

        Attributes
        ----------
        text : str
            text to be printed on the game screen
        size : int
            size of the text
        pos: str
            general area where the text will be displayed on-screen
        color : tuple, optional
            RGB values of the color that the text will be displayed in (default is GREEN)
        Methods
        -------
        get_font()
            Returns the font to be used in displaying the text
        
        printable()
            Returns the Surface with the text to be displayed
        
        get_coordinates(offset=POS_OFFSET)
            Returns the size and offset of the rendered text based on the specified position
    """    

    def __init__(self, text, size, pos, color=GREEN):
        """
            Parameters
            ----------
            text : str
                text to be displayed on the game screen
            size : int
                size of the text
            pos : str
                location of the game element on-screen
            color : list
                RGB values of the color that the text will be displayed in (default is GREEN)
        """

        self.text = text
        self.size = size
        self.pos = pos
        self.color = color
    
    def get_font(self):
        """ 
            Returns
            -------
            Font
                A pygame.Font object that can be used in rendering text
        """
        return pygame.font.Font(FONT_FILE_PATH, self.size)

    def printable(self):
        """
            Returns
            -------
            Surface
                A pygame.Surface object that displays the current string from the choices
        """

        return self.get_font().render(self.text, True, self.color)
    
    def get_coordinates(self, offset=POS_OFFSET):
        """ Returns the pygem.Rect of the object, which is a list of coordinates

            Parameters
            ----------
            offset : int, optional
                offset used in position game elements (default is POS_OFFSET)
            
            Returns
            -------
            Rect
                A pygame.Rect object that is used in positioning game elements on the screen based on the origin of the Surface
        """

        btn_rect = self.printable().get_rect()
        if self.pos == "UPPER_LEFT":
            btn_rect.topleft = (offset, offset)
        elif self.pos == "UPPER_MIDDLE":
            btn_rect.midtop = (SCREEN_WIDTH / 2, offset)
        elif self.pos == "UPPER_RIGHT":
            btn_rect.topright = (SCREEN_WIDTH - offset, offset)
        elif self.pos == "UPPER_HALF":
            btn_rect.center = (SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - (offset * 2))
        elif self.pos == "CENTER":
            btn_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        elif self.pos ==  "LOWER_HALF":
            btn_rect.center = (SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + (offset * 2))
        elif self.pos == "LOWER_LEFT":
            btn_rect.bottomleft = (offset, SCREEN_HEIGHT - offset)
        elif self.pos == "LOWER_MIDDLE":
            btn_rect.midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - offset)
        elif self.pos == "LOWER_RIGHT":
            btn_rect.bottomright = (SCREEN_WIDTH - offset, SCREEN_HEIGHT - offset)
        return btn_rect

class Button(Display):
    """ A class inherited from Display that supports text rendering and a hover state
    
        Attributes
        ----------
        text : str
            text to be printed on the game screen
        size : int
            size of the text
        pos : str
            location of the game element on-screen
        color : list
            RGB values of the color that the text will be displayed in
        hover : boolean
            truth value of whether the cursor is hovering over it or not

        Methods
        -------
        get_font()
            Returns the font to be used in displaying the text, which takes into account the hover state of the button
        
        is_colliding(obj_pos)
            Returns the truth value of whether the other object, mostly the mouse cursor, is overlapping the area of the button
    """

    HOVER_STATE_INCREMENT = 5

    def __init__(self, text, size, pos, color=GREEN, hover=False):
        """
            Parameters
            ----------
            text : str
                text to be displayed on the game screen
            size : int
                size of the text
            pos : str
                location of the game element on-screen
            color : list
                RGB values of the color that the text will be displayed in (default is GREEN)
            hover : boolean
                truth value of whether the cursor is hovering over it or not (default is False)
        """

        super().__init__(text, size, pos, color)
        self.hover = hover

    def get_font(self):
        """ Returns a pygame.Font object that takes into account the increase in size when a button is hovered over

            Returns
            -------
            Font
                A pygame.Font object that can be used in rendering text
        """

        if self.hover:
            return pygame.font.Font(FONT_FILE_PATH, self.size + self.HOVER_STATE_INCREMENT)
        return pygame.font.Font(FONT_FILE_PATH, self.size)

    def is_colliding(self, obj_pos):
        """ Checks whether the object specified is overlapping with the area of the button and returns a truth value

            Parameters
            ----------
            obj_pos : tuple
                position in terms of x and y of the object, usually the mouse cursor
            
            Returns
            -------
            boolean
                A truth value on whether the position of the object is overalapping the area of the button
        """

        return self.get_coordinates().collidepoint(obj_pos)

class Select(Button):
    """ A class inherited from Button that supports rendering a list of text values
    
        Attributes
        ----------
        choices : list
            list of strings to be cycled through and displayed on the game screen
        text : str
            currently displayed string from choices
        size : int
            size of the text
        pos : str
            location of the game element on-screen
        color : tuple, optional
            RGB values of the color that the text will be displayed in (default is GREEN)
        hover : boolean, optional
            truth value of whether the cursor is hovering over it or not (default is False)

        Methods
        -------
        change_text()
            Changes the text displayed by cycling through the list of strings
        
        printable()
            Returns the Surface with the text to be displayed which changes based on its text attribute
    """

    def __init__(self, choices, size, pos, color=GREEN, hover=False):
        """
            Parameters
            ----------
            choices : list
                list of strings to be cycled through and displayed on the game screen
            size : int
                size of the text
            pos : str
                location of the game element on-screen
            color : list
                RGB values of the color that the text will be displayed in (default is GREEN)
            hover : boolean
                truth value of whether the cursor is hovering over it or not (default is False)
        """

        self.choices = choices
        self.index = 0
        self.text = self.choices[self.index]
        super().__init__(self.text, size, pos, color)

    def change_text(self):
        """Increments the index and updates the text to be displayed"""

        if self.index < len(self.choices) - 1:
            self.index += 1
        else:
            self.index = 0
        self.text = self.choices[self.index]

    def printable(self):
        """
            Returns
            -------
            Surface
                A pygame.Surface object that displays the current string from the choices
        """
        
        return self.get_font().render(self.text, True, self.color)

class Input(Display):
    """ A class inherited from Display that supports displaying player input
    
        Attributes
        ----------
        size : int
            size of the text
        pos : int
            location of the game element on the screen
        text : str, optional
            player input (default is "")
        color : tuple, optional
            RGB values of the color that the text will be displayed in (default is GREEN)

        Methods
        -------
        add_input(char)
            Adds player input to the text attribute
        
        backspace()
            Removes the last character from the text attribute
        
        reset_input()
            Clears the player's input
    """

    def __init__(self, size, pos, text="", color=GREEN):
        """
            Parameters
            ----------
            size : int
                size of the text
            pos : str
                location of the game element on-screen
            text : str, optional
                player input (default is "")
            color : list
                RGB values of the color that the text will be displayed in (default is GREEN)
        """
        
        super().__init__(text, size, pos, color)
    
    def add_input(self, char):
        """ Updates the text attribute via the player's input per character

            Parameters
            ----------
            char : str
                character inputted by player
        """

        self.text += char
    
    def backspace(self):
        """Removes the last character of the text attribute"""

        if self.text != "":
            self.text = self.text[:-1]

    def reset_input(self):
        """Resets player input"""

        self.text = ""

# Elements of the game used in the interface

## Used in START SCENE
TITLE = Display(GAME_TITLE, TITLE_SIZE, TITLE_POS)
START_BTN = Button(START_BTN_TXT, MEDIUM_SIZE, START_BTN_POS)

## Used in MODES SCENE
MODES_HELP = Display(MODES_HELP_TXT, SMALL_SIZE, HELP_POS_1)
RND_WRDS_BTN = Button(RND_WRDS_BTN_TXT, MEDIUM_SIZE, RND_WRDS_BTN_POS)
DIVIDER = Display(DIVIDER_TXT, MEDIUM_SIZE, DIVIDER_POS)
ANAGRAMS_BTN = Button(ANAGRAM_BTN_TXT, MEDIUM_SIZE, ANAGRAM_BTN_POS)

## Used in SET TIMER SCENE
SET_TIMER_HELP_1 = Display(SET_TIMER_HELP_TXT_1, SMALL_SIZE, HELP_POS_1)
SET_TIMER_SELECT = Select(SET_TIMER_SELECT_TXT, LARGE_SIZE, SET_TIMER_SELECT_POS)
SET_TIMER_HELP_2 = Display(SET_TIMER_HELP_TXT_2, SMALL_SIZE, HELP_POS_2)

## Used in PLAY SCENE

### The following functions take into account the changing nature of the parameters,
### which is why constants/variables were not used for these.
def display_char_seq(char_seq, game_screen):
    char_seq_display = Display(char_seq, MEDIUM_SIZE, CHAR_SEQ_DISPLAY_POS)
    game_screen.blit(char_seq_display.printable(), char_seq_display.get_coordinates())

def display_score(score, game_screen):
    score_display = Display("$" + str(score), MEDIUM_SIZE, SCORE_DISPLAY_POS)
    game_screen.blit(score_display.printable(), score_display.get_coordinates())

def display_retries(retries, game_screen):
    retries_display = Display(str(retries) + "X", MEDIUM_SIZE, RETRIES_DISPLAY_POS)
    game_screen.blit(retries_display.printable(), retries_display.get_coordinates())

def display_time(time, game_screen):
    time_display = Display(time, MEDIUM_SIZE, TIME_DISPLAY_POS)
    game_screen.blit(time_display.printable(), time_display.get_coordinates())

PLAYER_INPUT = Input(INPUT_SIZE, PLAYER_INPUT_POS)

## Used in GAME OVER SCENE
GAME_OVER_DISPLAY = Display(GAME_OVER_DISPLAY_TXT, GAME_OVER_SIZE, GAME_OVER_DISPLAY_POS)

### Same as previous functions
def display_final_score(final_score, game_screen):
    if not final_score:
        final_score_display = Display(NO_MONEY_TXT, FINAL_SCORE_SIZE, FINAL_SCORE_POS)
    else:
        final_score_display = Display(FINAL_SCORE_TXT + "$" + str(final_score) + ".", FINAL_SCORE_SIZE, FINAL_SCORE_POS)
    game_screen.blit(final_score_display.printable(), final_score_display.get_coordinates())

NEW_GAME = Display(NEW_GAME_TXT, SMALL_SIZE, NEW_GAME_POS)
EXIT_GAME = Display(EXIT_GAME_TXT, SMALL_SIZE, EXIT_GAME_POS)

## Used in SAVE SCENE
SAVE_STATE = Display(SAVE_STATE_TXT, MEDIUM_SIZE, SAVE_STATE_POS)
YES_BTN = Button(YES_BTN_TXT, MEDIUM_SIZE, YES_BTN_POS)
NO_BTN = Button(NO_BTN_TXT, MEDIUM_SIZE, NO_BTN_POS)