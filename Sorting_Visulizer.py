import pygame
import random
import math
pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))    # bar size 
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending, speed):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

    controls = draw_info.FONT.render(f"R - Reset | SPACE - Start Sorting | A - Asc | D - Desc | Speed: {speed}", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 40))

    sorting = draw_info.FONT.render("B - Bubble | I - Insertion | S - Selection | M - Merge | Q - Quick | H - Heap | X - Radix", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 70))

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]
        if i in color_positions:
            color = color_positions[i] 

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

        # ⬇ New lines for showing numbers
        value_text = draw_info.FONT.render(str(val), True, draw_info.BLACK)
        value_x = x + draw_info.block_width // 2 - value_text.get_width() // 2
        value_y = y - 20
        draw_info.window.blit(value_text, (value_x, value_y))

    if clear_bg:
        pygame.display.update()



def generate_starting_list(n, min_val, max_val):
    return [random.randint(min_val, max_val) for _ in range(n)]

# ==================== Sorting Algorithms ====================

def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            if (lst[j] > lst[j+1] and ascending) or (lst[j] < lst[j+1] and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                yield True
    return lst


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(1, len(lst)):
        current = lst[i]
        while True:
            ascending_sort = i > 0 and lst[i-1] > current and ascending
            descending_sort = i > 0 and lst[i-1] < current and not ascending
            if not ascending_sort and not descending_sort:
                break
            lst[i] = lst[i-1]
            i -= 1
            lst[i] = current
            draw_list(draw_info, {i: draw_info.GREEN, i+1: draw_info.RED}, True)
            yield True
    return lst


def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst)):
        min_or_max_idx = i
        for j in range(i+1, len(lst)):
            if (lst[j] < lst[min_or_max_idx] and ascending) or (lst[j] > lst[min_or_max_idx] and not ascending):
                min_or_max_idx = j
        lst[i], lst[min_or_max_idx] = lst[min_or_max_idx], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, min_or_max_idx: draw_info.RED}, True)
        yield True
    return lst


def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst
    yield from _merge_sort(lst, 0, len(lst)-1, draw_info, ascending)
    return lst

def _merge_sort(lst, left, right, draw_info, ascending):
    if left >= right:
        return
    mid = (left + right) // 2
    yield from _merge_sort(lst, left, mid, draw_info, ascending)
    yield from _merge_sort(lst, mid+1, right, draw_info, ascending)
    yield from merge(lst, left, mid, right, draw_info, ascending)

def merge(lst, left, mid, right, draw_info, ascending):
    merged = []
    left_part = lst[left:mid+1]
    right_part = lst[mid+1:right+1]
    i = j = 0

    while i < len(left_part) and j < len(right_part):
        if (left_part[i] <= right_part[j] and ascending) or (left_part[i] >= right_part[j] and not ascending):
            merged.append(left_part[i])
            i += 1
        else:
            merged.append(right_part[j])
            j += 1

    merged.extend(left_part[i:])
    merged.extend(right_part[j:])

    for i, val in enumerate(merged):
        lst[left + i] = val
        draw_list(draw_info, {left+i: draw_info.GREEN}, True)
        yield True


def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst
    yield from _quick_sort(lst, 0, len(lst)-1, draw_info, ascending)
    return lst

def _quick_sort(lst, low, high, draw_info, ascending):
    if low < high:
        pi = yield from partition(lst, low, high, draw_info, ascending)
        yield from _quick_sort(lst, low, pi-1, draw_info, ascending)
        yield from _quick_sort(lst, pi+1, high, draw_info, ascending)

def partition(lst, low, high, draw_info, ascending):
    pivot = lst[high]
    i = low - 1
    for j in range(low, high):
        if (lst[j] <= pivot and ascending) or (lst[j] >= pivot and not ascending):
            i += 1
            lst[i], lst[j] = lst[j], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
            yield True
    lst[i+1], lst[high] = lst[high], lst[i+1]
    draw_list(draw_info, {i+1: draw_info.GREEN, high: draw_info.RED}, True)
    yield True
    return i+1


def heap_sort(draw_info, ascending=True):
    lst = draw_info.lst
    n = len(lst)

    def heapify(n, i):
        largest_smallest = i
        l = 2*i + 1
        r = 2*i + 2

        if l < n and ((lst[l] > lst[largest_smallest] and ascending) or (lst[l] < lst[largest_smallest] and not ascending)):
            largest_smallest = l
        if r < n and ((lst[r] > lst[largest_smallest] and ascending) or (lst[r] < lst[largest_smallest] and not ascending)):
            largest_smallest = r

        if largest_smallest != i:
            lst[i], lst[largest_smallest] = lst[largest_smallest], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN, largest_smallest: draw_info.RED}, True)
            yield True
            yield from heapify(n, largest_smallest)

    for i in range(n//2 - 1, -1, -1):
        yield from heapify(n, i)
    for i in range(n-1, 0, -1):
        lst[i], lst[0] = lst[0], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, 0: draw_info.RED}, True)
        yield True
        yield from heapify(i, 0)
    return lst


def radix_sort(draw_info, ascending=True):
    lst = draw_info.lst
    max_val = max(lst)
    exp = 1

    while max_val // exp > 0:
        yield from counting_sort_exp(lst, exp, draw_info, ascending)
        exp *= 10
    return lst

def counting_sort_exp(lst, exp, draw_info, ascending):
    n = len(lst)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = lst[i] // exp
        count[index % 10] += 1

    if ascending:
        for i in range(1, 10):
            count[i] += count[i-1]
    else:
        for i in range(8, -1, -1):
            count[i] += count[i+1]

    i = n - 1
    while i >= 0:
        index = lst[i] // exp
        output[count[index % 10] - 1] = lst[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(n):
        lst[i] = output[i]
        draw_list(draw_info, {i: draw_info.GREEN}, True)
        yield True

# ==================== Main Loop ====================

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100
    speed = 5  # NEW: default speed (1–10)

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1200, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(speed * 10)  # NEW: adjust FPS based on speed

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending, speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False

            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True

            elif event.key == pygame.K_d and not sorting:
                ascending = False

            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"

            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"

            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"

            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"

            elif event.key == pygame.K_h and not sorting:
                sorting_algorithm = heap_sort
                sorting_algo_name = "Heap Sort"

            elif event.key == pygame.K_x and not sorting:
                sorting_algorithm = radix_sort
                sorting_algo_name = "Radix Sort"

            elif event.key == pygame.K_UP and not sorting:  # NEW: increase speed
                if speed < 10:
                    speed += 1

            elif event.key == pygame.K_DOWN and not sorting:  # NEW: decrease speed
                if speed > 1:
                    speed -= 1

    pygame.quit()

if __name__ == "__main__":
    main()

