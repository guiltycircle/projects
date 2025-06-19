import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Game
from django.utils.crypto import get_random_string

CHOICES = ['rock', 'paper', 'scissors']

# Main game view
def play(request):
    # Reset scores if reset button is pressed
    if request.method == 'POST' and 'reset' in request.POST:
        request.session['user_score'] = 0
        request.session['computer_score'] = 0
        request.session['result'] = None
        request.session['user_choice'] = None
        request.session['computer_choice'] = None
        return HttpResponseRedirect(reverse('play'))

    # Initialize scores in session if not present
    if 'user_score' not in request.session:
        request.session['user_score'] = 0
    if 'computer_score' not in request.session:
        request.session['computer_score'] = 0

    # Single player mode logic
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

def home(request):
    return render(request, 'game/home.html')

def create_game(request):
    game = Game.objects.create()
    # Mark this session as player 1 for this game
    request.session['player_role'] = '1'
    request.session['player_game_code'] = game.code
    return redirect(f'/game/{game.code}/?player=1')

def join_game(request):
    error = None
    if request.method == 'POST':
        code = request.POST.get('code', '').upper()
        try:
            game = Game.objects.get(code=code)
            # Mark this session as player 2 for this game
            request.session['player_role'] = '2'
            request.session['player_game_code'] = game.code
            return redirect(f'/game/{game.code}/?player=2')
        except Game.DoesNotExist:
            error = 'Game not found.'
    return render(request, 'game/join.html', {'error': error})

def multiplayer_game(request, code):
    game = get_object_or_404(Game, code=code)
    player = request.GET.get('player')
    # Allow rejoining: only redirect to home if player/session info is missing or invalid
    if not player or request.session.get('player_game_code') != code or request.session.get('player_role') != player:
        return redirect('home')
    # Determine if this session is player 1 and should see the code
    show_code = False
    if request.session.get('player_role') == player and request.session.get('player_game_code') == code and player == '1':
        show_code = True
    error = None
    result = None
    # Handle player choice
    if request.method == 'POST':
        choice = request.POST.get('choice')
        if player == '1' and not game.player1_choice:
            game.player1_choice = choice
            game.save()
        elif player == '2' and not game.player2_choice:
            game.player2_choice = choice
            game.save()
        # After both have played, determine result and update scores
        if game.player1_choice and game.player2_choice:
            if game.player1_choice == game.player2_choice:
                result = 'Draw!'
                game.status = 'waiting'
            elif (
                (game.player1_choice == 'rock' and game.player2_choice == 'scissors') or
                (game.player1_choice == 'scissors' and game.player2_choice == 'paper') or
                (game.player1_choice == 'paper' and game.player2_choice == 'rock')
            ):
                result = 'Player 1 wins!'
                game.player1_score += 1
                game.status = 'waiting'
            else:
                result = 'Player 2 wins!'
                game.player2_score += 1
                game.status = 'waiting'
            game.save()
            # Store result in session for one GET for both players
            request.session[f'result_{code}_{player}'] = result
            # Reset choices for next round automatically
            game.player1_choice = None
            game.player2_choice = None
            game.save()
        return redirect(request.path + f'?player={player}')
    # Show result for one GET, then clear it
    result_key = f'result_{code}_{player}'
    if result_key in request.session:
        result = request.session[result_key]
        del request.session[result_key]
    context = {
        'game': game,
        'code': code,
        'player': player,
        'choices': CHOICES,
        'result': result,
        'show_code': show_code,
    }
    return render(request, 'game/multiplayer.html', context)
