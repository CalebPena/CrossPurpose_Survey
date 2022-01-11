import random
class Tiles:
    cord_list=[]
    def __init__(self):
        self.exists=True
        self.combined_this_turn=False
        self.p4=random.randrange(10)
        if self.p4==0:
            self.value=4
        else:
            self.value=2
        while True:
            if len(self.cord_list)>=16:
                print('game over')
                break
            self.cord=[random.randrange(0,4),random.randrange(0,4)]
            if self.cord not in self.cord_list:
                break
        self.cord_list.append(self.cord)
    def make_tiles(self):
        return ' '*(4-len(str(self.value)))+str(self.value)
    def move(self,c,nc,d):
        self.cord_list.remove(self.cord)
        if d==0:
            self.cord=[c,nc]
        if d==1:
            self.cord=[nc,c]
        self.cord_list.append(self.cord)
    def colition_check(self,x,y,d):
        if d==0:
            if [x,y] in self.cord_list:
                return [True,[x,y]]
            else:
                return [False]
        if d==1:
            if [y,x] in self.cord_list:
                return [True,[y,x]]
            else:
                return [False]
    def combine_tiles(self,tile2):
        if tile2.value==self.value:
            if tile2.combined_this_turn==False:
                tile2.value=tile2.value*2
                tile2.combined_this_turn=True
                self.exists=False
                self.cord_list.remove(self.cord)
                return tile2.make_tiles()
            else:
               return tile2.make_tiles() 
        else:
            return tile2.make_tiles()
class Board:
    def __init__(self):
        self.board={(0,0):' '*4,(1,0):' '*4,(2,0):' '*4,(3,0):' '*4,
                    (0,1):' '*4,(1,1):' '*4,(2,1):' '*4,(3,1):' '*4,
                    (0,2):' '*4,(1,2):' '*4,(2,2):' '*4,(3,2):' '*4,
                    (0,3):' '*4,(1,3):' '*4,(2,3):' '*4,(3,3):' '*4}
    def update(self,x,y,v):
        self.board[(x,y)]=v
    def remove(self,x,y):
        self.board[(x,y)]=' '*4
    def make_board(self):
        print('-'*5+'-'*16)
        for i in range(4):
            print('',self.board[(0,i)],self.board[(1,i)],
                  self.board[(2,i)],self.board[(3,i)],'',sep="|")
            print('-'*5+'-'*16)  
def reorder(all_tiles,direction):
    ordered_tiles=[]
    if direction=='up':
        for y in range(4):
            for x in range(4):
                for i in all_tiles:
                    if [x,y]==i.cord:
                        ordered_tiles.append(i)
    elif direction=='down':
        for y in range(4):
            for x in range(4):
                for i in all_tiles:
                    if [x,3-y]==i.cord:
                        ordered_tiles.append(i)
    elif direction=='left':
        for x in range(4):
            for y in range(4):
                for i in all_tiles:
                    if [x,y]==i.cord:
                        ordered_tiles.append(i)
    else:
        for x in range(4):
            for y in range(4):
                for i in all_tiles:
                    if [3-x,y]==i.cord:
                        ordered_tiles.append(i)
    return ordered_tiles
def turn(all_tiles,b,):
    check=0
    '''moves_list format:
            direction it is moving
            axis it is moving on: 0 is x, 1 is y
            cordinate on that axis it is aproaching
            how the x or y cordinates are changing
            axis it is not moving on: 0 is x, 1 is y
            Says whether or not the key has been checked this turn
    '''
    moves_list={'w':['up',1,0,-1,0,False],
                'a':['left',0,0,-1,1,False],
                's':['down',1,3,1,0,False],
                'd':['right',0,3,1,1,False]}
    while check==0:
        for i in all_tiles:
            i.combined_this_turn=False
        while True:
            move=str(input())
            #possible_moves=['w','a','s','d']
            #move=possible_moves[random.randrange(4)]
            if move in moves_list:
                break
        moves_list[move][5]=True
        move=moves_list[move]
        for i in reorder(all_tiles,move[0]):
            while i.cord[move[1]] != move[2]:
                colition=i.colition_check(i.cord[move[1]]+move[3],
                                          i.cord[move[4]],
                                          move[1])
                if colition[0]:
                    for f in all_tiles:
                        if f.cord==colition[1]:
                            b.update(colition[1][0],colition[1][1],i.combine_tiles(f))
                            if i.exists==False:
                                check+=1
                                b.remove(i.cord[0],i.cord[1])
                                all_tiles.remove(i)
                    break
                if not colition[0]:
                    check+=1
                    b.remove(i.cord[0],i.cord[1])
                    i.move(i.cord[move[1]]+move[3],i.cord[move[4]],move[1])
                    b.update(i.cord[0],i.cord[1],i.make_tiles())
        if moves_list['w'][5] and moves_list['a'][5] and moves_list['s'][5] and moves_list['d'][5]:
            check+=1
def start_2048():
    b=Board()
    all_tiles=[]
    for i in range(2):
        all_tiles.append(Tiles())
        b.update(all_tiles[-1].cord[0],
                 all_tiles[-1].cord[1],all_tiles[-1].make_tiles())
    b.make_board()
    while True:
        turn(all_tiles,b)
        try:
            all_tiles.append(Tiles())
        except:
            break
        b.update(all_tiles[-1].cord[0],
                 all_tiles[-1].cord[1],all_tiles[-1].make_tiles())
        b.make_board()
start_2048()
