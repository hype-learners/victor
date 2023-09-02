#!/usr/bin/env python3
from collections import defaultdict
import signal
import sys

# Config start.

START_POINTS = 7
VOTE_POINTS = 5
NO_VOTE = 0
FAKE = "Фэйк"

GM = "FILL THIS"
players = {
    # Fill this.
}

if GM in players:
    raise 'ГМ не должен входить в список игроков'

points_per_player = {}
for player in players:
    points_per_player[player] = START_POINTS

# Config end.


def select_opinion(options, player):
    print(f"Выбирает {player}:")
    for n, option in enumerate(options):
        print(f"{n + 1}: {option}")
    print(f"0: Отказ от голосования")

    opinion = -1
    while opinion < 0 or opinion > len(options):
        opinion = input("Выберите номер: ")
        if not opinion.isdigit():
            continue
        opinion = int(opinion)

    if opinion == 0:
        return 0, NO_VOTE

    opinion -= 1

    if player == GM:
        return 0, opinion

    player_points = points_per_player[player]

    points = -1
    while points < 0 or points > player_points:
        points = input(f"Сколько очков поставить? (максимум {player_points}) ")
        if not points.isdigit():
            continue
        points = int(points)

    return points, opinion


def exit_game(*_):
    print('Завершение работы...')
    exit()


def main():
    # Catch ctrl-C and exit.
    signal.signal(signal.SIGINT, exit_game)

    while True:
        # Important: dict order is preserved from python 3.7,
        # see https://mail.python.org/pipermail/python-dev/2017-December/151283.html
        options = {}

        print(f"{GM} вводит варианты выбора:")
        for gm_input in sys.stdin.readlines():
            options[gm_input.strip()] = 0

        opinions = defaultdict(list)

        for player in players:
            points, opinion = select_opinion(options, player)

            if opinion != NO_VOTE:
                if points < VOTE_POINTS:
                    opinions[FAKE].append(player)
                else:
                    option = list(options.keys())[opinion]
                    options[option] += points
                    opinions[option].append(player)

        max_points = max(options)

        if max_points == 0:
            print('Никто не проголосовал, скип.')
            continue

        winning_options = list(filter(lambda p: p == max_points, options))

        if len(winning_options) == 1:
            print(f"Победил выбор: {winning_options[0]}")
            print(f"За него проголосовали: {opinions[winning_options[0]]}")
        else:
            gm_opinion, _ = select_opinion(winning_options, GM)
            print(f"Ничья, {GM} выбрал: {gm_opinion}")
        print(f"Пофейкали: {opinions[FAKE]}")

        print()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Ошибка: {e}")
