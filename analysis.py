import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import pickle
import matplotlib.colors as colors

np.set_printoptions(threshold=np.inf)

logm = np.zeros(120)
logg = np.zeros(200)

Z = np.zeros((200,120))

#with open('results1','r') as res1:
 #   for i in range(200):
  #      ligne = res1.readline()
   #     res = ligne.split(',')
    #    value = res[2]
     #   l = i%10
      #  c = i//10
       # Z[l,c] = value
res=np.zeros((24000,3))
count=0
with open('results_fin.txt','r') as results:
    for i in range (120):
        for j in range (200):
            ligne = results.readline()
            res[count] = ligne.split(' ')
            count += 1

print(len(res))
            
def tri_ins1(t):
    for k in range(1,len(t)):
        temp=t[k,0]
        temp2=t[k,1]
        temp3=t[k,2]
        j=k
        while j>0 and temp<t[j-1,0]:
            t[j,0]=t[j-1,0]
            t[j,1]=t[j-1,1]
            t[j,2]=t[j-1,2]
            j-=1
        t[j,0]=temp
        t[j,1]=temp2
        t[j,2]=temp3
    return t

def tri_ins2(t):
    for k in range(1,len(t)):
        temp1=t[k,0]
        temp=t[k,1]
        temp3=t[k,2]
        j=k
        while j>0 and temp<t[j-1,1]:
            t[j,0]=t[j-1,0]
            t[j,1]=t[j-1,1]
            t[j,2]=t[j-1,2]
            j-=1
        t[j,0]=temp1
        t[j,1]=temp
        t[j,2]=temp3
    return t

res = tri_ins1(res)

for s in range(0,24000,200):
    res[s:s+200] = tri_ins2(res[s:s+200])

print(res)






line=0
for i in range(120):
    for j in range(200):
        value = res[line,2]
        logm[i] = res[line,0]
        logg[j] = res[line,1] + 9
        count += 1
        l = i
        c = j
        Z[c,l] = value/2
        line += 1


            
X,Y = np.meshgrid(logm,logg)

            
with open('grid', 'wb') as grid:
    mon_pickler = pickle.Pickler(grid)
    mon_pickler.dump(Z)



abs = np.array([7.60326340326340321951,7.84257964257964257371,8.10054390054390083264,8.10054390054389905629,8.00108780108779882312,7.50069930069929835525,6.42222222222222072219,5.07334887334887341126,4.00730380730380719712])
ord = np.array([-9.00102215472143818431,-9.47553819821122722544,-9.99037390612569531356,-11.3989657915672211175,-11.4983269448663225631,-11.4987150743713968382,-10.9627974253272562066,-10.2905739977339010238,-9.75464670572069003640])
    
plt.figure()
axes = plt.gca()
levels = [0.0, 1.78, 1e150]
contour = plt.contour(X, Y, Z, levels, colors='w')
#plt.clabel(contour, colors = 'k', fmt = '%2.1f', fontsize=12)
contour_filled = plt.contourf(X, Y, Z, levels, colors=['w','b'])
plt.colorbar(contour_filled)
plt.xlabel('log10(m/eV)', fontsize=20)
plt.ylabel('log10(g/GeV-1)', fontsize=20)
axes.yaxis.set_tick_params(width=2, labelsize=20)
axes.xaxis.set_tick_params(width=2, labelsize=20)
plt.plot(abs, ord, 'r', linewidth=2)
plt.show()


L = -0.5*Z/0.59333

plt.figure()
levels = [-1e20,-1e8,-1e7,-1e6,-1e5,-1e4,-1e3,-100.0,-10.0,-5.915,-3.09,-1.5,-1.15,0.0]
contour = plt.contour(X, Y, L, levels, colors='k')
plt.clabel(contour, colors = 'k', fmt = '%2.1f', fontsize=8)
contour_filled = plt.contourf(X, Y, L, levels, colors=['brown','indigo','darkblue','cornflowerblue','lightskyblue','teal','mediumspringgreen','limegreen','greenyellow','gold','goldenrod','olive', 'darkgreen'])
plt.colorbar(contour_filled)
plt.xlabel('log10(m/eV)')
plt.ylabel('log10(g/GeV-1')
plt.plot(abs, ord, 'r')
plt.show()
