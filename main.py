import torch
from torch import nn
from config import *
from util import *


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

def train_loop(model, loss_fn, optimizer):
    for e in range(5000):
        # print(e)
        for answer in answers:
            guesses = []
            preds = []
            for i in range(row_count):
                pred = model(mk_grid(answer, guesses))
                guess = pred_to_letters(pred)
                preds.append(pred)
                guesses.append(guess)
            if e % 100 == 0:
                print(e, show_grid(answer, guesses))
            loss = loss_fn(torch.stack(preds), torch.stack([mk_answer(answer)] * row_count))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

train_loop(model, loss_fn, optimizer)
