import math
import random
import time
#import matplotlib.pyplot as plt
#import numpy


def objective_1(blocked_hosts):
	value = 6 - blocked_hosts
	return value

def objective_2(failure_cell, failure_channel):
	rel_cell = 0
	rel_channel = 0
	for x in range(0,7):
		rel_cell = rel_cell + (failure_cell[x]*60)

	for x in range(0,140):
		rel_channel = rel_channel + (failure_channel[x]*10)

	value = (math.exp(-rel_cell)) * (math.exp(-rel_channel))
	return value

def index_of(a,list):
    for i in range(0,len(list)):
        if list[i] == a:
            return i
    return -1

#Function to sort by values
def sort_by_values(list1, values):
    sorted_list = []
    while(len(sorted_list)!=len(list1)):
        if index_of(min(values),values) in list1:
            sorted_list.append(index_of(min(values),values))
        values[index_of(min(values),values)] = float('inf')
    return sorted_list

def fast_non_dominated_sort(values1, values2):
    S=[[] for i in range(0,len(values1))]
    front = [[]]
    n=[0 for i in range(0,len(values1))]
    rank = [0 for i in range(0, len(values1))]

    for p in range(0,len(values1)):
        S[p]=[]
        n[p]=0
        for q in range(0, len(values1)):
            if (values1[p] > values1[q] and values2[p] > values2[q]) or (values1[p] >= values1[q] and values2[p] > values2[q]) or (values1[p] > values1[q] and values2[p] >= values2[q]):
                if q not in S[p]:
                    S[p].append(q)
            elif (values1[q] > values1[p] and values2[q] > values2[p]) or (values1[q] >= values1[p] and values2[q] > values2[p]) or (values1[q] > values1[p] and values2[q] >= values2[p]):
                n[p] = n[p] + 1
        if n[p]==0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)

    i = 0
    while(front[i] != []):
        Q=[]
        for p in front[i]:
            for q in S[p]:
                n[q] =n[q] - 1
                if( n[q]==0):
                    rank[q]=i+1
                    if q not in Q:
                        Q.append(q)
        i = i+1
        front.append(Q)

    del front[len(front)-1]
    return front

def crowding_distance(values1, values2, front):
    distance = [0 for i in range(0,len(front))]
    sorted1 = sort_by_values(front, values1[:])
    sorted2 = sort_by_values(front, values2[:])
    distance[0] = 4444444444444444
    distance[len(front) - 1] = 4444444444444444
    for k in range(1,len(front)-1):
        distance[k] = distance[k]+ (values1[sorted1[k+1]] - values2[sorted1[k-1]])/(max(values1)-min(values1))
    for k in range(1,len(front)-1):
        distance[k] = distance[k]+ (values1[sorted2[k+1]] - values2[sorted2[k-1]])/(max(values2)-min(values2))
    return distance

def matrix_crossover(index1, index2, population):
	matrix1 = population[index1]
	matrix2  = population[index2]
	matrix3 = list()
	matrix4 = list()
	for i in range(0,7):
		arr1 = [0 for j in range(0,14)]
		arr2 = [0 for j in range(0,14)]
		arr1[0:7] = matrix2[i][0:7]
		arr2[0:7] = matrix1[i][0:7]
		list1 = matrix1[i][7:14]
		list2 = matrix2[i][7:14]
		common_list1 = [x for x in list2 if x in list1]
		common_list2 = [x for x in list1 if x in list2]
		if(len(common_list1) == 7):
			common_list1 = list1
			arr1[7:14] = common_list1
		else:
			#uncommon_list = [x for x in list1 if x not in common_list]
			j = 0
			for k in range(0,7):
				if(list1[k] not in common_list1):
					arr1[k+7] = list1[k]
				else:
					arr1[k+7] = common_list1[j]
					j = j+1

		if(len(common_list2) == 7):
			common_list2 = list2
			arr2[7:14] = common_list2
		else:
			#uncommon_list = [x for x in list1 if x not in common_list]
			j = 0
			for k in range(0,7):
				if(list2[k] not in common_list2):
					arr2[k+7] = list2[k]
				else:
					arr2[k+7] = common_list2[j]
					j = j+1
		matrix3.append(arr1)
		matrix4.append(arr2)
	# population1.append(matrix3)
	# population1.append(matrix4)
	return matrix3,matrix4

def update(matrix1, matrix2,demand_channels, population1):

	for row in range(0,7):
		if(demand_channels[row] > matrix1[row][1]):
			matrix1[row][2:8] = [0,0,0,0,0,0,0]
			diff = demand_channels[row] - matrix1[row][1]
			matrix1[row][1] = 0
			count = 0
			while(count < diff):
				for neighbour in range(0,7):
					if(neighbour!=row):
						if(matrix1[neighbour][1] > 0):
							if(matrix1[neighbour][1] >= (diff-count) ):
								matrix1[neighbour][1] = matrix1[neighbour][1] - (diff-count)
								matrix1[neighbour][2+row] = diff-count 
								matrix1[row][8+neighbour] = diff-count 
								count = diff
							else:
								count = count + matrix1[neighbour][1]
								matrix1[neighbour][2+row] = matrix1[neighbour][1]
								matrix1[row][8+neighbour] = matrix1[neighbour][1]
								matrix1[neighbour][1] = 0
					if(count == diff):
						break
				if(count<diff):
					matrix1[row][0] = matrix1[row][0] + diff - count    #NO OF BLOCKED HOSTS ARE INCREASED
					break
		else:
			matrix1[row][0] = 0
			matrix1[row][8:14] = [0,0,0,0,0,0,0]
			matrix1[row][1] = matrix1[row][1] - demand_channels[row]

		if(demand_channels[row] > matrix2[row][1]):
			matrix2[row][2:8] = [0,0,0,0,0,0,0]
			diff = demand_channels[row] - matrix2[row][1]
			matrix2[row][1] = 0
			count = 0
			while(count < diff):
				for neighbour in range(0,7):
					if(neighbour!=row):
						if(matrix2[neighbour][1] > 0):
							if(matrix2[neighbour][1] >= (diff-count) ):
								matrix2[neighbour][1] = matrix2[neighbour][1] - (diff-count)
								matrix2[neighbour][2+row] = diff-count 
								matrix2[row][8+neighbour] = diff-count
								count = diff
							else:
								count = count + matrix2[neighbour][1]
								matrix2[neighbour][2+row] = matrix2[neighbour][1]
								matrix2[row][8+neighbour] = matrix2[neighbour][1]
								matrix2[neighbour][1] = 0
					if(count == diff):
						break
				if(count<diff):
					matrix2[row][0] = matrix2[row][0] + diff - count    #NO OF BLOCKED HOSTS ARE INCREASED
					break
		else:
			matrix2[row][0] = 0
			matrix2[row][8:14] = [0,0,0,0,0,0,0]
			matrix2[row][1] = matrix2[row][1] - demand_channels[row]

	return matrix1,matrix2

# def crossover(index1, index2, population, population1):
#  	chrom1 = population[index1]
#  	chrom2 = population[index2]
#  	chrom3 = list()
#  	chrom4 = list()
#  	for i in range(0,20):
#  		mat1 = chrom1[0]
#  		mat2 = chrom2[0]
#  		mat3,mat4 = matrix_crossover(mat1,mat2)
#  		chrom3.append(mat3)
#  		chrom4.append(mat4)
#  	population1.append(chrom3)
#  	population1.append(chrom4)
 	
 	#for i in range(0,7):

def random_select(population,population1,demand_channels):
	pop = 0
	#random.seed(time.clock())
	while(len(population1)<len(population)):
		a = random.sample(range(0,99), 2)
		rand1 = a[0]
		rand2 = a[1]
		mat1,mat2 = matrix_crossover(rand1,rand2,population)
		if(len(population1)==2):
			print(mat1)
			print("")
			print("")
			print("")
			print("")
		mat1,mat2 = update(mat1,mat2,demand_channels,population1)
	
		if(len(population1)==2):
			# print(mat1)
			print("")
		population1.append(mat1)
		population1.append(mat2)
		pop = pop + 1
	return population,population1


pop_size = 100
max_no_of_hosts = 140
max_gen = 1000
no_of_cells = 20
#NO. OF CELLS IN A CLUSTER = 7
demand_channels = random.sample(range(1,20), 7)

population_set = list()
chrom = list()

#random.seed(time.clock())

count = 0
for j in range(0,pop_size):
	count = 0
	chrom = list()
	a = random.sample(range(1,20), 7)
	for z in range(0,7):
		rand = [0 for i in range(0,14)]
		rand[1] = 14
		rand[0] = a[count]
		count = count + 1
		chrom.append(rand)
		#chrom.append(super_gene)
	population_set.append(chrom)

# print(a)
# #print(len(chrom))
# #print(chrom)
#print(demand_channels)
gen = 0
while(gen < 1):
	population_set1 = list()
	population_set, population_set1 = random_select(population_set,population_set1,demand_channels)
	combined_population = list()
	#print(population_set1[0])
	combined_population = population_set + population_set1
	function1_values = list()
	function2_values = list()

	for i in range(0,len(combined_population)):
		sum = 0
		for j in range(0,7):
			sum = sum + objective_1(combined_population[i][j][0])
		function1_values.append(sum)
		failure_cell = [random.uniform(0.2,0.5) for i in range(0,7)]
		failure_channel = [random.uniform(0.5,0.9) for i in range(0,140)]
		function2_values.append(objective_2(failure_cell, failure_channel))

	front = fast_non_dominated_sort(function1_values[:], function2_values[:])

	count = 0

	for i in range(0,len(front)):
		for j in range(0,len(front[i])):
			population_set.append(combined_population[front[i][j]])
			count = count + 1
		if(count == 100):
			break
	gen = gen + 1
print("")
print("")
print("")

#print(population_set[80])

#distance = list()
#print(front)

# for x in range(0,len(front)):
# 	distance.append(crowding_distance(function1_values[:], function2_values[:], front[x]))

# new_solution= []
# for i in range(0,len(front)):
# 	non_dominated_sorted_solution2_1 = [index_of(front[i][j],front[i] ) for j in range(0,len(front[i]))]
# 	front22 = sort_by_values(non_dominated_sorted_solution2_1[:], distance[i][:])
# 	front1 = [front[i][front22[j]] for j in range(0,len(front[i]))]
# 	front1.reverse()
# 	for value in front1:
# 		new_solution.append(value)
# 		if(len(new_solution)==pop_size):
# 			break
# 		if (len(new_solution) == pop_size):
# 			break
# solution = [combined_population[i] for i in new_solution]
	
#print(solution)
# print(population_set[0])
# print(population_set1[0])
# print(len(population_set))
# print(len(population_set1))
# for y in range(0,7):
# 	print(chrom[y])
# for y in range(0,2):
# 	print(population_set[y])
