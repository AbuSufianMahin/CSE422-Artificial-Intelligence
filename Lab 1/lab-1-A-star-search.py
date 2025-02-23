import heapq

def data_extraction(txt_file):
    line_list = txt_file.readlines()

    heuristic = {}
    graph = {}

    for line in line_list:
        count = 0
        for i in line.split():
            if count == 0 :
                key = i
                count += 1
                continue
            elif count == 1:
                heuristic[key] = int(i)
                graph[key] = {}
            else:
                if count%2 == 0:
                    graph_key = i
                    count +=1 
                    continue
                else:
                    graph[key][graph_key] = int(i)

            count += 1

    return heuristic, graph

def A_star_search(start, target, map, heuristic):
    visited = {}
    for i in heuristic:
        visited[i] = False

    path = {}
    path[(start, heuristic[start])] = None  # path = {(child, distance) : parent}
    visited[start] = 0

    pq = []
    heapq.heappush(pq, (heuristic[start], start))
    path_found = False
    while len(pq) != 0:
        current_distance, current_node = heapq.heappop(pq)
        if visited[current_node]:  # tackling cycles
            continue
        else:
            visited[current_node] = True

        if current_node == target:
            path_found = True
            distance = current_distance
            # print(path)
            break

        if map[current_node] != None:
            for child_node, edge in map[current_node].items():

                if visited[child_node] == False:
                    # approximate distance at this point, starting from start node
                    approximate_distance = current_distance - heuristic[current_node] + edge + heuristic[child_node]
                    # print(f"Child: {child_node} | Value: {approximate_distance}")
                    heapq.heappush(pq, (approximate_distance, child_node))
                    
                    path[(child_node, approximate_distance)] = (current_node, current_distance)
                    
    if path_found:
        direction = target

        endpoint = target
        x = distance

        while path[(endpoint, x)] != None:
            startpoint, x = path[(endpoint, x)]
            direction = f"{startpoint} -> {direction}" 
            endpoint = startpoint

        print(direction)
        print(f"Total Distance: {distance} KM")
    else:
        return "Path not fount"

input_file = open(r"Python\cse422 - Artificial Inteligence\Lab 1\input_file.txt", 'r')
heuristic_table, given_graph = data_extraction(input_file)

city_from = input("Start Node: ")
city_to = input("End Node: ")

if city_from not in given_graph or city_to not in given_graph:
    print("Please provide a valid city name!")
else:
    result = A_star_search(city_from, city_to, given_graph, heuristic_table)