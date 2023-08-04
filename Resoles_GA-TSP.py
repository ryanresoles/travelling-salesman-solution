import random 
import string

MAXPOP = 100
PATHS = []
ADJ_MATRIX = []
ALPHABET = list(string.ascii_uppercase)
TOTAL_FITNESS = 0
TOTAL_CHANCE = 0
PAIR_COUNT = 2
GENERATION = 0
INITIAL_POPULATION = 10
MAX_ITER = 100

class Path:
    def __init__(self, path):
        self.path = path
        self.fitness = self.calculate_fitness()
        self.chance = 0

    def calculate_fitness(self):
        total = 0
        row = 0

        for i in range(len(self.path)-1):
            
            if self.path[i] < self.path[i+1]:
                row = ALPHABET.index(self.path[i+1])
                col = ALPHABET.index(self.path[i])
            else:
                row = ALPHABET.index(self.path[i])
                col = ALPHABET.index(self.path[i+1])

            total += ADJ_MATRIX[row][col]

        return total

    def mutate(self, newChrom):
        self.chrom = newChrom
        self.fitness = self.calculate_fitness()

## mutation swaps cities from path (e.g. ABCDA -> ADCBA)
def mutation(individual):
    x = random.randint(0,len(individual.path)-2)
    y = random.randint(0,len(individual.path)-2)

    new_path = individual.path[:x] + individual.path[y] + individual.path[x+1:y] + individual.path[x] + individual.path[y+1:]
    individual.mutate(new_path)

# crossover using order crossover, swaps every bit
# except bits appearing in selected portion
def order_crossover(mating_population, vertices):
    offsprings_holder = []
    os = []

    temp = random.sample(range(1, vertices), 2)
    if temp[0] > temp[1]:
        t = temp[0]
        temp[0] = temp[1]
        temp[1] = t

    for i in mating_population:
        os = (['0']*temp[0]) + [*PATHS[i[0]].path[temp[0]:temp[1]]] + (['0']*(vertices-temp[1]))
        #print(len(PATHS[i[0]].path)-1, PATHS[i[0]].path, temp[0], temp[1], os)
        iter = 0

        for j in range(len(os)):
            for k in PATHS[i[1]].path:
                if os[j]=='0' and k not in os:
                    os[j] = k
                    iter+=1

        
        os.append(os[0])
        #print(os)
        offsprings_holder.append(''.join(os))

    return offsprings_holder                                   

def selection():
    pairs = []

    # roulette wheel implementation
    for i in range(PAIR_COUNT):
        temp = random.sample(range(0,TOTAL_CHANCE+1), 2)
        
        ind1, ind2 = 0, 0
        for j in range(1,len(PATHS)):
            if temp[0] > PATHS[j].chance:
                ind1 = j
            if temp[1] > PATHS[j].chance:
                ind2 = j    
        pairs.append((ind1,ind2))    

    # returns indices of pairs in POPULATION list
    return pairs   


# Funcion for updating chance of selection (in case of mutation/addition of new individuals)
def compute_chance():
    chance = 0

    for i in PATHS:
        chance += (TOTAL_FITNESS - i.fitness)
        i.chance = chance

    global TOTAL_CHANCE
    TOTAL_CHANCE = chance

# Funcion for updating fitness (in case of mutation/addition of new individuals)
def compute_fitness():
    fitness = 0

    for i in PATHS:
        fitness += (i.fitness)

    global TOTAL_FITNESS
    TOTAL_FITNESS = fitness

def addOffsprings(offsprings):
    for i in offsprings:
        if len(PATHS) < MAXPOP: PATHS.append(Path(i))
        else: PATHS[PATHS.index(max(PATHS,key=lambda x:x.fitness))] = Path(i)
            

###########################################################
######################## MAIN CODE ########################          
###########################################################
if __name__ == "__main__":
    edges=30
    start=0

    while(edges>26 or edges<1):
        edges = int(input("Enter number of edges/cities (max input:26): "))    
    for i in range(edges):
        path = []
 
        for j in range(i+1):
            if i==j:
                path.append(0)
                break
            path.append(random.randint(0, 10))
        ADJ_MATRIX.append(path)

    for i in range(INITIAL_POPULATION):
        path_str = ""
        for j in range(edges):
            path_str += ALPHABET[j]
        
        PATHS.append(path_str)


    for i in range(len(ADJ_MATRIX)):
        print(ADJ_MATRIX[i])

    # creates 'Path' object
    for i in range(len(PATHS)):
        path_str = ''.join(random.sample(PATHS[i], len(PATHS[i])))
        PATHS[i] = Path(path_str + path_str[0])
    compute_fitness()
    compute_chance()
    counter = 0
    
    MAX_ITER = int(input("Enter number of iterations: "))

    while(counter < MAX_ITER):
        counter += 1
        
        for i in PATHS:
            mut_rate = random.randint(1,100)
            if mut_rate==1:
                mutation(i)

        if start==0:
            ind = min(PATHS, key=lambda x:x.fitness)
            print(f'GEN{GENERATION+1}: path:{ind.path} | fitness:{ind.fitness}')
            start+=1     

        # for i in range(len(PATHS)):
        #     print(i, PATHS[i].path, PATHS[i].fitness)

        mating_population = selection()
        offsprings = order_crossover(mating_population, edges)

        # adds offsprings to population
        addOffsprings(offsprings)
        compute_fitness()
        compute_chance()


        # recomputes chance of getting selected
        compute_chance()
        GENERATION+=1
        ind = min(PATHS, key=lambda x:x.fitness)
        
        print(f"GEN{GENERATION}: path:{ind.path} | cost:{ind.fitness} | chance:{ind.chance}")
    
    print(f'OPTIMAL PATH: path:{ind.path} | cost:{ind.fitness}')