import random

words = ['wheelchair', 'bathroom', 'lasagne']
answer = random.choice(words)
guess = '_' * len(answer)

while guess != answer:
    print('Word: ', guess)

    turn = str(input('Provide a letter: '))

    if turn == '.': break

    if not turn.isalpha() or len(turn) > 1:
        print('incorrect input')
    
    if (turn in answer) and (turn not in guess):
        for index in range(0, len(answer)):
            if answer[index] == turn:
                guess = guess[:index] + answer[index] + guess[index + 1:]

print('Great! Your word was ' + answer + '.')