import random
import string

ALPHABET = list(string.ascii_uppercase)
ADJ_MATRIX = []

# each ant has 10 pheromone to spread in each path
class Ant:
    def __init__(self, ant_no):
        self.no = ant_no
        self.path = []
        self.cost = 0

    def add_city(self, city):
        self.path.append(city)

    def update_cost(self, addedcost):
        self.cost += addedcost

    def reset(self):
        self.path = []
        self.cost = 0

class City:
    def __init__(self, city_name):
        self.city_name = city_name
        self.probability = 10

    def update_probability(self, pheromone):
        self.probability = pheromone

# COMPUTES TOTAL PROBABILITY OF CITIES NOT VISITED BY ANT
def compute_prob(city_list, cities):
    total = 0
    
    for i in cities:
        total += next(x for x in city_list if x.city_name==i).probability

    return total

# SELECTS NEXT CITY TO BE EXPLORED
def find_path(ant, cities, prob):
    temp = random.uniform(0, prob)

    for i in cities:
        city_prob = next(x for x in city_list if x.city_name==i)
        if temp > city_prob.probability:
            temp -= city_prob.probability
            continue
        
        # next city is found
        ind1 = ALPHABET.index(ant.path[-1])
        ind2 = ALPHABET.index(city_prob.city_name)

        if ind1 < ind2:
            temp = ind1
            ind1 = ind2
            ind2 = temp
        
        city_cost = ADJ_MATRIX[ind1][ind2][0]
        ant.add_city(city_prob.city_name)
        ant.update_cost(city_cost)
        ADJ_MATRIX[ind1][ind2][1].append(10/city_cost)
        city_pheromone = sum(ADJ_MATRIX[ind1][ind2][1])

        city_prob.update_probability(city_pheromone)
        break



###########################################################
######################## MAIN CODE ########################          
###########################################################
if __name__ == "__main__":
    city_list = []
    ant_list = [] 
    best_solution = []
    ant_count = edges = start = total_prob = num_iter = 0

    while(edges>26 or edges<3):
        edges = int(input("Enter number of edges/cities (range: 3-26): "))
    while(ant_count<5):
        ant_count = int(input("Enter number of ants (min input:5): "))

    # INITIALIZATION OF CITIES
    for i in range(edges):
        path = []
        city_list.append(City(ALPHABET[i]))
        total_prob += city_list[i].probability

        for j in range(i+1):
            if i==j:
                path.append([0, []])
                break
            path.append([random.randint(1, 10), []])
        ADJ_MATRIX.append(path)

    for i in range(ant_count):
        ant_list.append(Ant(str(i)))
    
    # ADJ MATRIX FORMAT PER ELEMENT: (cost, pheromone values)
    print("")
    for i in range(len(ADJ_MATRIX)):
        print(f"City {ALPHABET[i]}: {ADJ_MATRIX[i]}")

    for i in range(edges): print(f"| [{i+1}] City {ALPHABET[i]} ", end="")

    while start>(edges+1) or start<1:
        start = int(input("|\nSelect starting city: "))

    while num_iter < 1:
        num_iter = int(input("\nEnter number of iterations: "))

    # MAIN LOOP FOR ACO-TSP TRIALS
    ctr = 0
    ant_no = 0
    while ctr < num_iter:
        #every 3 iterations, initial pheromone trail evaporates
        if ctr%2==0:
            for i in range(len(ADJ_MATRIX)):
                for j in range(len(ADJ_MATRIX[i])):
                    ADJ_MATRIX[i][j][1] = ADJ_MATRIX[i][j][1][1:]


        ctr+=1 
        for i in ant_list: i.add_city(ALPHABET[start-1])

        for i in range(len(city_list)-1):
            for j in ant_list:
                visited = [item for item in ALPHABET[:edges] if item not in j.path]
                prob = compute_prob(city_list, visited)
                find_path(j, visited, prob)

        for i in ant_list:
            ind1 = ALPHABET.index(i.path[0])
            ind2 = ALPHABET.index(i.path[-1])

            if ind1 < ind2:
                temp = ind1
                ind1 = ind2
                ind2 = temp

            i.path.append(i.path[0])
            i.update_cost(ADJ_MATRIX[ind1][ind2][0])
        
        shortest = min(ant_list, key=lambda x:x.cost)
        if len(best_solution)==0 or best_solution[1] > shortest.cost:
            best_solution = [shortest.path,shortest.cost]

        print(f"ITERATION#{ctr}\t|\tShortest path:{shortest.cost} | Path:{shortest.path} | Discovered by:{shortest.no}")

        for i in ant_list:
            i.reset()
    
    print(f"\nBEST PATH: {best_solution[0]} | COST: {best_solution[1]}")