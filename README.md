# ICA$H.exe

ICA$H, for short, is a word unscrambler game with two modes of play labeled “Random Words” and “Anagrams”. The former combines random words to form a sequence of characters from which the player must get from to form either the words used in creating the sequence or other words that are in the provided word list. The latter, on the other hand, gives the player a word that they must rearrange the letters, if possible, to form new words. The goal for both game modes is to amass the highest amount of money in the case of this game, hopefully giving players the feeling of accomplishment as if they successfully “hacked into the system”. Players can opt to either work under time pressure or not, given that they have only 3 retries if they were to input an invalid string. The game as a whole is comprised of three Python (.py) files, namely main.py, engine.py, and interface.py, as well as other files that are loaded into the game to be used in providing gameplay.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Setting Up

A virtual environment was included in the folder so to get the game running, execute the following commands:

This is assuming that you've cd into the project directory.

**For Windows**

```
iCash\Scripts\activate
```

**For Mac & Linux**

```
source <venv>/bin/activate
```

Once activated, execute the following just to make sure that the required packages are installed

```
python -m pip install -r requirements.txt
```

Lastly, start up the game by running

```
python main.py
```

## Required Packages

The packages listed below are for linting and running the game.

* astroid==2.0.4
* colorama==0.4.0
* isort==4.3.4
* lazy-object-proxy==1.3.1
* mccabe==0.6.1
* pygame==1.9.4
* pylint==2.1.1
* six==1.11.0
* wrapt==1.10.11

## Folder Structure

```bash
├── .vscode (vscode support)
│   └── launch.json
├── iCash (venv)
├── lib
│   ├── 2of12inf.txt
│   ├── press_start_regular.ttf
│   └── save_file.txt
├── .gitignore
├── engine.py
├── iCash.code-workspace (vscode support)
├── interface.py
├── main.py
├── README.md
└── requirements.txt
```

## Authors

* Eunice Ceniza
* Nigel Padua
* Brandon Martin

## Sources

* [http://wordlist.aspell.net/12dicts/](http://wordlist.aspell.net/12dicts/)
* [https://www.1001fonts.com/press-start-font.html](https://www.1001fonts.com/press-start-font.html)