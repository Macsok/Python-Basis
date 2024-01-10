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
        
#Save provided array of processes to file
def processes_to_file(proc_array, file_name):
    df = pd.DataFrame({'WhenArrived' : [x[0] for x in proc_array], 'RunningTime' : [x[1] for x in proc_array]})
    df.to_csv(file_name, index=False)

#plot arrays on one plot
def plot_from_arrays(arrays_in_array, id_of_parameter, label_array):
    label = 0
    for array in arrays_in_array:
        plt.plot([i for i in range(len(array))], [elem[id_of_parameter] for elem in array], label=label_array[label])
        #plt.plot([i for i in range(len(array))], [elem[id_of_parameter + 1] for elem in array])
        label += 1
    plt.ylabel('waiting time')
    plt.xlabel('process')
    plt.legend(loc='upper left')
    plt.show()

#Random Processes Generator - Customize to get different results
def generate_random_processes(numb_of_proc):
    proc = []
    for i in range(numb_of_proc):
        #append random number   [when_arrive, time_to_complete]

        proc.append([random.randrange(0, 101), random.randrange(1, 11)])
        #proc.append([0, random.randrange(1, 11)])
    return proc

#Analyse
def analyse_processes(numb):
    #generate new example

    file = '125_rand.csv'

    processes_to_file(generate_random_processes(numb), file)
    array = array_from_file(file)

    #run simulations
    SJF = symulate_SJF(array)
    FCFS = symulate_FCFS(array)
    LCFS = symulate_LCFS(array)

    #calculate mean
    SJF_sum = 0
    LCFS_sum = 0
    FCFS_sum = 0
    for i in range(len(SJF)):
        SJF_sum += SJF[i][0]
        LCFS_sum += LCFS[i][0]
        FCFS_sum += FCFS[i][0]
    
    SJF_mean = SJF_sum/len(SJF)
    FCFS_mean = FCFS_sum/len(FCFS)
    LCFS_mean = LCFS_sum/len(LCFS)

    print(f'Means:\nSJF: {SJF_mean}\nFCFS: {FCFS_mean}\nLCFS: {LCFS_mean}')

    #compare results
    plot_from_arrays([SJF, FCFS, LCFS], 1, ['SJF', 'FCFS', 'LCFS'])

#--------------

analyse_processes(125)