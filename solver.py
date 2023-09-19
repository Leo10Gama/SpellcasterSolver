"""Methods and functions to solve Discord's SpellCast game"""


from typing import Dict, List, Optional, Tuple
from trie import Trie


LETTER_POINTS = {
    "a": 1,
    "b": 4,
    "c": 5,
    "d": 3,
    "e": 1,
    "f": 5,
    "g": 3,
    "h": 4,
    "i": 1,
    "j": 7,
    "k": 6,
    "l": 3,
    "m": 4,
    "n": 2,
    "o": 1,
    "p": 4,
    "q": 8,
    "r": 2,
    "s": 2,
    "t": 2,
    "u": 4,
    "v": 5,
    "w": 5,
    "x": 7,
    "y": 4,
    "z": 8
}


def find_words(
    board: str, trie: Trie, dl: Optional[Tuple[int, int]], dw: Optional[Tuple[int, int]], tl: Optional[Tuple[int, int]]
) -> Dict[int, List[str]]:
    """Find all words and their respective point values on the board.
    
    Parameters
    ----------
    board: str
        A string representation of the board, as read from top left, rightwards, to
        bottom right.
    trie: Trie
        The trie dictionary of words to check.
    dl: Optional[Tuple[int, int]]
        The (x, y) position of the double-letter modifier, if it exists on the board.
    dw: Optional[Tuple[int, int]]
        The (x, y) position of the double-word modifier, if it exists on the board.
    tl: Optional[Tuple[int, int]]
        The (x, y) position of the triple-word modifier, if it exists on the board.
    """
    points_to_words = {}
    # TODO: This method


def solver():
    board = input("Enter board (from top left, read rightwards to bottom right): ").lower()
    dl_in = input("Enter double-letter modifier position (in form 'x,y' from (0-4), nothing if no modifier): ")
    dl = (int(dl_in.split(",")[0]), int(dl_in.split(",")[1])) if dl_in else None
    dw_in = input("Enter double-word modifier position (in form 'x,y' from (0-4), nothing if no modifier): ")
    dw = (int(dw_in.split(",")[0]), int(dw_in.split(",")[1])) if dw_in else None
    tl_in = input("Enter triple-letter modifier position (in form 'x,y' from (0-4), nothing if no modifier): ")
    tl = (int(tl_in.split(",")[0]), int(tl_in.split(",")[1])) if tl_in else None
    trie = Trie(populate=True)
    words = find_words(board, trie, dl, dw, tl)


if __name__=='__main__':
    solver()
