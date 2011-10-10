from field import create_hw4_map
import copy
from numpy import zeros
import time

INCLUDE_DIAG=True

# def neighbors(f, wave_front, processed, p):
#     if p[0]+1 < (f.height-0) and f[p[0]+1, p[1]] != -1 and (p[0]+1, p[1]) not in wave_front and (p[0]+1, p[1]) not in processed:
#         wave_front.append((p[0]+1, p[1]))
#     if p[0]-1 >= 0           and f[p[0]-1, p[1]] != -1 and (p[0]-1, p[1]) not in wave_front and (p[0]-1, p[1]) not in processed:
#         wave_front.append((p[0]-1, p[1]))
#     if p[1]+1 < (f.width-0)  and f[p[0], p[1]+1] != -1 and (p[0], p[1]+1) not in wave_front and (p[0], p[1]+1) not in processed:
#         wave_front.append((p[0], p[1]+1))
#     if p[1]-1 >= 0           and f[p[0], p[1]-1] != -1 and (p[0], p[1]-1) not in wave_front and (p[0], p[1]-1) not in processed:
#         wave_front.append((p[0], p[1]-1))
#     
#     if INCLUDE_DIAG:
#         # x+1, y+1
#         if p[0]+1 < (f.height-0) and p[1]+1 < (f.width-0) and f[p[0]+1, p[1]+1] != -1 \
#                 and (p[0]+1, p[1]+1) not in wave_front and (p[0]+1, p[1]+1) not in processed:
#             wave_front.append((p[0]+1, p[1]))
#         # x+1, y-1
#         if p[0]+1 < (f.height-0) and p[1]-1 >= 0 and f[p[0]+1, p[1]-1] != -1 \
#                 and (p[0]+1, p[1]-1) not in wave_front and (p[0]+1, p[1]-1) not in processed:
#             wave_front.append((p[0]+1, p[1]-1))
#         # x-1, y+1
#         if p[0]-1 >= 0 and p[1]+1 < (f.width-0)  and f[p[0]-1, p[1]+1] != -1 \
#                 and (p[0]-1, p[1]+1) not in wave_front and (p[0]-1, p[1]+1) not in processed:
#             wave_ront.append((p[0]-1, p[1]+1))
#         # x-1, y-1
#         if p[0]-1 >= 0 and p[1]-1 >= 0 and f[p[0]-1, p[1]-1] != -1 \
#                 and (p[0]-1, p[1]-1) not in wave_front and (p[0]-1, p[1]-1) not in processed:
#             wave_front.append((p[0]-1, p[1]-1))

def neighbors(f, wave_front, processed, p):
    """Returns the neighbors of the given coordinate"""
    (x, y) = p
    if INCLUDE_DIAG:
        possible_neighbors = [(x-1,y+1), (x,y+1), (x+1,y+1),
                              (x-1,y),            (x+1,y),
                              (x-1,y-1), (x,y-1), (x+1,y-1)]
    else:
        possible_neighbors = [           (x,y+1),
                              (x-1,y),            (x+1,y),
                                         (x,y-1)]
    for pn in possible_neighbors:
        if 0 <= pn[0] < f.height and 0 <= pn[1] < f.width and f[pn[0], pn[1]] == 0 and pn not in processed:
            wave_front.add(pn)

def brushfire(f, wave_front, processed):
    current_distance=1
    for x in wave_front:
        f[x[0], x[1]] = current_distance
    while len(wave_front) > 0:
        current_wave_front = copy.copy(wave_front)
        wave_front = set([])
        current_distance = current_distance + 1
        for p in current_wave_front:
            neighbors(f, wave_front, processed, p)
            # print len(processed), len(wave_front)
            (x, y) = p
            if INCLUDE_DIAG:
                possible_neighbors = [(x-1,y+1), (x,y+1), (x+1,y+1),
                                      (x-1,y),            (x+1,y),
                                      (x-1,y-1), (x,y-1), (x+1,y-1)]
            else:
                possible_neighbors = [           (x,y+1),
                                      (x-1,y),            (x+1,y),
                                                 (x,y-1)]
            for pn in possible_neighbors:
                if 0 <= pn[0] < f.height and \
                        0 <= pn[1] < f.width and \
                        f[pn[0], pn[1]] == 0:
                    f[pn[0], pn[1]] = current_distance
                    processed.add(pn)

def plot_performance():
    """Calculates the run time for many map scales and plots the times vs the scales"""
    scales = [1+0.25*x for x in range(30)]
    times = []
    for scale in scales:
        f = create_hw4_map(scale)

        f[0,0] = -1

        if INCLUDE_DIAG:
            f[1,0] = 1
            f[0,1] = 1
            f[1,1] = 1

            wave_front = set([(1,0), (0,1), (1,1)])
            processed = set([(0,0), (1,0), (0,1), (1,1)])
        else:
            f[1,0] = 1
            f[0,1] = 1

            wave_front = set([(1,0), (0,1)])
            processed = set([(0,0), (1,0), (0,1)])

        import time
        start = time.time()
        brushfire(f, wave_front, processed)
        t = time.time() - start
        times.append(t)
        print "Processing a field of size {}x{} took".format(f.width, f.height), t, "seconds"
        print f
    print times
    from matplotlib.pyplot import plot, show
    plot(scales, times)
    show()

if __name__ == '__main__':
    plot_performance()
    