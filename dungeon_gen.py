import argparse, random

class Room:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
    def center(self): return (self.x + self.w//2, self.y + self.h//2)

def bsp_split(x, y, w, h, depth, min_size=5):
    if depth <= 0 or w < min_size*2 or h < min_size*2:
        rw = random.randint(min_size-1, w-2)
        rh = random.randint(min_size-1, h-2)
        rx = x + random.randint(1, w-rw-1)
        ry = y + random.randint(1, h-rh-1)
        return [Room(rx, ry, rw, rh)]
    if w > h:
        split = random.randint(min_size, w-min_size)
        return bsp_split(x, y, split, h, depth-1, min_size) + bsp_split(x+split, y, w-split, h, depth-1, min_size)
    else:
        split = random.randint(min_size, h-min_size)
        return bsp_split(x, y, w, split, depth-1, min_size) + bsp_split(x, y+split, w, h-split, depth-1, min_size)

def generate(w=60, h=30, depth=4, seed=None):
    if seed: random.seed(seed)
    grid = [["#"]*w for _ in range(h)]
    rooms = bsp_split(0, 0, w, h, depth)
    for room in rooms:
        for y in range(room.y, min(room.y+room.h, h)):
            for x in range(room.x, min(room.x+room.w, w)):
                grid[y][x] = "."
    # Connect rooms
    for i in range(len(rooms)-1):
        cx1, cy1 = rooms[i].center()
        cx2, cy2 = rooms[i+1].center()
        x, y = cx1, cy1
        while x != cx2:
            if 0 <= y < h and 0 <= x < w: grid[y][x] = "."
            x += 1 if cx2 > x else -1
        while y != cy2:
            if 0 <= y < h and 0 <= x < w: grid[y][x] = "."
            y += 1 if cy2 > y else -1
    # Place stairs
    start = rooms[0].center()
    end = rooms[-1].center()
    grid[start[1]][start[0]] = "<"
    grid[end[1]][end[0]] = ">"
    return grid, rooms

def main():
    p = argparse.ArgumentParser(description="Dungeon generator")
    p.add_argument("-w", "--width", type=int, default=60)
    p.add_argument("-H", "--height", type=int, default=25)
    p.add_argument("-d", "--depth", type=int, default=4)
    p.add_argument("--seed", type=int)
    args = p.parse_args()
    grid, rooms = generate(args.width, args.height, args.depth, args.seed)
    for row in grid: print("".join(row))
    print(f"Rooms: {len(rooms)}")

if __name__ == "__main__":
    main()
