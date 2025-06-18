import random
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

CHOICES = ['rock', 'paper', 'scissors']

# Main game view
def play(request):
    # Reset scores if reset button is pressed
    if request.method == 'POST' and 'reset' in request.POST:
        request.session['user_score'] = 0
        request.session['computer_score'] = 0
        # Clear result display
        request.session['result'] = None
        request.session['user_choice'] = None
        request.session['computer_choice'] = None
        return HttpResponseRedirect(reverse('play'))

    # Initialize scores in session if not present
    if 'user_score' not in request.session:
        request.session['user_score'] = 0
    if 'computer_score' not in request.session:
        request.session['computer_score'] = 0

    if request.method == 'POST' and 'choice' in request.POST:
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
            request.session['user_score'] += 1
        else:
            result = 'Computer wins!'
            request.session['computer_score'] += 1
        # Store result and choices in session for display after redirect
        request.session['result'] = result
        request.session['user_choice'] = user_choice
        request.session['computer_choice'] = computer_choice
        return HttpResponseRedirect(reverse('play'))

    # Get result and choices from session, then clear them for next round
    result = request.session.get('result')
    user_choice = request.session.get('user_choice')
    computer_choice = request.session.get('computer_choice')
    request.session['result'] = None
    request.session['user_choice'] = None
    request.session['computer_choice'] = None

    return render(request, 'game/play.html', {
        'choices': CHOICES,
        'result': result,
        'user_choice': user_choice,
        'computer_choice': computer_choice,
        'user_score': request.session['user_score'],
        'computer_score': request.session['computer_score'],
    })
