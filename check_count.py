from sys import argv


GAME_FILE = argv[1]

with open(f"{GAME_FILE}", "r") as f:
    plays = [line for line in f if line.startswith("play")]

for play in plays:
    *_, count, sequence, event = play.split(",")

    strikes = ["A", "C", "K", "M", "Q", "S"]
    fouls = ["F", "L", "O", "R", "T"]
    balls = ["B", "I", "P", "V"]

    count_strikes = 0
    count_balls = 0

    for index, action in enumerate(sequence):
        if event[:2] in ["SB", "CS", "PB", "WP"] and index == len(sequence) - 1:
            pass
        else:
            if action in strikes and count_strikes < 2:
                count_strikes += 1
            if action in balls and count_balls < 3:
                count_balls += 1
            if action in fouls and count_strikes < 2:
                count_strikes += 1

    new_count = f"{count_balls}{count_strikes}"

    if new_count != count:
        print(play, end="")
        print(" count " + count + " | should be: " + new_count + "\n")
