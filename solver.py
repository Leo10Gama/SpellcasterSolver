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

    # recurse on each tile
    for x in range(5):
        for y in range(5):
            curr_letter = board[x + (y * 5)]
            found_words = find_words_at_tile(board, x, y, trie, dl, dw, tl, curr=curr_letter)
            for points, words in found_words.items():
                if not points_to_words.get(points):
                    points_to_words.update({points: words})
                else:
                    points_to_words[points].update(words)
    return points_to_words


def find_words_at_tile(board, x, y, trie, dl, dw, tl, curr="", taken_coords=[]) -> Dict[int, List[str]]:
    """Starting at a given tile, find all words from that tile.
    
    Parameters are identical to `find_words()`, with the exception being x and y, which
    are the x and y coordinates in range [0, 4] of the tile on the board. In addition,
    curr is used to keep track of whatever the current word we're trying to spell is,
    and taken_coords (which should be equal in length to curr) marks which letters have
    already been used in the current word.
    """
    true_board = [  # allows us to index as board[x][y]
        [board[0], board[5], board[10], board[15], board[20]],
        [board[1], board[6], board[11], board[16], board[21]],
        [board[2], board[7], board[12], board[17], board[22]],
        [board[3], board[8], board[13], board[18], board[23]],
        [board[4], board[9], board[14], board[19], board[24]],
    ]
    points_to_words = {}

    def update_word_total(new_points_to_words):
        for points, words in new_points_to_words.items():
            if not points_to_words.get(points):
                points_to_words.update({points: words})
            else:
                points_to_words[points].update(words)

    # RECURSIVE CASE: tiles in each of the 8 directions
    def check_direction(x, y):
        next_letter = true_board[x][y]
        curr_word = curr + next_letter
        if trie.is_word(curr_word):
            taken_coords.append((x, y))
            points = compute_points(curr_word, taken_coords, dl, dw, tl)
            taken_coords.pop()
            update_word_total({points: set([curr_word])})
        if trie.word_can_continue(curr_word):
            update_word_total(
                find_words_at_tile(board, x, y, trie, dl, dw, tl, curr=curr_word, taken_coords=taken_coords)
            )

    # NW
    if x - 1 >= 0 and y - 1 >= 0 and (x-1, y-1) not in taken_coords:
        taken_coords.append((x, y))
        check_direction(x-1, y-1)
        taken_coords.pop()
    # N
    if y - 1 >= 0 and (x, y-1) not in taken_coords:
        taken_coords.append((x, y))
        check_direction(x, y-1)
        taken_coords.pop()
    # NE
    if x + 1 <= 4 and y - 1 >= 0 and (x+1, y-1) not in taken_coords:
        taken_coords.append((x, y))
        check_direction(x+1, y-1)
        taken_coords.pop()
    # W
    if x - 1 >= 0 and (x-1, y) not in taken_coords:
        taken_coords.append((x, y))
        check_direction(x-1, y)
        taken_coords.pop()
    # E
    if x + 1 <= 4 and (x+1, y) not in taken_coords:
        taken_coords.append((x, y))
        check_direction(x+1, y)
        taken_coords.pop()
    # SW
    if x - 1 >= 0 and y + 1 <= 4 and (x-1, y+1) not in taken_coords:
        taken_coords.append((x, y))
        check_direction(x-1, y+1)
        taken_coords.pop()
    # S
    if y + 1 <= 4 and (x, y+1) not in taken_coords:
        taken_coords.append((x, y))
        check_direction(x, y+1)
        taken_coords.pop()
    # SE
    if x + 1 <= 4 and y + 1 <= 4 and (x+1, y+1) not in taken_coords:
        taken_coords.append((x, y))
        check_direction(x+1, y+1)
        taken_coords.pop()

    # BASE CASE: return all the values we retrieved
    return points_to_words


def compute_points(word: str, coords: List[Tuple[int, int]], dl, dw, tl) -> int:
    """Compute how many points a given word is."""
    total_points = 0
    dw_multiplier = 1
    for i, coord in enumerate(coords):
        points = LETTER_POINTS[word[i]]
        if coord == dl:
            points *= 2
        if coord == tl:
            points *= 3
        if coord == dw:
            dw_multiplier = 2
        total_points += points
    
    return total_points * dw_multiplier + (10 if len(word) >= 6 else 0)


def solver():
    trie = Trie(populate=True)
    working = True
    while working:
        board = input("Enter board (from top left, read rightwards to bottom right): ").lower()
        if len(board) != 25:
            print("Error: board size not equal to 25.")
            return
        dl_in = input("Enter double-letter modifier position (in form 'x,y' from (0-4), nothing if no modifier): ")
        dl = (int(dl_in.split(",")[0]), int(dl_in.split(",")[1])) if dl_in else None
        dw_in = input("Enter double-word modifier position (in form 'x,y' from (0-4), nothing if no modifier): ")
        dw = (int(dw_in.split(",")[0]), int(dw_in.split(",")[1])) if dw_in else None
        tl_in = input("Enter triple-letter modifier position (in form 'x,y' from (0-4), nothing if no modifier): ")
        tl = (int(tl_in.split(",")[0]), int(tl_in.split(",")[1])) if tl_in else None
        swaps = True if input("Would you like to use a swap? (y/N): ").lower() == "y" else False

        print("Finding best words:\n[                         ]\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b", end="")
        words = find_words(board, trie, dl, dw, tl)
        print("#########################] (Done)")
        words_with_swaps = {}
        if swaps:
            print("Performing swaps:\n[                         ]\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b", end="")
            for i, letter in enumerate(board):
                for new_letter in "abcdefghijklmnopqrstuvwxyz":
                    if new_letter == letter: continue
                    new_board = board[:i] + new_letter + board[i+1:]
                    new_words = find_words(new_board, trie, dl, dw, tl)
                    for points, wordset in new_words.items():
                        words_with_swaps.update({points: {f"({i%5}, {i//5})->{new_letter}": wordset}})
                print("#", end="", flush=True)
            print("] (Done)")
        print("Found all words!")

        if swaps: print("=== WITHOUT SWAPPING ===")
        possible_points = []
        for points in words:
            possible_points.append(points)
        possible_points.sort()
        top_results = 5  # give this many points results
        for i in range(min(top_results, len(possible_points))):
            points = possible_points[-1-i]
            print(f"For {points} points...")
            print(f"\t{' / '.join(words[points])}")
        if swaps:
            print("=== WITH 1 SWAP ===")
            possible_points = []
            for points in words_with_swaps:
                possible_points.append(points)
            possible_points.sort()
            top_results = 5  # give this many points results
            for i in range(min(top_results, len(possible_points))):
                points = possible_points[-1-i]
                print(f"For {points} points...")
                for swap in words_with_swaps[points]:
                    print(f"\tSwap {swap}: {' / '.join(words_with_swaps[points][swap])}")
        working = False if input("Continue? (Y/n): ").lower() == "n" else True
    print("Thanks for playing!")
    # osnruymbiidxeugodnonaiuec
    # ourfoujsdiamxaigkiaedlqia


if __name__=='__main__':
    solver()
