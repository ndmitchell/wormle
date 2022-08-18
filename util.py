import torch
from torch import nn
from config import *

_blank_row = torch.zeros(((letter_bits + color_bits) * column_count,), dtype=torch.float)

# Create a blank row of the approxiate size
def blank_row():
    return _blank_row

# Convert a single letter to a array of letter bits
def encode_letter(x):
    return [1.0 if c == x else 0.0 for c in letters]

def filled_row(answer, guess):
    res = []
    for i in range(column_count):
        letter = encode_letter(guess[i])
        if guess[i] == answer[i]:
            status = green
        elif guess[i] in answer:
            status = yellow
        else:
            status = gray
        res += letter + status
    return torch.tensor(res)

def mk_grid(answer, guess):
    res = []
    for i in range(row_count):
        if len(guess) <= i:
            res.append(blank_row())
        else:
            res.append(filled_row(answer, guess[i]))
    return torch.stack(res).flatten()

def pred_to_letters(pred):
    res = ""
    for p in pred.reshape((column_count, letter_bits)):
        res += letters[p.argmax()]
    return res

def mk_answer(answer):
    res = []
    for x in answer:
        res += encode_letter(x)
    return torch.tensor(res)


def show_grid(answer, grid):
    green_tick = "\033[92m\u2714\uFE0F\033[0m"
    red_cross = "\033[91m\u274C\033[0m"

    res = answer + " | "
    for x in grid:
        res += " "
        for xc, ac in zip(x, answer):
            if xc == ac:
                res += "\033[42m" + xc
            elif xc in answer:
                res += "\033[43m" + xc
            else:
                res += "\033[100m" + xc
        res += "\033[0m"
        if x == answer:
            return res + " " + green_tick
    return res + " " + red_cross
