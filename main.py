import torch
from torch import nn

answers = ["ant", "and", "tan"]
letters = "antd"

letter_bits = len(letters)
color_bits = 2
column_count = 3
row_count = 5

white = [0, 0]
gray = [0, 1]
yellow = [1, 0]
green = [1, 1]


class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear((letter_bits + color_bits) * column_count * row_count, 50),
            nn.ReLU(),
            nn.Linear(50, 50),
            nn.ReLU(),
            nn.Linear(50, letter_bits * column_count),
        )

    def forward(self, x):
        # x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

model = NeuralNetwork()

learning_rate = 1e-3


def blank_row():
    return (([0.0] * letter_bits) + white) * 3

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
        mx_val = 'x'
        for j in range(4):
            new = list[i*4 + j]
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

def train_loop(model, loss_fn, optimizer):
    for e in range(3000):
        for answer in answers:
            guesses = []
            preds = []
            for i in range(row_count):
                pred = model(mk_grid(answer, guesses))
                guess = pred_to_letters(pred)
                preds.append(pred)
                guesses.append(guess)
            if e % 100 == 0:
                print(e, answer, guesses)
            loss = loss_fn(torch.stack(preds), torch.stack([mk_answer(answer)] * row_count))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

train_loop(model, loss_fn, optimizer)
