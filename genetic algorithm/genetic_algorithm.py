# -*- coding: utf-8 -*-
"""genetic algorithm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ND7sITsrkz8D9ulyGEqEyOqcVjXml5FR

## Population Generation

The first step of the genetic algorithm is to generate an initial population of different states (chromosomes).

Complete the following function. It must generate a population of size $k$ for a graph with $n$ vertices.
"""

def population_generation(n, k): 
    v = np.random.randint(0, 2,(k,n))
    return v

"""## Cost Function

For cost function, we use another, more simple formula for this problem. Because the Genetic algorithm tends to run much longer than simulated annealing, we prefer to use a more simple cost function for this problem.

The cost function for this problem is as follows:
- Add 1 to the cost for each vertex in the answer
- Add 5 (or any other number you prefer) to the cost for each edge that is not covered.
"""

def cost_function2(graph,state):
    n = np.size(graph,axis=0)
    cost = 0
    cost += np.sum(state)
    Nor_Mat = np.ones((n,n))
    for i in range(n):
        if (state[i] == 1): 
                Nor_Mat[i,:] = 0
                Nor_Mat[:,i] = 0
    cost += 5*np.sum(Nor_Mat*graph_matrix)
    return cost

"""## Selection


We select the best chromosomes (states) in the selection phase and allow them to pass to the next generation (iteration). Others will be discarded.

For this part, we use a procedure named "tournament selection." In this procedure, we divide match each element in population with another one and compare their cost. The winner is the one that has a lower cost, and it gets selected for the next part, and the others are discarded.
"""

def tournament_selection(graph, population):
    row,col = np.shape(population)
    new_population = np.zeros((row//2,col))
    for i in range(row//2):
        s0 = population[2*i,:]
        c0 = cost_function2(graph,s0)
        s1 = population[2*i+1,:]
        c1 = cost_function2(graph,s1)
        if (c0<c1):
            new_population[i] = s0
        else:
            new_population[i] = s1
    return new_population

"""## Crossover

In the crossover phase, we combine two chromosomes to get a better chromosome (solution). There are lots of ways to implement crossover. For this problem, we propose this method:

Take two chromosomes as input. Generate a random 'index'. The resulting chromosome consists of genes from chromosome1 from 0 up until 'index' and genes from chromosome2 from 'index+1' until the end. Another chromosome is generated by swapping chromosome1 and chromosome2 and doint the same procedure.
"""

def crossover(graph, parent1, parent2):
    n = len(parent1)
    index = np.random.randint(0, n-1)
    child1 = np.concatenate((parent1[0:index+1],parent2[index+1:n]), axis=0)
    child2 = np.concatenate((parent2[0:index+1],parent1[index+1:n]), axis=0)
    return child1, child2

"""## Mutation

In the mutation part of this problem, we take chromosomes coming out of Crossover and change them slightly in the hope of getting better. There are many ways to implement mutation. We propose two methods here. You can implement each one of them or even both.

For this part, we generate a random number. If this number is greater than the mutation probability, we choose a random index in the chromosome and change it from '0' to '1' or '1' to '0'.
"""

def mutation(graph,chromosme,probability):
    p = random.random()
    n = len(chromosme)
    if p>probability:
        index = np.random.randint(0, n)
        chromosme[index] = 1-chromosme[index]
    return chromosme

"""## Main Algorithm

Now implement the main 'genetic_algorithm' function.
"""

def genetic_algorithm(graph_matrix,mutation_probability=0.1,pop_size=100,max_generation=200):
    n = np.size(graph_matrix,axis=0)
    population = population_generation(n, pop_size)
    counter = 0
    best_cost = cost_function2(graph_matrix,population[0,:])
    best_solution = population[0,:]
    while counter<max_generation:
        new_population = tournament_selection(graph_matrix, population)
        k = np.size(new_population,axis=0)
        for i in range(0,k,2):
            parent1 = new_population[i]
            parent2 = new_population[i+1]
            child1, child2 = crossover(graph_matrix, parent1, parent2)
            parent1 = mutation(graph_matrix,parent1,mutation_probability)
            parent2 = mutation(graph_matrix,parent2,mutation_probability)
            child1 = mutation(graph_matrix,child1,mutation_probability)
            child2 = mutation(graph_matrix,child2,mutation_probability)
            population[2*i]=parent1
            population[2*i+1]=parent2
            population[2*i+2]=child1
            population[2*i+3]=child2
        for i in range(2*k):
            cost = cost_function2(graph_matrix,population[i,:])
            if cost<best_cost:
                best_cost=cost
                best_solution = population[i,:]
        counter += 1
        print(counter,best_cost)
    return best_cost,best_solution

best_cost_GA, best_sol_GA = genetic_algorithm(graph_matrix)