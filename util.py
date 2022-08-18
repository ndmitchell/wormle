import torch
from torch import nn
from config import *

def blank_row():
    return (([0.0] * letter_bits) + white) * column_count

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
    return res

def mk_grid(answer, guess):
    res = []
    for i in range(row_count):
        if len(guess) <= i:
            res += blank_row()
        else:
            res += filled_row(answer, guess[i])
    return torch.Tensor(res)

def pred_to_letters(pred):
    res = ""
    list = pred.tolist()
    for i in range(column_count):
        mx = -100
        mx_val = '?'
        for j in range(letter_bits):
            new = list[i*letter_bits + j]
            if new > mx:
                mx = new
                mx_val = letters[j]
        res += mx_val
    return res

def mk_answer(answer):
    res = []
    for x in answer:
        res += encode_letter(x)
    return torch.tensor(res)
