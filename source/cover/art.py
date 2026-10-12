import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
rng=np.random.default_rng(6)
navy="#0f1b2d"; gold="#d9b86c"; ivory="#efe6d2"
fig=plt.figure(figsize=(6.4,5.2)); ax=fig.add_axes([0,0,1,1]); ax.set_facecolor(navy); fig.patch.set_facecolor(navy)
x=np.linspace(0,2*np.pi,300); y=np.linspace(0,1.6*np.pi,240); X,Y=np.meshgrid(x,y)
U=np.sin(X)*np.cos(Y); V=-np.cos(X)*np.sin(Y)
sp=ax.streamplot(X,Y,U,V,density=1.6,color=gold,linewidth=0.55,arrowsize=0)
# mask streamlines on left part by overlay of particles fading
n=2600
px=rng.uniform(0,2*np.pi,n)**1.0; py=rng.uniform(0,1.6*np.pi,n)
w=np.clip(1-px/(2*np.pi)*1.5,0,1)
keep=rng.random(n)<w
# fade gradient over streamlines on the left
from matplotlib.colors import LinearSegmentedColormap
cm=LinearSegmentedColormap.from_list("f",[(0x0f/255,0x1b/255,0x2d/255,1.0),(0x0f/255,0x1b/255,0x2d/255,0.0)])
ax.imshow(np.linspace(0,1,500)[None,:]**0.8,cmap=cm,extent=[0,2*np.pi*0.62,0,1.6*np.pi],aspect="auto",zorder=3)
ax.scatter(px[keep],py[keep],s=1.6,color=ivory,alpha=0.9,lw=0,zorder=4)
ax.set_xlim(0,2*np.pi); ax.set_ylim(0,1.6*np.pi); ax.axis("off")
fig.savefig("art.png",dpi=400,facecolor=navy)
