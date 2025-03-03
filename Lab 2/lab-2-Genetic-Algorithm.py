import random


def fitness_function(chromosome, starting_capital, history):
    capital = starting_capital
    invest = capital * (chromosome["trade_size"]/100)
    for i in range(len(history)):

        price_change = history[i]
        if price_change > 0:
            if price_change > chromosome["take_profit"]:
                price_change = chromosome["take_profit"]
        else:
            if price_change < -chromosome["stop_loss"]:
                price_change = -chromosome["stop_loss"]

        profitOrLoss = invest * (price_change/100)
        capital += profitOrLoss

    fitness = capital - starting_capital
    return fitness


def single_point_crossover(chromosome1, chromosome2):
    point = random.randint(1, 2)
    offspring1 = {}
    offspring2 = {}

    # making replica to avoid pass by reference
    for key in chromosome1:
        offspring1[key] = chromosome1[key]
        offspring2[key] = chromosome2[key]

    if point == 1:  # {"stop_loss": 2, || "take_profit": 5, "trade_size": 20}
        offspring1["stop_loss"], offspring2["stop_loss"] = offspring2["stop_loss"], offspring1["stop_loss"]
        
    else:  # {"stop_loss": 2, "take_profit": 5, || "trade_size": 20}
        offspring1["trade_size"], offspring2["trade_size"] = offspring2["trade_size"], chromosome1["trade_size"]

    return offspring1, offspring2


def mutation(chromosome):
    point = random.randint(1, 3)

    if point == 1:  # stop_loss
        maximum = chromosome["stop_loss"] + chromosome["stop_loss"]*0.05
        minimum = chromosome["stop_loss"] - chromosome["stop_loss"]*0.05

        new_value = random.random() * (maximum - minimum) + minimum
        chromosome["stop_loss"] = round(new_value, 2)
    elif point == 2:
        maximum = chromosome["take_profit"] + chromosome["take_profit"]*0.05
        minimum = chromosome["take_profit"] - chromosome["take_profit"]*0.05

        new_value = random.random() * (maximum - minimum) + minimum
        chromosome["take_profit"] = round(new_value, 2)
    else:
        maximum = chromosome["trade_size"] + chromosome["trade_size"]*0.05
        minimum = chromosome["trade_size"] - chromosome["trade_size"]*0.05

        new_value = random.random() * (maximum - minimum) + minimum
        chromosome["trade_size"] = round(new_value, 2)

    # return chromosome


def min_fitness_elimination(chromosome_li, investment, history):
    value_list = []

    for i in range(len(chromosome_li)):
        if i == 0:
            value = fitness_function(chromosome_li[i], investment, history)
            value_list.append(value)
            min_fitness = value
            min_fitness_index = 0
        else:
            value = fitness_function(chromosome_li[i], investment, history)
            value_list.append(value)

            if value < min_fitness:
                min_fitness = value
                min_fitness_index = i

    chromosome_li.pop(min_fitness_index)

    #chromosome_li => pass by reference



# main procedure

initial_capital = int(input("Capital to start with: "))
price_history = list(map(float, input("Historical Prices: ").split(","))) # comma seperated price change values ==> "-1.2, 3.4, -0.8, 2.1, -2.5, 1.7, -0.3, 5.8, -1.1, 3.5"
population_numbers = input("Initial Population: ").split()  # space seperated 6 digit numbers in a single string ==> "020520 030730 070425 080615"
max_generations = int(input("Generations: "))

# initial_capital = 1000
# price_history = list(map(float, "-1.2, 3.4, -0.8, 2.1, -2.5, 1.7, -0.3, 5.8, -1.1, 3.5".split(',')))
# population_numbers = "020520 030730 070425 080615".split()
# max_generations = 10



population = []
for number in population_numbers:
    sl = int(number[:2])
    tp = int(number[2:4])
    ts = int(number[4:6])
    population.append({"stop_loss": sl, "take_profit": tp, "trade_size": ts})

min_fitness_elimination(population, initial_capital, price_history) #lowest fitness parent eliminated


for i in range(max_generations):

    os_population = []

    while len(os_population) < len(population): #ensuring that offspringCount == parentCount
        p1_index, p2_index = random.sample(range(0, len(population)), 2)

        os1, os2 = single_point_crossover(population[p1_index], population[p2_index])

        mutation(os1)
        mutation(os2)

        os_population.append(os1)
        os_population.append(os2)

    min_fitness_elimination(os_population, initial_capital, price_history)

    population = os_population


best_chromosome = None
best_fitness = None

while len(population) != 1:
    min_fitness_elimination(population, initial_capital, price_history)

best_chromosome = population[0]
final_profit = fitness_function(best_chromosome, initial_capital, price_history)


print("Best Strategy: ", best_chromosome)
print("Final profit: ", final_profit)

print()
# Part two
def two_point_crossover(chromosome1, chromosome2):

    point1 = random.randint(1, len(chromosome1)-3)
    point2 = random.randint(point1 + 1, len(chromosome1)-2)
    os1 = chromosome1[:point1] + chromosome2[point1:point2] + chromosome1[point2:]
    os2 = chromosome2[:point1] + chromosome1[point1:point2] + chromosome2[point2:]

    return os1, os2

index1, index2 = random.sample(range(0, len(population_numbers)-1),2)

random_p1 = population_numbers[index1]
random_p2 = population_numbers[index2]

offspring1, offspring2  = two_point_crossover(random_p1, random_p2)

print(offspring1)
print(offspring2)