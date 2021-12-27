import time
randef=input('would you like to generate a random problem or a predefined one is ok? 1 or other: ')
if randef=='1':
    n=int(input('Please enter the number of items you would like to put in the knapsack: '))+1
    import random
# Problem Generator Function
    def Problem_Generator(n):
        w=[]                                   #weight of items
        v=[]                                   #value of each item
        for i in range(1,n):
            w.append(random.randint(2,10))
            v.append(random.randint(25,45))
            sum_items=sum(w)                   # sum of the items' weight
            C=int(0.85*sum_items)              # option 1 to generate C
        #     C=float('inf')                   # option 2 to generate C
        # while sum_items<C:    
        #     C=random.randint(18,35)                             
            vperw=[]                           # value per weight for each item
        for i,j in enumerate(w):
            vperw.append(round(v[i]/j,2))
        return [C,w,v,sum_items,vperw]
    Problem=Problem_Generator(n)
    C=Problem[0]
    w=Problem[1]
    v=Problem[2]
    sum_items=Problem[3]
    vperw=Problem[4]
else:
    n=9
    C=29 
    w=[3, 3, 5, 6, 4, 5, 8, 6, 4]
    v=[32, 34, 36, 35, 28, 36, 45, 27, 33]
    sum_items=44
    vperw=[10.67, 11.33, 7.2, 5.83, 7.0, 7.2, 5.62, 4.5, 8.25]

print(' A Knapsack problem is genrated\n C={} \n w={}'.format(C,w))
print(' v={}\n sum_items={}\n vperw={}'.format(v,sum_items,vperw))
#------------------------------------------------------------------------------
traversal='BestF'
start_time = time.time()
#The class of items to define their attributes
class node_gen:
    def __init__(self, level, value, weight):
        self.level = level
        self.value = value
        self.weight = weight
        self.selected = []
        self.opt = []
        self.side= []
#------------------------------------------------------------------------------        

#Linear Relaxation Solution (An optimistic solution to the problem)
def LRS(node):
    if node.weight >= C:
        return 0
    else:
        Opt_val = node.value                                  #Optimistic value
        totalweight = node.weight
        order=sorted(range(len(vperw)), key=lambda k: vperw[k], reverse=True)
        for rem in range(node.level+1):
            order.remove(rem)
        for j in order:
            if totalweight + w[j] <= C:
                totalweight = totalweight + w[j]
                Opt_val = Opt_val + v[j]  
            else:
                Opt_val=Opt_val + round((C-totalweight)*vperw[j],3)
    return Opt_val                                            #Optimistic value

#------------------------------------------------------------------------------
class Queue:     # We need to have control over what happens in the queue of nodes to be investigated
    def __init__(self):         # this queue has two attributes:
        self.Q = []             # Q to have access to traversed nodes
        self.length = 0         # length to see whether the queue is empty or not
    def add(self, node):        # add method: we define this to add traversed nodes to the queue
        if traversal=='BestF':  # if you choose Best first traversal strategy,
                                # the algorithm will place the added nodes in order based their
                                # their optimistic objective
            i=0                 # we should set the default value of i to zero since the queue can be empty
            for i in range(self.length):    # we find the place where the new node doesn't disrupt
                                            # the ascending order of the nodes based on their optimistic values
                if self.Q[i].opt > node.opt:
                    break
            self.Q.insert(i,node)
            self.length += 1
            
        elif traversal=='DepthF' or traversal=='BreadthF':  # if you choose to use DepthFirst or BreadthFirst strategies
                                                            # you should add new nodes to the queue chronologically
            self.Q.insert(self.length,node)
            self.length += 1
                
    def remove(self):           
      # Selecting the traversal branch as Best First to proceed with exploration  
        if traversal=='BestF':
            if self.length != 0:            # the BestFirst strategy tends to choose 
                                            # the most optimistic node to begin exploration
                result = self.Q.pop()
                self.length -= 1
                return result
          
     # Selecting the traversal branch as Breadth First to proceed with exploration           
        elif traversal=='BreadthF':         # the BreadthFirst strategy tends to choose
                                            # the node that has stayed in the queue the longest
            if self.length != 0:
                result = self.Q.pop(0)
                self.length -= 1
                return result

     # Selecting the traversal branch as Depth First to proceed with exploration
        elif traversal=='DepthF':           # the DepthFirst strategy tends to go 
                                            # deep enough until it reaches a deadend
                                            # so long as there is a left side branch,
                                            # we would not go to right
            if self.length>=2:
                if  self.Q[-1].side == 'right' and  self.Q[-2].side=='left':
                    result = self.Q.pop(self.length-2)
                else:
                    result = self.Q.pop()
                self.length -= 1
                return result
            elif self.length == 1:
                result = self.Q.pop()
                self.length -= 1
                return result

#------------------------------------------------------------------------------
Traversal_queue = Queue()
prt = node_gen(-1, 0, 0) # The Parent (ancestor) node in the tree (here it's the root)
                     # 1st argument: the level of the node in the tree. 
                     # this level represents items we are trying to put it the knapsack
                     # 2nd argument: the value of the item
                     # 3rd argument: the weight of the item
                     # obviously the value and weight would be zero for the root
                     # and since the index of items begins from zero, the root's 
                     # level is set to -1
nodes=1              # this updating variable will show us how many nodes we have
                     # in the tree
Objective = 0        # this updating variable will show us the value we obtained
prt.opt = LRS(prt)   # the optimistic value of the objective function (after linear relaxation)
print('\n Optimistic Value of the Knapsack after\n Linear Relaxation of weight constraint : {}'.format(prt.opt))

Traversal_queue.add(prt)

while Traversal_queue.length != 0:
    prt = Traversal_queue.remove()  # we should remove a node from the queue 
                                    # based on the traversal strategy and generate a couple of new nodes
                                    # where the next item can be selected or not
    if prt.opt > Objective:         # if the optimistic value of the parent node is better than
                                    # the objective value obtained so far, it is reasonable to proceed with the exploration
        lhbranch = node_gen(0, 0, 0) # a new node (the left one where X=1) is generated
        lhbranch.level = prt.level + 1  # the attributes of the new node are determined
        lhbranch.value = prt.value + v[lhbranch.level]
        lhbranch.weight = prt.weight + w[lhbranch.level]
        lhbranch.selected = prt.selected.copy()   # we shoud copy the sequence of selected items so far and then:
        lhbranch.selected.append(lhbranch.level)  # we add the current node to its ancestors
        nodes+=1                                  # since we have generated a new node, we add to the number of nodes
        
        lhbranch.opt = LRS(lhbranch)              
        if lhbranch.opt > Objective:
            lhbranch.side='left'
            Traversal_queue.add(lhbranch)
        
        if  lhbranch.value > Objective and lhbranch.weight <= C: #if the value of the new node helps to improve the solution
                                                                 # while it doesn't violate the constraint
            select = lhbranch.selected
            Objective = lhbranch.value
    
        rhbranch = node_gen(lhbranch.level, prt.value, prt.weight)  #the right hand side branch is generated here
                                                                    # where the decision variable will be zero and
                                                                    # hence, the value and weight will be the same as the parent's
        rhbranch.opt = LRS(rhbranch)
        rhbranch.selected = prt.selected.copy()
        nodes+=1
        if rhbranch.opt > Objective:
            rhbranch.side='right'
            Traversal_queue.add(rhbranch)
    else:
        print('\n The node ({}, {}, {}) is a deadend'.format(prt.level,prt.value,prt.weight))
    

print('\n Optimal items is/are {} \n {} items from {} items are put in the knapsack'.format(select,len(select),n))
print('\n Objective Function Value is " {} " and\n the number of the nodes in the tree is " {} "'.format(Objective,nodes))
print(' Execution time is {} seconds'.format(round(time.time() - start_time,5)))