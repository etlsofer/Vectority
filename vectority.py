import numpy as np
import matplotlib.pyplot as plt
import math
import networkx as nx


class Node:

    def __init__(self, cordinate, in_v=[], out_v=[]):
        self.in_v = in_v
        self.out_v = out_v
        self.counter = 0
        self.cordinate = cordinate

    def __lt__(self, other):
        return self.counter > other.counter

    def __str__(self):
        return str(self.cordinate[0]) +" "+ str(self.cordinate[1])

class Vectority:

    def __init__(self,list_file,widtm,min_dist,max_iter = np.inf, count = 1):
        self.list_file = list_file
        self.widtm = widtm
        self.nodes = []
        self.min_dist = min_dist
        self.max_iter = max_iter
        #self.g = nx.Graph()
        self.count = count
        self.c_node = set()

    # check if they are neighbors
    def not_adj(self,node1,node2):
        if (node1.in_v.__contains__(node2)) or (node1.out_v.__contains__(node2))\
                or (node2.in_v.__contains__(node1)) or (node2.out_v.__contains__(node1)):
            return False
        return True

    def update_adj_of_node(self,old_node, new_node):
        for node in old_node.in_v:
            node.out_v.remove(old_node)
            node.out_v.append(new_node)
        for node in old_node.out_v:
            node.in_v.remove(old_node)
            node.in_v.append(new_node)

    def union(self, node1,node2):
        new_node = Node(((node1.cordinate[0]+node2.cordinate[0])/2,(node1.cordinate[1]+node2.cordinate[1])/2))
        #self.g.add_node(new_node)
        #self.g = nx.contracted_nodes(self.g, new_node, node1)
        #self.g = nx.contracted_nodes(self.g, new_node, node2)
        self.update_adj_of_node(node1, new_node)
        self.update_adj_of_node(node2, new_node)
        new_node.in_v = node1.in_v + node2.in_v
        new_node.out_v = node1.out_v + node2.out_v
        self.nodes.append(new_node)
        self.nodes.remove(node1)
        self.nodes.remove(node2)

    def dist(self,node1,node2):
        return math.sqrt((node1.cordinate[0]-node2.cordinate[0])**2+(node1.cordinate[1]-node2.cordinate[1])**2)

    def convert_str_to_float(self,list_str):
        res = []
        for str in list_str:
            res.append(float(str))
        return res

    #get list of x and y cordinate. and v, u vectors, and produces NODE from both ends of the vector.
    def makegraph(self):
        for items in self.list_file:
            items = self.convert_str_to_float(items)
            #print(items)
            # Create new nodes
            node1 = Node((items[0],items[1]))
            node2 = Node((items[0]+items[2]*self.widtm,items[1]+items[3]*self.widtm))
            node1.out_v = [node2]
            node2.in_v = [node1]
            self.nodes.append(node1)
            self.nodes.append(node2)
            #self.g.add_node(node1)
            #self.g.add_node(node2)
            #self.g.add_edge(node1,node2)



    def dfs(self,visited, node):
        if node not in visited:
            #print(node)
            visited.append(node)
            for neighbour in node.out_v:
                self.dfs(visited, neighbour)
        else:
            #print("FINISH",node)
            node.counter += 1
            if node.counter >= self.count:
                self.c_node.add(node)


    # Returns true if graph is cyclic else false
    def update_cycle(self):
        visited = []  # Set to keep track of visited nodes.
        for node in self.nodes:
            self.dfs(visited,node)
            visited = []


    def execution(self):
        self.makegraph()
        #print(len(self.nodes))
        counter = 0
        changed = True
        breack_i = False
        while(changed) and (counter < self.max_iter):
            for i in range(len(self.nodes)):
                if breack_i:
                    breack_i = False
                    break
                changed = False
                for j in range(i):
                    # print(self.dist(self.nodes[i], self.nodes[j]))
                    if (self.dist(self.nodes[i], self.nodes[j]) <= self.min_dist) \
                            and (self.not_adj(self.nodes[i], self.nodes[j])):
                        self.union(self.nodes[i], self.nodes[j])
                        changed = True
                        breack_i = True
                        break
            counter += 1
        self.nodes = set(self.nodes)
        for node in self.nodes:
            node.in_v = set(node.in_v)
            node.out_v = set(node.out_v)
        #for node in self.nodes:
        #    print(node.in_v)
        self.update_cycle()
        #print(len(self.c_node),len(self.nodes))
        #for node in self.c_node:
        #   print(node,"PROBLEM")
        return self.c_node



    '''
        changed = False
            nodes = list(self.g.nodes)
            for node1 in nodes:
                if breack_i:
                    breack_i = False
                    break
                for node2 in nodes:
                    if node1 == node2:
                        continue
                    if self.dist(node1, node2) <= self.min_dist:
                        self.union(node1, node2)
                        changed = True
                        breack_i = True
                        break
            counter += 1
        nx.draw(self.g)
        plt.savefig("simple_path.png")  # save as png
        plt.show()
    '''

class C_vectority:
    def __init__(self,file_name,widtm,min_dist,max_iter = np.inf, max_of_point = np.inf, biger = False):
        self.file_name = file_name
        self.widtm = widtm
        self.min_dist = min_dist
        self.max_iter = max_iter
        # self.g = nx.Graph()
        self.max_of_point = max_of_point
        self.biger = biger
    '''
    def search(self, left,right,list_of_lists):
        templ = Vectority(list_of_lists, 0.0025, 0.5, count=left).execution()
        tempr = Vectority(list_of_lists, 0.0025, 0.5, count=right).execution()
        if len(templ) > self.max_of_point and len(tempr) == 0:
            right = int((right + left) / 2)
            left = left + 1
            return self.search(left,right,list_of_lists)
        elif len(tempr) > self.max_of_point:
            right = int((len(list_of_lists)+right)/2)
            return self.search(left, right, list_of_lists)
        else:
            print("The problem points are:")
            if len(templ) > len(tempr) and not self.biger:
                for node in tempr:
                    print(node)
            else:
                for node in templ:
                    print(node)

    '''

    def execution(self):
        list_of_lists = []
        with open(self.file_name) as f:
            for line in f:
                inner_list = [elt.strip() for elt in line.split('\t')]
                # in alternative, if you need to use the file content as numbers
                # inner_list = [int(elt.strip()) for elt in line.split(',')]
                list_of_lists.append(inner_list)
        # search
        #self.search(1,len(list_of_lists)-1,list_of_lists)
        max_count = 0
        count = 0
        final_point = []
        temp = Vectority(list_of_lists, self.widtm, self.min_dist, count=1).execution()
        for node in temp:
            if node.counter > max_count:
                max_count = node.counter
        #if len(temp) <= self.max_of_point:
        print("The problem points are:")
        for node in temp:
            final_point.append(node)
            #print(node," with score of "+str(node.counter/max_count))
        final_point.sort()
        for node in final_point:
            if(count >= self.max_of_point):
                return
            print("{:.3f}, {:.3f} with score {:.3f}".format(node.cordinate[0],node.cordinate[1],node.counter/max_count))
            count += 1



def main():
    C_vectority('exp1_001.txt',widtm=0.0025,min_dist=0.025).execution()

    '''
    list_of_lists = []
    with open('exp1_001.txt') as f:
        for line in f:
            inner_list = [elt.strip() for elt in line.split('\t')]
            # in alternative, if you need to use the file content as numbers
            # inner_list = [int(elt.strip()) for elt in line.split(',')]
            list_of_lists.append(inner_list)
    res  = Vectority(list_of_lists, widtm=0.0025, min_dist=0.5, count=300).execution()
    for node in res:
        print(node)

    '''


if __name__ == '__main__':
    main()
