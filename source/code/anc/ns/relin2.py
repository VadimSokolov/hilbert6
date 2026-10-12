"""With the c^4 term removed by re-linearisation, does the error fall like sqrt(D/M)
and cross the Laplace/BvM error?"""
import numpy as np, json, time
exec(open('relin.py').read().split("r=np.random.default_rng(555)")[0])
r=np.random.default_rng(777); Lc=np.linalg.cholesky(Cov)
out={'laplace':score(th_map+(Lc@r.normal(size=(D,8000))).T)}
print("Laplace %.4f"%out['laplace'],flush=True)
c=5.0; Mmax=1100
TH=th_map+c*(Lc@r.normal(size=(D,Mmax))).T
t0=time.time(); GG=np.array([G(TH[m]) for m in range(Mmax)])
Ysim=GG+SIGMA*r.normal(size=(Mmax,2*N))
S=np.array([S_k(Ysim[m],2) for m in range(Mmax)]); s_obs=S_k(Y,2)
print("summaries built %.0fs"%(time.time()-t0),flush=True)
for M in [300,600,1100]:
    for lin in [False,True]:
        if lin:
            X=np.hstack([np.ones((M,1)),S[:M]]); B=np.linalg.lstsq(X,TH[:M],rcond=None)[0]
            R=TH[:M]-X@B; ctr=np.r_[1,s_obs]@B
        else:
            R=TH[:M]-S[:M]; ctr=s_obs
        C=np.cov(R.T); L=np.linalg.cholesky(C+1e-10*np.eye(D)); W=np.linalg.solve(L,R.T).T
        idx=r.integers(0,M,8000)
        out[f'M{M}_{"lin" if lin else "id"}']=score(ctr+(L@W[idx].T).T)
    print("M=%4d  id %.4f  lin %.4f"%(M,out[f'M{M}_id'],out[f'M{M}_lin']),flush=True)
json.dump(out,open('relin2.json','w'),indent=1)
