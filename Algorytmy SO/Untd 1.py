#Let process be an array of an array: a[index] = [process_arrive, process_execution_time]
#We read whole queue from file and then, in each step, add some of them on the heap and run one.

import pandas as pd
import random
from matplotlib import pyplot as plt

#Create array [[arrive_time, execution_time], ...]
def array_from_file(file_path):
    #read file as DataFrame
    df = pd.read_csv(file_path)
    proc_array = []
    #append elements to the list
    for index, row in df.iterrows():
        proc_array.append([row['WhenArrived'], row['RunningTime']])
    return proc_array

#Returns updated arrays of process_array and heap
def update_heap(process_array, heap, current_time):
    #add element if the time for it has passed
    heap += [elem for elem in process_array if elem[0] <= current_time]
    #remove moved processes
    process_array = [elem for elem in process_array if elem[0] > current_time]
    return process_array, heap

#Shortest Job First
def symulate_SJF(proc_array, steps = False):
    time = 0
    heap = []
    wait_time = []
    while proc_array != [] or heap != []:
        #update arrays
        proc_array, heap = update_heap(proc_array, heap, time)
        if steps:
            if heap != []: print(f'[{time}ms] updating arrays... Current queue [arriv., exec. time]: {heap}')
        
        #wait if queue is empty
        if heap == []:
            time += 1
        else:
            #find shortest job
            min = heap[0]
            for elem in heap:
                if min[1] > elem[1]:
                    min = elem
            #save waiting, end of process time
            wait_time.append([time - min[0], time + min[1] - min[0]])
            #remove (one) min element from heap
            heap.remove(min)

            #Execute process - add time
            if steps: print(f'Executing process for {min[1]}ms\n')
            time += min[1]
    if steps: print(f'Finished symulation at {time}ms')
    return wait_time

#Round Robin (with time slice), steps=True to display every step
def symulate_RoundRobin(proc_array, time_slice = 10, steps = False):
    time = 0
    wait_time = []
    heap = []
    while proc_array != [] or heap != []:
        #update arrays
        proc_array, heap = update_heap(proc_array, heap, time)
        if steps:
            if heap != []: print(f'[{time}ms] updating arrays... Current queue [arriv., exec. time]: {heap}')

        #wait if queue is empty
        if heap == []:
            #wait
            time += 1
        else:
            #do first job in queue for one time slice
            if heap[0][1] > 10:
                #append partly-processed process to the end of queue
                heap.append([heap[0][0], heap[0][1] - 10])
                heap.pop(0)
                if steps: print(f'[{time}ms] Executed process for 10ms ({heap[-1][1]}ms left).')
                #add execution time
                time += 10
            else:
                #add execution time
                time += heap[0][1]
                #save start of processing
                #wait_time.append([])
                if steps: print(f'[{time}ms] Executed process for {heap[0][1]}ms (process finished).')
                heap.pop(0)
    if steps: print(f'Finished symulation at {time}ms')
    return time

#First Come First Serve
def symulate_FCFS(proc_array, steps = False):
    time = 0
    wait_time = []
    heap = []
    while proc_array != [] or heap != []:
        #update arrays
        proc_array, heap = update_heap(proc_array, heap, time)
        if steps:
            if heap != []: print(f'[{time}ms] updating arrays... Current queue [arriv., exec. time]: {heap}')
        
        #wait if queue is empty
        if heap == []:
            time += 1
        else:
            #execute first job
            if steps: print(f'[{time}ms] Executed process for {heap[-1][1]}ms (process finished).')
            #save time exec.
            wait_time.append([time - heap[0][0], time - heap[0][0] + heap[0][1]])

            time += heap[0][1]
            #remove first element
            heap.pop(0)
            
    if steps: print(f'Finished symulation at {time}ms')
    return wait_time

#Last Come First Serve
def symulate_LCFS(proc_array, steps = False):
    time = 0
    wait_time = []
    heap = []
    while proc_array != [] or heap != []:
        #update arrays
        proc_array, heap = update_heap(proc_array, heap, time)
        if steps:
            if heap != []: print(f'[{time}ms] updating arrays... Current queue [arriv., exec. time]: {heap}')
        
        #wait if queue is empty
        if heap == []:
            time += 1
        else:
            #execute latest job
            if steps: print(f'[{time}ms] Executed process for {heap[-1][1]}ms (process finished).')
            #save time stamps
            wait_time.append([time - heap[-1][0], time - heap[-1][0] + heap[-1][1]])

            time += heap[-1][1]
            #remove first element
            heap.pop()
            
    if steps: print(f'Finished symulation at {time}ms')
    return wait_time
        
def generate_random_processes(numb_of_proc):
    proc = []
    for i in range(numb_of_proc):
        #append random number
        proc.append([random.randrange(0, 10000), random.randrange(50, 100)])
        #proc.append([0, random.randrange(5, 250)])
    return proc

#Save provided array of processes to file
def processes_to_file(proc_array, file_name):
    df = pd.DataFrame({'WhenArrived' : [x[0] for x in proc_array], 'RunningTime' : [x[1] for x in proc_array]})
    df.to_csv(file_name, index=False)

#plot arrays on one plot
def plot_from_arrays(arrays_in_array, id_of_parameter):
    for array in arrays_in_array:
        plt.plot([i for i in range(len(array))], [elem[id_of_parameter] for elem in array])
        #plt.plot([i for i in range(len(array))], [elem[id_of_parameter + 1] for elem in array])
    plt.show()

#Analyse
def analyse_processes():
    #generate new example
    processes_to_file(generate_random_processes(55), 'proc_2.csv')

    #run simulations
    SJF = symulate_SJF(array_from_file('proc_2.csv'))
    FCFS = symulate_FCFS(array_from_file('proc_2.csv'))
    LCFS = symulate_LCFS(array_from_file('proc_2.csv'))

    #compare results
    plot_from_arrays([SJF, FCFS, LCFS], 0)

#--------------------------------
#   Virtual Memory
    
#read data from file
def read_array(file_path):
    arr = []
    file = open(file_path, 'r')
    content = file.read()
    for line in content.split('\n'):
        arr.append(int(line))
    return arr

#Generate array of rand. numbers
def generate_random_array(length, from_ = 0, to_ = 9):
    arr = []
    for i in range(length + 1):
        arr.append(random.randrange(from_, to_ + 1))
    return arr

#First In First Out
def symulate_FIFO(array, queue_size = 4):
    queue = []
    for i in range(queue_size):
        queue.append(-1)

    swaps = 0
    ind = 0

    #swap elements
    for element in array:
        if element not in queue:
            #add element
            queue[ind] = element
            swaps += 1

            #change index
            if ind < queue_size - 1:
                ind += 1
            else:
                ind = 0
    return swaps

#Least Recently Used
def symulate_LRU(array, queue_size = 4, steps = False):
    queue = []
    when_used = []
    #create array
    for i in range(queue_size):
        queue.append(-1)
        when_used.append(-queue_size + i)

    swaps = 0

    #swap elements
    for element in array:
        if element in queue:
            #update time of usage
            when_used[queue.index(element)] = swaps
            if steps: print(f'update {element}, id {queue.index(element)} to {swaps}')
            #note: no need to swap element, no swapping

        #if not in queue
        else:
            #update swaps
            swaps += 1

            #find minimum (less - used least recently)
            min = when_used[0]
            if steps: print(f'when used {when_used}')
            for x in range(len(when_used)):
                if when_used[x] < min:
                    #update wanted element
                    min = when_used[x]
            
            if steps: print(f'replacing element, minimum at index {when_used.index(min)}')
            #swap element
            queue[when_used.index(min)] = element
            #update when_used
            when_used[queue.index(element)] = swaps
            
        if steps: 
            print(queue)
            print('\n')

    return swaps

print(symulate_FIFO(read_array('strony.txt')))
print(symulate_LRU(read_array('strony.txt')))