from collections import deque
import os
import timeit
import sqlite3
import argparse

def sam_read(sam_file):    #read sequence ID from SAM file.
    print('\n'+'loading sam file....')
    reads = []
    with open(sam_file) as f:
        for line in f:
            str_list = line.split()
            head = str_list[0]
            if '@' not in head[0]:
                reads.append(str_list[0])
    print('\n'+'loading complete.')
    return reads

def save_result(node_list):
    cwd = os.getcwd()
    textFile = cwd + '/result.txt'
    file = open(textFile, 'w+')
    for i in node_list:
        file.write(''.join(i) + "\n")
    file.close()
    return


parser = argparse.ArgumentParser(description = 'find all the connected component of the start node.')
parser.add_argument('graph_database', help='select the database of the graph')
parser.add_argument('sam_file', help='select the sam file as start node')
args = parser.parse_args()

samfile = args.sam_file
database_name = args.graph_database

time_start = timeit.default_timer()
reads = sam_read(samfile)

connect_queue = deque()
visited = set()
connect_queue.extend(reads)

conn = sqlite3.connect(database_name)
c = conn.cursor()

all_node = c.execute("SELECT keyword FROM edge_data")
node_set = set()
for node in all_node:
    node_set.add(node[0])

initial_visited = set(reads).intersection(node_set)  #filter out all the node that not in the graph
for node in initial_visited:
    visited.add(node)

print('\n'+'total number of start nodes: %i' %len(visited))

while connect_queue:
    pop_out = connect_queue.popleft()
    data = c.execute("SELECT * FROM edge_data WHERE keyword = '%s'" %pop_out)
    for row in data:
        if row[1] not in visited:
            connect_queue.append(row[1])
            visited.add(row[1])
            print('number of nodes found now: %i' % len(visited))

time_end = timeit.default_timer()
save_result(visited)
print('\n'+'save complete.')
print('please check the result.txt')
print('duration: '+ str(time_end - time_start) + 's')

c.close()
conn.close()