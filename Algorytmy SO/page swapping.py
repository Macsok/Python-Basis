import random
from matplotlib import pyplot as plt

#   Virtual Memory
    
#read data from file
def read_array(file_path):
    arr = []
    file = open(file_path, 'r')
    content = file.read()
    for line in content.split('\n'):
        if line != '': arr.append(int(line))
    return arr

#Save provided array to file
def array_to_file(array, file_name):
    with open(file_name, 'w') as txt_file:
        for line in array:
            txt_file.write(str(line) + "\n")

#Generate array of rand. numbers
def generate_random_array(length, from_ = 0, to_ = 10):
    arr = []
    for i in range(length):
        arr.append(random.randrange(from_, to_ + 1))
    return arr

#Generate array of rand. numbers where every second number is X
def generate_random_array_diffrent(length, from_ = 0, to_ = 10, numb = 1):
    arr = []
    for i in range(length):
        if i%2 == 0: arr.append(random.randrange(from_, to_ + 1))
        else: arr.append(numb)
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
        
        #print steps
        if steps: 
            print(queue)
            print('\n')

    return swaps

def analyse_pages(length_of_array):
    #rand_arr = generate_random_array(length_of_array, 0, 5)
    rand_arr = generate_random_array_diffrent(length_of_array, 0, 10, 5)
    #rand_arr = read_array('zapis.txt')

    #array_to_file(rand_arr, 'zapis.txt')

    x = symulate_FIFO(rand_arr)
    y = symulate_LRU(rand_arr)

    #print(f'Results:\n[FIFO] swaps: {x}\n[LRU] swaps: {y}')
    return [x, y]   #FIFO, LRU

def analyse_multiple(times, save_to, len_):
    arr = []
    #clear file
    with open(save_to, 'w') as txt_file:
        txt_file.write('\n')

    #generate array of results
    for i in range(times + 1):
        buff = analyse_pages(len_)
        #append to a file
        with open(save_to, 'a') as txt_file:
            for line in buff:
                txt_file.write(str(line) + "\n")
            txt_file.write("\n")
        arr.append(buff)

    #sum
    FIFO_sum = 0
    LRU_sum = 0
    for el in arr:
        FIFO_sum += el[0]
        LRU_sum += el[1]
    
    #calculate means
    FIFO_mean = FIFO_sum/len(arr)
    LRU_mean = LRU_sum/len(arr)
    #print means
    print(f'Means:\nFIFO: {FIFO_mean}\nLRU: {LRU_mean}')

    plt.plot([x for x in range(len(arr))], [x[0] for x in arr], label='FIFO')
    plt.plot([x for x in range(len(arr))], [x[1] for x in arr], label='LRU')
    plt.xlabel('n-th test')
    plt.ylabel('swaps')
    plt.legend(loc='upper left')
    plt.show()

#-------------


#analyse_pages(20)
analyse_multiple(100, '200_5.txt', 200)