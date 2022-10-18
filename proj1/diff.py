
a = ''
ibytes = open('INPUT.bin','rb').read()
b = ''
obytes = open('OUTPUT.bin','rb').read()
   
for i in range(6250):
    a += (10-len(bin(ibytes[i])))*'0' + bin(ibytes[i])[2:len(bin(ibytes[i]))]
    b += (10-len(bin(obytes[i])))*'0' + bin(obytes[i])[2:len(bin(obytes[i]))]




if len(a)!=len(b):
    print("Wrong length!")
    print("output length:{}".format(len(b)))
    exit()

c={i:0 for i in range(0,126)}
for i in range(400):
    d=0
    for j in range(125):
        if a[i*125+j]!=b[i*125+j]:
            print(i*125+j)
            d+=1
    c[d]+=1
print(*sorted(c.items(), key=lambda x:x[1]), sep="\n")
print("Total wrong:{}".format(sum(map(lambda x:x[0]*x[1], c.items()))))

t=list(range(50000))
y=[1 if i in c else 0 for i in range(50000)]
