def sort(lst):
    if not lst:
        return lst

    head, tail = lst[0], lst[1:]
    return (sort([a for a in tail if a <= head]) +
            [head] +
            sort([a for a in tail if a > head]))
