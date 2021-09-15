import random
n = random.randint(1, 10)
while True:
    guess = int(input('Enter guess: '))
    if guess > n:
        print('Too high! Guess again!')
    elif guess < n:
        print('Too low! Guess again!')
    else:
        print('Success!')
        break
        