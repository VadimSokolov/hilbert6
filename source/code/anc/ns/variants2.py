import numpy as np, json
d=np.load('cache.npz'); r=np.random.default_rng(9)
post=d['post']; th_map=d['th_map']; Cov=d['Cov']; J=d['J']; g_map=d['g_map']
Y=d['Y']; SIGMA=float(d['SIGMA']); prior_sd=d['prior_sd']; D=len(th_map)
Fi=np.linalg.inv(J.T@J/SIGMA**2+np.diag(1/prior_sd**2))
def summ(Yv): return th_map+Fi@(J.T@(Yv-g_map)/SIGMA**2-th_map/prior_sd**2)
s_obs=summ(Y)
def w1(a,b):
    q=np.linspace(0.005,0.995,199); return np.mean(np.abs(np.quantile(a,q)-np.quantile(b,q)))
def score(s): return float(np.mean([w1(s[:,j],post[:,j])/np.std(post[:,j]) for j in range(D)]))
TH=d['TH_l']; GG=d['GG_l']; SCL=3.0
Lc=np.linalg.cholesky(Cov)
def logprior(t): return -0.5*np.sum((t/prior_sd)**2,axis=-1)
def logprop(t):
    z=np.linalg.solve(SCL*Lc,(t-th_map).T).T; return -0.5*np.sum(z**2,axis=-1)
def build(M,weighted,linear):
    S=np.array([summ(GG[m]+SIGMA*r.normal(size=len(Y))) for m in range(M)])
    Tm=TH[:M]
    lw=logprior(Tm)-logprop(Tm) if weighted else np.zeros(M)
    w=np.exp(lw-lw.max()); w/=w.sum()
    if linear:
        X=np.hstack([np.ones((M,1)),S])
        Wd=np.diag(w); B=np.linalg.solve(X.T@Wd@X+1e-8*np.eye(D+1), X.T@Wd@Tm)
        R=Tm-X@B; ctr=np.r_[1,s_obs]@B
    else:
        R=Tm-S; ctr=s_obs
    mu=(w[:,None]*R).sum(0); Rc=R-mu
    C=(w[:,None]*Rc).T@Rc/(1-np.sum(w**2)); L=np.linalg.cholesky(C+1e-10*np.eye(D))
    Wn=np.linalg.solve(L,Rc.T).T
    idx=r.choice(M,size=8000,p=w)
    return ctr+mu+(L@Wn[idx].T).T
lap=th_map+(Lc@r.normal(size=(D,8000))).T
print("Laplace/BvM %.4f"%score(lap))
out={'laplace':score(lap)}
for M in [400,800,1600]:
    for wt in [False,True]:
        for lin in [False,True]:
            k="M%d_%s_%s"%(M,'IW' if wt else 'noIW','lin' if lin else 'id')
            out[k]=score(build(M,wt,lin)); print("%-20s %.4f"%(k,out[k]))
json.dump(out,open('variants2.json','w'),indent=1)
