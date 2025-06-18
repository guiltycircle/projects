import random
from django.shortcuts import render

CHOICES = ['rock', 'paper', 'scissors']

# Main game view
def play(request):
    result = None
    user_choice = None
    computer_choice = None
    if request.method == 'POST':
        user_choice = request.POST.get('choice')
        computer_choice = random.choice(CHOICES)
        if user_choice == computer_choice:
            result = 'Draw!'
        elif (
            (user_choice == 'rock' and computer_choice == 'scissors') or
            (user_choice == 'scissors' and computer_choice == 'paper') or
            (user_choice == 'paper' and computer_choice == 'rock')
        ):
            result = 'You win!'
        else:
            result = 'Computer wins!'
    return render(request, 'game/play.html', {
        'choices': CHOICES,
        'result': result,
        'user_choice': user_choice,
        'computer_choice': computer_choice,
    })
