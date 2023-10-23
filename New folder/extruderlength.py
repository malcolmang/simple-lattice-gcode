import math
def dist(tuple1, tuple2, currdist=0):
    ans = round(currdist + math.sqrt(abs((tuple1[0] - tuple2[0])**2 + (tuple1[1] - tuple2[1])**2)), 4)
    print(ans)
    return ans
    
biglist = [(3.9,0),(4.1,0),(4.25,1),(3.75,1),(3.5,2),(4.5,2),(4.75,3),(3.25,3), (3,4), (5,4), (5.25, 5), (2.75,5), (2.5, 6), (5.5, 6)]

currdist = 0
for i, currtup in enumerate(biglist):
    if i + 1 == len(biglist):
        break
    currdist = dist(currtup, biglist[i+1], currdist)