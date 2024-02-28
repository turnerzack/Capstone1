from gurobipy import *

file1 = open('C:/Users/zackt/OneDrive/Desktop/p01_d.txt','r')
file2 = open('C:/Users/zackt/OneDrive/Desktop/gr17_d.txt','r')
file3 = open('C:/Users/zackt/OneDrive/Desktop/five_d.txt','r')
file4 = open('C:/Users/zackt/OneDrive/Desktop/dantzig42_d.txt','r')
file5 = open('C:/Users/zackt/OneDrive/Desktop/att48_d.txt','r')
file6 = open('C:/Users/zackt/OneDrive/Desktop/fri26_d.txt','r')

def loop_check(arr, starter, loop):
  has_loops = False
  deep_copy = []

  for a in arr:
     deep_copy.append(a)
  while sum(len(l) for l in loop) < len(arr):
    cur_arr = deep_copy[0]
    starter = cur_arr[0]
    current = cur_arr[1]
    deep_copy.remove(cur_arr)
    temp = []
    temp.append(starter)
    temp.append(current)
    while current != starter:
      for a in deep_copy:
        if current in a:
          if a[0] == current:
            current = a[1]
            temp.append(current)
            cur_arr = a
            deep_copy.remove(cur_arr)
            break
          else:
            current = a[0]
            temp.append(current)
            cur_arr = a
            deep_copy.remove(cur_arr)
            break
    loop.append(temp)
  current = starter
  count = 0
  has_loops = len(loop) != 1
  if has_loops:
    print("Loops Detected")
    print(loop, len(loop), len(arr))
  else:
    print("No more loops")
    print(loop)
  return loop, has_loops


def tspModelSync(table):
  tsp = Model('Travel')
  has_loops = True
  addCons = []
  loops = []
  itteration = 0
  while(has_loops):
    tsp = Model('Travel')
    node = []
    for i in range(len(table)):
      node.append([0]*len(table[i]))
      for j in range(len(table[i])):
        if table[i][j] > 0:
          node[i][j] = tsp.addVar(obj = table[i][j], vtype = GRB.BINARY, name = '%dto%d' % ((i+1), (j+1)))
    tsp.update()
    qs1 = 0
    qs2 = 0
    length = 0
    if (len(node) > len(node[0])):
      length = len(node)
    else:
      length = len(node[0])
    for i in range(length):
      try:
        qs1 = quicksum(node[i][j] for j in range(len(node[i])) if table[i][j] > 0 and i > j)
      except:
        qs1 = 0
      try:
        qs2 = quicksum(node[k][i] for k in range(len(node)) if table[k][i] > 0 and k > i)
      except:
        qs2 = 0
      tsp.addConstr(qs1 + qs2 == 2)
    for loop in addCons:
      loopCon = 0
      for i in range(len(loop) - 1):
          loopCon += node[loop[i]][loop[i+1]]
          if len(loop) > 3:
            loopCon += node[loop[i+1]][loop[i]]
      if len(loop) > 0:
        tsp.addConstr(loopCon <= len(loop) - 2)
    tsp.ModelSense = 1
    tsp.optimize()
    cells = []
    cell_counter = 0
    for i in range(len(node)):
      for j in range(len(node[i])):
        if table[i][j] > 0 and node[i][j].X != 0:
          cells.append([i,j])
    loops = []
    loops, has_loops = loop_check(cells, cells[0][0], loops)
    for loop in loops:
      addCons.append(loop)
  return tsp

files = [file1, file2, file3, file4, file5, file6]

tsp = []
for file in files:
  table = []
  for line in file:
    current = line.strip().split()
    print(current)
    for i in range(len(current)):
      current[i] = int(float(current[i]))
    table.append(current)
    print(current)
  tsp.append(tspModelSync(table))
for i in range(len(tsp)):
  for v in tsp[i].getVars():
    if v.X != 0:
      print('%6s = %5d' % (v.VarName,v.X))
  print()
  print('Objective Value:', int(tsp[i].ObjVal))
  """
  if i == 0:
    tsp[i].write('C:/Users/zackt/OneDrive/Desktop/p01_d.lp')
  if i == 1:
    tsp[i].write('C:/Users/zackt/OneDrive/Desktop/gr17_d.lp')
  if i == 2:
    tsp[i].write('C:/Users/zackt/OneDrive/Desktop/five_d.lp')
  if i == 3:
    tsp[i].write('C:/Users/zackt/OneDrive/Desktop/dantzig42_d.lp')
  if i == 4:
    tsp[i].write('C:/Users/zackt/OneDrive/Desktop/att48_d.lp')
  if i == 5:
    tsp[i].write('C:/Users/zackt/OneDrive/Desktop/fri26_d.lp')
    """



