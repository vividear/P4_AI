def getDCtopo():
    
    level1 = 12;level2 = 12;level3 = 6;level4 = 3
    level_sum = level1 + level2 + level3 +level4
    topo_list = [[0 for i in range(level_sum)] for i in range(level_sum)]
    host_list = [0 for i in range(level_sum)]
    links=0
    for row in range(len(topo_list)):
        if row < level1:
            topo_list[row][level1+(row/2)*2] = 1
            topo_list[row][level1+(row/2)*2+1] = 1
            links+=2
        elif row < (level1+level2):
            topo_list[row][level1+level2+((row-level1)/4)*2] = 1
            topo_list[row][level1+level2+((row-level1)/4)*2+1] = 1
            links+=2
        elif row < (level1+level2+level3):
            for i in range(level4):
                topo_list[row][level1+level2+level3+i] = 1
                links+=1
        else:
            pass

    for row in range(len(topo_list)):
        for col in range(row, len(topo_list)):
            if topo_list[row][col] == 1:
                topo_list[col][row] = 1
                links+=1
    for i in range(level1):
        host_list[i] = 1
    '''
    topo_list=[[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0], [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0]]
    host_list=[1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0]
    lever_sum=18
    links=56
    '''
    return topo_list,host_list,level_sum,links
    
#topo_list,host_list,level_sum,links=getDCtopo()
#print topo_list
#print host_list 

