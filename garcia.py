# -*- coding: utf-8 -*-
"""
Ellipses over finite fields
"""

from finitefield import FiniteField
import numpy as np
import matplotlib.pyplot as plt


def find_mult_generator(p,m):
    """function to create class and find generators of it
    """
    print('Looking for generator of {0}^{1}'.format(p,m))
    f = FiniteField(p,m)
    done = False
    #random lists, hopefully one will  work
    for k in range(1000):
        rand = np.random.rand(p+1)*m
        totest = [int(i) for i in rand]
        test = f(totest)
        print('testing {0}'.format(k),test.poly)
        print(f.fieldSize)
        ans = []
        temptest = test
        for i in range(f.fieldSize-1):
            ans.append(temptest)
            temptest = temptest * test
        print('generated field')
        same = -1 * f.fieldSize + 1
        for i in ans:
            for j in ans:
                if i == j:
                    same +=1
        
    
        if same == 0:
            done = True
            break
    #so test is generator
    if done:
        print('generator calculated')
        return f,ans
    
def find_generator(p,m,a,b,name):
    if m > 1:
        f,ans = find_mult_generator(p,m)
        x_list = []
        y_list = []
        for i,x in enumerate(ans):
            for j,y in enumerate(ans):
                aone = y**2
                atwo = x**3 + a * x + b
                if aone == atwo:
                    x_list.append(i)
                    y_list.append(j)
                
    else:
        x_list = []
        y_list = []
        for x in range(p):
            for y in range(p):
                aone = y**2 % p
                atwo = (x**3 + a * x + b) % p
                if aone == atwo:
                    x_list.append(x)
                    y_list.append(y)
        
    #now output the latex
    #first make the axis
    print('Elements calculated, now drawing')
    step = (10)/p**m
    #draw the grid
    dstep = -5
    outstr = ''
    if p**m < 30:
        for i in range(p**m+1):
            outstr += "\draw[gray,very thin](-5,{0}) --(5,{0});\n".format(dstep)
            outstr += "\draw[gray,very thin]({0},-5) -- ({0},5);\n".format(dstep)
            dstep += step
        if m == 1:
            ind = [i for i in range(p)]
        else:
            ind = [0,1] + ['$g^{0}$'.format('{'+str(i)+'}') for i in range(1,p**m-1)]
        k = step-5
        for i in ind:
            outstr+= "\\node at ({0},{1}) {2};\n".format(k,-5.5,'{'+str(i)+'}')
            outstr+= "\\node at ({0},{1}) {2};\n".format(-5.5,k,'{'+str(i)+'}')
            k+= step
    dot_size = step/3
    for i in range(len(x_list)):
        x = x_list[i] * step - 5 + step
        y = y_list[i] * step - 5 + step
        outstr +="\draw[fill = black] ({0},{1}) circle({2}cm);\n".format(x,y,dot_size)
    else:
        outstr += "\draw[gray,very thin](-5,-5) --(5,-5)node[right]{$x$};\n"
        outstr += "\draw[gray,very thin](-5,-5) -- (-5,5)node[above]{$y$};\n"
    with open(name,'w') as fp:
        fp.write(outstr)
    
    print('Calculations Complete')
        

if __name__ == '__main__':
    find_generator(3,5,1,2,'35out.txt')