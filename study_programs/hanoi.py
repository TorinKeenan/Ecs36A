#tower of hanoi recursion provlem
def move_disk(a,b):
    print("move disk from",a,'to',b)
def hanoi(n,src,dst,tmp):
    if n>0:
        hanoi(n-1,src,dst,tmp)
        move_disk(src,tmp)
        hanoi(n-1,src,tmp,dst)

hanoi(5,1,2,3)