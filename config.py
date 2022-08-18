real_answers = 0

if real_answers == 0:
    letters = "antd"
    answers = ["ant", "and", "tan"]
else:
    letters = "abcdefghijklmnopqrstuvwxyz"
    with open("wordlist_hidden.txt") as f:
        answers = f.read().split("\n")[:-1]
    answers = answers[:real_answers]

letter_bits = len(letters)
color_bits = 2
column_count = len(answers[0])
row_count = 6

white = [0, 0]
gray = [0, 1]
yellow = [1, 0]
green = [1, 1]
