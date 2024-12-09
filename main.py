from os.path import isdir, isfile
from rich.console import Console
from rich.markdown import Markdown

from lib.getch import _Getch
from lib.clear import clear_screen
from lib.albumatify import albumatify

console = Console()

getch = _Getch()

clear_screen()

with open("WELCOME.md") as welcome:
    markdown = Markdown(welcome.read())
console.print(markdown)

raw_tracks_path = input("\nLet's Albumatify your tracks!\nEnter path to your unordered .mp3's > ")
while not isdir(raw_tracks_path):
    print("Sorry, this path does not exist in your filesystem.")
    raw_tracks_path = input("Enter path to your unordered .mp3's > ")

cover_art_path = input("\nEvery album needs a cover art!\nEnter path to your album's cover art > ")
while not isfile(cover_art_path):
    print("Sorry, this file does not exist in your filesystem.")
    cover_art_path = input("Enter path to your album's cover art > ")

albumatify(raw_tracks_path, cover_art_path, getch, console, clear_screen)
