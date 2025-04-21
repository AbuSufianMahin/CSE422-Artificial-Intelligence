import math
import random

# part - 1
def strength(x):
    return math.log2(x+1) + x/2


def utility(max_V, min_V):
    i = random.randint(0, 1)
    random_1to10 = random.randint(1, 10)

    result = strength(max_V) - strength(min_V) + ((-1)**i) * (random_1to10/10)

    return result


def minimax(alpha, beta, depth, maximizing_player, maxP_baseStregnth, minP_baseStrength, mind_control=False):
    if depth == 0:
        return utility(maxP_baseStregnth, minP_baseStrength)

    if maximizing_player == True:
        minAlpha = -math.inf

        for x in range(2):
            current_value = minimax(alpha, beta, depth-1, False, maxP_baseStregnth, minP_baseStrength)

            max_value = max(minAlpha, current_value)
            alpha = max(alpha, current_value)

            if alpha >= beta:
                break

        return round(max_value, 2)
    
    else:
        if mind_control == True:
            minAlpha = -math.inf

            for y in range(2):
                current_value = minimax(alpha, beta, depth-1, False, maxP_baseStregnth, minP_baseStrength)

                max_value = max(minAlpha, current_value)
                alpha = max(alpha, current_value)

                if alpha >= beta:
                    break

            return round(max_value, 2)

        else:
            maxBeta = math.inf

            for p in range(2):
                current_value = minimax(alpha, beta, depth-1, True, maxP_baseStregnth, minP_baseStrength)

                min_value = min(maxBeta, current_value)
                beta = min(beta, current_value)

                if alpha >= beta:
                    break

        return round(min_value, 2)


starting_player = int(input("Enter starting player for game 1 (0 for Carlsen, 1 for Caruana):"))

carlsen_base_strength = int(input("Enter base strength for Carlsen:"))
caruana_base_strength = int(input("Enter base strength for Caruana:"))


carlsen_score = 0
caruana_score = 0
draw_count = 0

for game_num in range(4):  # 4 games
    if (game_num + starting_player) % 2 == 0:
        max_player = "Magnus Carlsen"
        min_player = "Fabiano Caruana"

        maxV = carlsen_base_strength
        minV = caruana_base_strength
    else:
        max_player = "Fabiano Caruana"
        min_player = "Magnus Carlsen"

        maxV = caruana_base_strength
        minV = carlsen_base_strength

    score = minimax(-math.inf, math.inf, 5, True, maxV, minV)

    if score > 0:
        winner = max_player
    elif score < 0:
        winner = min_player
    else:
        winner = "Draw"

    if winner == "Magnus Carlsen":
        carlsen_score += 1
    elif winner == "Fabiano Caruana":
        caruana_score += 1
    else:
        draw_count += 1

    if winner == min_player:
        attribute = "Min"
    elif winner == max_player:
        attribute = "Max"

    print(f"Game {game_num + 1} winner : {winner} ({attribute}) (Utility value : {score})")


print("Overall Results:")
print("Magnus Carlsen Wins:", carlsen_score)
print("Fabiano Caruana Wins:", caruana_score)
print("Draws:", draw_count)
print("Overall Winner:", end=" ")

if carlsen_score > caruana_score:
    print("Magnus Carlsen")
elif carlsen_score < caruana_score:
    print("Fabiano Caruana")
else:
    print("Draw")



# part 2 
part2_starting_player = int(input("Enter who goes first (0 for Light, 1 for L): "))

cost = float(input("Enter the cost of using Mind Control: "))
light_stregth = float(input("Enter base strength for Light: "))
l_strength = float(input("Enter base strength for L: "))

if part2_starting_player == 0: 
    max_p = "Light"
    max_base_strength = light_stregth
    min_base_strength = l_strength
else:
    max_p = "L"
    max_base_strength = l_strength
    min_base_strength = light_stregth

normal_score = minimax(-math.inf, math.inf, 5, True, max_base_strength, min_base_strength)
controlled_score = minimax(-math.inf, math.inf, 5, True, maxV, minV, mind_control=True)

score_incurring_cost = round(controlled_score - cost, 2)

print(f"Minimax value without Mind Control: {normal_score}")
print(f"Minimax value with Mind Control: {controlled_score}")
print(f"Minimax value with Mind Control after incurring the cost: {score_incurring_cost}")

if normal_score > 0:
    if score_incurring_cost > 0 :
        print(f"{max_p} should NOT use Mind Control as the position is already winning.")
    else:
       print(f"{max_p} should NOT use Mind Control as it backfires.") 
else:
    if score_incurring_cost > 0:
        print(f"{max_p} should use Mind Control.")
    else:
        print(f"{max_p} should NOT use Mind Control as the position is losing either way.")

