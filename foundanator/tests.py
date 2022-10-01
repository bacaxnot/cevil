def sum(d, n):

    def isum(ni):
        if ni <= 0:
            return 0
        else:
            valuei = ni + isum(ni-1)
            return valuei
    
    value = 0;
    while d > 0:
        value =  isum(n)
        n = value;
        d -= 1;
    return value

print(sum(2,3))