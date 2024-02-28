from gurobipy import *


file1 = open("C:\\Users\\zackt\\OneDrive\\Desktop\\br17.atsp", 'r')
file2 = open("C:\\Users\\zackt\\OneDrive\\Desktop\\ftv35.atsp", 'r')
file3 = open("C:\\Users\\zackt\\OneDrive\\Desktop\\ft53.atsp", 'r')
file4 = open("C:\\Users\\zackt\\OneDrive\\Desktop\\kro124p.atsp", 'r')
files = [file1, file2, file3, file4]

def loopCheck(arr, starter, loop):
    has_loops = False

    return loop, has_loops
def tspAsymmetric(table):
    tsp = Model('Travel')
    node = []
    has_loops = True
    addCons = []
    loops = []
    itteration = 0
    while has_loops:
        for i in range(len(table)):
            node.append([0]*len(table[i]))
            for j in range(len(table[i])):
                if table[i][j] > 0 and i != j:
                    node[i][j] = tsp.addVar(obj = table[i][j], vtype = GRB.BINARY, name = '%dto%d' %((i+1), (j+1)))
        tsp.update()
        if (len(node) > len(node[0])):
          length = len(node)
        else:
          length = len(node[0])
        for i in range(length):
          try:
            qs1 = quicksum(node[i][j] for j in range(len(node[i])) if table[i][j] > 0)
          except:
            qs1 = 0
          try:
            qs2 = quicksum(node[i][j] for i in range(len(node)) if table[i][j] > 0)
          except:
            qs2 = 0
          tsp.addConstr(qs1 + qs2 == 2)
    for loop in addCons:
        loopCon = 0
        for i in range(len(loop) - 1):
            loopCon += node[loop[i]][loop[i + 1]]
        if len(loop) > 0:
            tsp.addConstr(loopCon <= len(loop) - 2)
    tsp.ModelSense = 1
    tsp.optimize()
    cells = []
    cell_counter = 0
    for i in range(len(node)):
        for j in range(len(node[i])):
            if table[i][j] > 0 and node[i][j].X != 0:
                cells.append([i, j])
    loops = []
    loops, has_loops = loopCheck(cells, cells[0][0], loops)
    for loop in loops:
        addCons.append(loop)
    return tsp

for file in files:
    line_counter = 1
    size = 0
    table = []
    curr_line = 0
    curr_num = 0
    for line in file:
        if line_counter == 4:
            words = line.split()
            size = int(words[1])
            table = [[0]*size for i in range(size)]
        if line_counter > 7:
            if(curr_num < size):
                numbers = line.split()
                if 'EOF' in numbers:
                    break
                for num in numbers:
                    table[curr_line][curr_num] = int(num)
                    curr_num += 1
            if curr_num == size:
                curr_num = 0
                curr_line += 1
        line_counter += 1
    tspAsymmetric(table)
