#!/usr/bin/env python3
"""dungeon_gen - BSP-based dungeon generator."""
import sys, random
class Room:
    def __init__(self, x, y, w, h): self.x=x; self.y=y; self.w=w; self.h=h
    def center(self): return self.x+self.w//2, self.y+self.h//2
def bsp_split(x, y, w, h, min_size=6, depth=0, max_depth=4):
    if depth>=max_depth or w<min_size*2 and h<min_size*2:
        rw=random.randint(min_size-2, w-2); rh=random.randint(min_size-2, h-2)
        rx=x+random.randint(1, w-rw-1); ry=y+random.randint(1, h-rh-1)
        return [Room(rx, ry, rw, rh)]
    if w>h:
        split=random.randint(min_size, w-min_size)
        return bsp_split(x,y,split,h,min_size,depth+1,max_depth)+bsp_split(x+split,y,w-split,h,min_size,depth+1,max_depth)
    else:
        split=random.randint(min_size, h-min_size)
        return bsp_split(x,y,w,split,min_size,depth+1,max_depth)+bsp_split(x,y+split,w,h-split,min_size,depth+1,max_depth)
def generate(w=50, h=25, seed=None):
    if seed: random.seed(seed)
    grid=[["#"]*w for _ in range(h)]
    rooms=bsp_split(0,0,w,h)
    for room in rooms:
        for r in range(room.y, min(room.y+room.h, h)):
            for c in range(room.x, min(room.x+room.w, w)):
                grid[r][c]="."
    for i in range(len(rooms)-1):
        cx1,cy1=rooms[i].center(); cx2,cy2=rooms[i+1].center()
        x,y=cx1,cy1
        while x!=cx2:
            if 0<=y<h and 0<=x<w: grid[y][x]="."
            x+=1 if cx2>x else -1
        while y!=cy2:
            if 0<=y<h and 0<=x<w: grid[y][x]="."
            y+=1 if cy2>y else -1
    return grid, rooms
if __name__=="__main__":
    seed=int(sys.argv[1]) if len(sys.argv)>1 else random.randint(0,9999)
    grid, rooms = generate(seed=seed)
    print(f"Seed: {seed} | Rooms: {len(rooms)}")
    for row in grid: print("".join(row))
