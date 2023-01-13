from tree_search import *
from cidades import *
from blocksworld import *


def func_branching(connections,coordinates):
    #IMPLEMENT HERE
    vizinhos = {}
    for (c1, c2, cost) in connections:

        if c1 not in vizinhos.keys():
            vizinhos[c1] = [c2]
        else:
            vizinhos[c1].append(c2)

        if c2 not in vizinhos.keys():
            vizinhos[c2] = [c1]
        else:
            vizinhos[c2].append(c1)

    nVizinhos = 0
    for city in vizinhos :
        nVizinhos += len(vizinhos[city])

    nCities = len(coordinates)

    return (nVizinhos/nCities) - 1
            

class MyCities(Cidades):
    def __init__(self,connections,coordinates):
        super().__init__(connections,coordinates)
        # ADD CODE HERE IF NEEDED
        self.branching = func_branching(connections,coordinates)

class MySTRIPS(STRIPS):
    def __init__(self,optimize=False):
        super().__init__(optimize)

    def simulate_plan(self,state,plan):
        #IMPLEMENT HERE
        last = [state]
        for action in plan:
            state = self.result(state, action)
            last.append(state)
        return last[-1]

 
class MyNode(SearchNode):
    def __init__(self,state,parent,depth=0,cost=0,heuristic=0,action=None):
        super().__init__(state,parent)
        #ADD HERE ANY CODE YOU NEED
        self.cost = cost
        self.heuristic = heuristic
        self.depth = depth
    


class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth',optimize=0,keep=0.25): 
        super().__init__(problem,strategy)
        #ADD HERE ANY CODE YOU NEED

        self.optimize = optimize
        self.keep = keep

        if optimize == 0:
            root = MyNode(problem.initial, None)
        if optimize == 1:
            root = (problem.initial, None, 0, 0, 0)
        if optimize == 2:
            root = (problem[1], None, 0, 0, 0, 2)
            self.open_nodes = [0]
        if optimize == 4:
            root = (problem[1], None, 0, 0, 0, 2)
            self.open_nodes = [0]
            self.close_nodes = []
        self.all_nodes = [root]
       

    def get_path(self,node):

        if self.optimize != 0:
            if node[1] == None:
                return [node[0]]
            path = self.get_path(self.all_nodes[node[1]])
            path += [node[0]]
            return (path)
        else:
            return super().get_path(node)

        

    def astar_add_to_open(self,lnewnodes):
        #IMPLEMENT HERE
        if self.optimize == 0:
            self.open_nodes = sorted(self.open_nodes + lnewnodes, key = lambda index : self.all_nodes[index].cost + self.all_nodes[index].heuristic)
        else :
            self.open_nodes = sorted(self.open_nodes + lnewnodes, key = lambda index : self.all_nodes[index][2] + self.all_nodes[index][3])

    # remove a fraction of open (terminal) nodes
    # with lowest evaluation function
    # (used in Incrementally Bounded A*)
    def forget_worst_terminals(self):
        #IMPLEMENT HERE
        pass

    # procurar a solucao
    def search2(self):
        #IMPLEMENT HERE

        if self.optimize == 0:
            while self.open_nodes != []:
                nodeID = self.open_nodes.pop(0)
                node = self.all_nodes[nodeID]
                if self.problem.goal_test(node.state):
                    self.solution = node
                    self.terminals = len(self.open_nodes)+1
                    self.cost = node.cost #
                    return self.get_path(node)
                lnewnodes = []
                self.non_terminals += 1
                for a in self.problem.domain.actions(node.state):
                    # (state, parent, depth, heuristic, cost)
                    newstate = self.problem.domain.result(node.state,a)
                    if newstate not in self.get_path(node):
                        newnode = MyNode(   newstate,
                                            nodeID,
                                            node.depth+1, #
                                            node.cost+self.problem.domain.cost(node.state,(node.state,newstate)), #
                                            self.problem.domain.heuristic(newstate,self.problem.goal),
                                            self.optimize
                                            ) #
                        lnewnodes.append(len(self.all_nodes))
                        self.all_nodes.append(newnode)
                self.add_to_open(lnewnodes)
            return None

        if self.optimize == 1:
            while self.open_nodes != []:
                nodeID = self.open_nodes.pop(0)
                node = self.all_nodes[nodeID]
                if self.problem.goal_test(node[0]):
                    self.solution = node
                    self.terminals = len(self.open_nodes)+1
                    self.cost = node[2] #
                    return self.get_path(node)
                lnewnodes = []
                self.non_terminals += 1
                for a in self.problem.domain.actions(node[0]):
                    newstate = self.problem.domain.result(node[0],a)
                    if newstate not in self.get_path(node):
                       # (state, parent, cost, heuristic, depth)
                        newnode = ( newstate,
                                    nodeID,
                                    node[2]+self.problem.domain.cost(node[0],(node[0],newstate)), #
                                    self.problem.domain.heuristic(newstate,self.problem.goal),
                                    node[4]+1 #
                                    ) #
                        lnewnodes.append(len(self.all_nodes))
                        self.all_nodes.append(newnode)
                self.add_to_open(lnewnodes)
            return None

        if self.optimize == 2:
            while self.open_nodes != []:
                nodeID = self.open_nodes.pop(0)
                node = self.all_nodes[nodeID]
                if self.problem[0][4](node[0],self.problem[2]):
                    self.solution = node
                    self.terminals = len(self.open_nodes)+1
                    self.cost = node[2] #
                    return self.get_path(node)
                lnewnodes = []
                self.non_terminals += 1
                for a in self.problem[0][0](node[0]):
                    newstate = self.problem[0][1](node[0],a)
                    if newstate not in self.get_path(node):
                       # (state, parent, cost, heuristic, depth)
                        newnode = ( newstate,
                                    nodeID,
                                    node[2]+self.problem[0][2](node[0],(node[0],newstate)), #
                                    self.problem[0][3](newstate,self.problem[2]),
                                    node[4]+1 #
                                    ) #
                        lnewnodes.append(len(self.all_nodes))
                        self.all_nodes.append(newnode)
                self.add_to_open(lnewnodes)
            return None

        if self.optimize == 4:
            while self.open_nodes != []:
                nodeID = self.open_nodes.pop(0)
                node = self.all_nodes[nodeID]
                self.close_nodes.append(node[0])
                if self.problem[0][4](node[0],self.problem[2]):
                    self.solution = node
                    self.terminals = len(self.open_nodes)+1
                    self.cost = node[2] #
                    return self.get_path(node)
                lnewnodes = []
                self.non_terminals += 1

                for a in self.problem[0][0](node[0]):
                    newstate = self.problem[0][1](node[0],a)

                    if newstate not in self.get_path(node) and newstate not in self.close_nodes:
                        self.close_nodes.append(newstate)
                       # (state, parent, cost, heuristic, depth)
                        newnode = ( newstate,
                                    nodeID,
                                    node[2]+self.problem[0][2](node[0],(node[0],newstate)), #
                                    self.problem[0][3](newstate,self.problem[2]),
                                    node[4]+1 #
                                    ) #
                        lnewnodes.append(len(self.all_nodes))
                        self.all_nodes.append(newnode)
                self.add_to_open(lnewnodes)
            return None
# If needed, auxiliary functions can be added