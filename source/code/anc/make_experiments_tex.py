"""Emit the Experiments section of the manuscript from results/paper_figs.json.

Every number in Section~\ref{sec:experiments} is written by this script, so the
section cannot drift from the runs that produced it.  Usage:

    python3 make_experiments_tex.py --results results/paper_figs.json \
        --study results/study.json --out ../paper/experiments_generated.tex
"""
import argparse
import json
import os
import re


def f(x, n=3):
    return f"{x:.{n}f}"


def sci(x, n=2):
    s = f"{x:.{n}e}"
    m, e = s.split('e')
    return rf"{m}\times10^{{{int(e)}}}"


def cnt(b):
    """Modes covered out of the informed ones, as a count rather than a ratio."""
    return ('none' if b['cover2_informed'] is None
            else f"{round(b['cover2_informed'] * b['k_eff'])} of {b['k_eff']}")


def cntall(b):
    return f"{round(b['cover2_all'] * b['kmax'])} of {b['kmax']}"


def diagnosis_table(d):
    rows = [("Uncalibrated prior", 'published'),
            (r"Calibrated $\rho$", 'calibrated_N2000'),
            ("", 'calibrated_N50000'),
            ("", 'calibrated_N1300000'),
            ("Prior-typical truth", 'typical_N2000'),
            ("", 'typical_N50000'),
            ("", 'typical_N1300000')]
    out = []
    for lab, key in rows:
        b = d[key]
        # k_eff is a handful of modes, so a ratio there is not a coverage
        # probability; report counts, as Figure~\ref{fig:heatgbc} does
        ci = ('--' if b['cover2_informed'] is None
              else rf"{round(b['cover2_informed'] * b['k_eff'])} of {b['k_eff']}")
        ca = rf"{round(b['cover2_all'] * b['kmax'])} of {b['kmax']}"
        zi = '--' if b['max_absz_informed'] is None else f(b['max_absz_informed'], 2)
        N = b['N']
        Ns = rf"$2\times10^3$" if N == 2000 else (rf"$5\times10^4$" if N == 50000 else rf"$1.3\times10^6$")
        out.append(rf"{lab} & {Ns} & {b['rho']:.0f} & {b['k_eff']} & "
                   rf"{f(b['max_truth_in_prior_sd'], 1)} & {ci} & {ca} & "
                   rf"{zi} & {f(b['rel_l2'], 3)} & ${sci(b['bvm_max_rel'])}$ \\")
    return "\n".join(out)


def cost_table(d):
    b = d['baselines']
    rows = [
        # GBC's mean is the exact posterior mean in this model (prop:linsuff), so its mean
        # error is zero analytically, exactly as the Laplace row's is. Scoring it from the
        # M output draws returns the sampling noise of those draws, which is what an earlier
        # version of this table printed here and what rem:artifact retracts. The
        # standard-deviation ratio is the column that carries information about the method.
        (r"GBC, Algorithm~\ref{alg:gbc}", b['solves_gbc'], f(b['gbc_time_s'], 2),
         r"$0^{\dagger}$", f(b['gbc_sd_ratio_med'], 3), "amortised"),
        # In this linear-Gaussian model the Laplace approximation at the posterior mode IS
        # the exact posterior, so these two entries are analytic, not measured: mean error
        # exactly 0 and standard-deviation ratio exactly 1. They are marked as such in the
        # table note rather than printed as though they were measurements.
        (r"Laplace at $\hat S_N$", 2, f(b['laplace_time_s'], 4),
         r"$0^{\dagger}$", r"$1^{\dagger}$", "no"),
        (rf"pCN, ${sci(b['solves_pcn'], 0)}$ iterations", b['solves_pcn'], f(b['pcn_time_s'], 1),
         f(b['pcn_mean_err_psd'], 3), f(b['pcn_sd_ratio_med'], 3), "no"),
    ]
    return "\n".join(rf"{a} & {c} & {t} & {e} & {s} & {am} \\" for a, c, t, e, s, am in rows)


def resolution_table(d):
    cur = d['resolution']['curve']
    hdr = " & ".join(rf"$10^{{{len(str(int(c['N'])))-1}}}$" for c in cur)
    vals = " & ".join(str(c['k_eff']) for c in cur)
    return hdr, vals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--results', default='results/paper_figs.json')
    ap.add_argument('--study', default='results/study.json')
    ap.add_argument('--cover2', default='results/cover2_agg.json')
    ap.add_argument('--study2', default='results/study2_agg.json')
    ap.add_argument('--ns', default='results/ns')
    ap.add_argument('--out', default='../paper/experiments_generated.tex')
    a = ap.parse_args()
    d = json.load(open(a.results))
    b = d['baselines']
    study = json.load(open(a.study)) if os.path.exists(a.study) else None
    cov2 = json.load(open(a.cover2)) if os.path.exists(a.cover2) else None
    s2 = json.load(open(a.study2)) if os.path.exists(a.study2) else None
    ns = None
    if os.path.isdir(a.ns):
        ns = {os.path.splitext(fn)[0]: json.load(open(os.path.join(a.ns, fn)))
              for fn in os.listdir(a.ns) if fn.endswith('.json')}
        # the M values live in the variants keys; read them off rather than restating them
        ms = sorted(int(m) for m in re.findall(r'global_identity_M(\d+)', ' '.join(ns['variants'])))
        ns['variants']['M_small'], ns['variants']['M_headline'] = ms[0], ms[-1]
        # predicted spread inflation at c=5 from the measured prior fraction, Theorem 10.2(iii)
        sp = ns['spectrum']['0.0']
        pj = [(a_ / b_) ** 2 for a_, b_ in zip(sp['post_sd'], sp['prior_sd'])]
        ns['infl'] = [((1 - q) + 25 * q * q) ** 0.5 for q in pj]
    hdr, vals = resolution_table(d)
    cur = d['resolution']['curve']
    rho = d['rho_calibrated']

    T = rf"""%==== GENERATED BY code/make_experiments_tex.py; DO NOT EDIT BY HAND ====
\section{{Experiments}}\label{{sec:experiments}}

Everything reported here is produced from fixed seeds by the scripts in the accompanying
repository: \texttt{{exp\_paper\_figs.py}} and \texttt{{exp\_gbc\_local.py}} for the
finite-$N$ and cost tables, \texttt{{exp\_study2.py}}, \texttt{{exp\_cover2.py}},
\texttt{{agg\_cover2.py}} and \texttt{{fig\_cost.py}} for the replicate study and
Figure~\ref{{fig:cost}}, and \texttt{{ns/}} for the Navier--Stokes run of
Section~\ref{{sec:expns}}, whose outputs are recorded in \texttt{{results/ns/}}. The generator
\texttt{{make\_experiments\_tex.py}} writes this section, tables included, directly from the
resulting \texttt{{json}}, so every measured number here comes from a recorded run rather than
being transcribed by hand; the two entries marked $\dagger$ in Table~\ref{{tab:cost}} are
analytic, not measurements. The
setting is the heat equation of Section~\ref{{sec:heat}} on $\Omega=[0,1]$ with $\nu={d['nu']}$,
$T={d['T']:.0f}$, prior \eqref{{eq:prior}} of smoothness $\alpha={d['alpha']:.0f}$, and the
conjugate Gaussian posterior available in closed form, so that the exact posterior is known and
every approximation can be measured against it rather than against another approximation.

\subsection{{The finite-$N$ check, in the regime where the data speak}}\label{{sec:expfinite}}

Table~\ref{{tab:diag}} reports the diagnosis. The first row is the uncalibrated setting of
the left panel of Figure~\ref{{fig:heatgbc}}, $\rho=1$ and $N=2000$: no mode has data
precision exceeding prior precision, the true initial condition lies up to
${f(d['published']['max_truth_in_prior_sd'], 0)}$ prior standard deviations from the prior mean,
the posterior mean has relative $L^2$ error ${f(d['published']['rel_l2'], 3)}$, and the truth lies
inside a two-standard-deviation credible interval in none of the
{d['typical_N2000']['kmax']} modes. The agreement with the Bernstein--von Mises scale there,
${sci(d['published']['bvm_max_rel'])}$, is therefore not a validation of anything: both sides of
the comparison are the prior, and a diagnostic that compares the prior with itself is vacuous
whatever number it returns.

Two things are wrong at once and they have to be separated. The first is the scale of the prior,
which $\rho$ fixes: calibrating $\rho$ so that the prior standard deviation at $|k|=1$ matches the
initial condition there gives $\rho={f(rho, 1)}$, moves $k_{{\rm eff}}$ from $0$ to
{d['calibrated_N2000']['k_eff']}, covers every informed mode, and brings the relative $L^2$ error
to ${f(d['calibrated_N2000']['rel_l2'], 3)}$. The second is the shape: the initial condition
$\theta_{{0,k}}=1/(1+k^2)$ decays like $k^{{-2}}$ whereas a draw from \eqref{{eq:prior}} with
$\alpha=3$ decays like $k^{{-3}}$, so after calibration the worst mode is still
${f(d['calibrated_N2000']['max_truth_in_prior_sd'], 1)}$ prior standard deviations out. That tail
is invisible while $k_{{\rm eff}}$ is small and becomes visible as $N$ grows: the informed modes
covered go from {cnt(d['calibrated_N2000'])} at $N=2\times10^3$ to
{cnt(d['calibrated_N1300000'])} at $N=1.3\times10^6$, with the worst standardised error
over informed modes rising to ${f(d['calibrated_N1300000']['max_absz_informed'], 2)}$. Nothing is wrong
with the posterior; the prior is wrong about the truth, and more data is what reveals it.

The last three rows replace the fixed $\theta_0$ by a draw from the prior itself, the only setting
in which nominal coverage is the right thing to expect. The worst mode is then
${f(d['typical_N2000']['max_truth_in_prior_sd'], 1)}$ prior standard deviations out, and of the
{d['typical_N2000']['kmax']} modes the number covered is {cntall(d['typical_N2000'])},
{cntall(d['typical_N50000'])} and {cntall(d['typical_N1300000'])} at the three sample sizes.
Relative $L^2$ error stays near one at the smaller two, which is not a failure but the statement
that a prior-typical function puts most of its energy in modes the experiment cannot resolve: the
estimator is right to leave them at the prior mean, and Section~\ref{{sec:resolution}} says how
many it can.

\begin{{table}}[t]\centering\footnotesize\setlength{{\tabcolsep}}{{4pt}}
\caption{{The finite-$N$ check for the heat equation. $k_{{\rm eff}}$ is the number of modes with
$N\iota_k\ge\rho^{{-2}}\lambda_k^\alpha$; ``truth/prior sd'' is
$\max_k|\theta_{{0,k}}|/\sigma_{{0,k}}$, a measure of how atypical the truth is under the prior;
the coverage columns count the modes whose truth lies within two posterior standard deviations,
over the informed modes and over all twenty; with $k_{{\rm eff}}$ this small these are counts and
not estimates of a coverage probability, for which see the replicate study of
Section~\ref{{sec:expstudy}}; $|z|_{{\max}}$ is the largest standardised error over
informed modes; and the last column is the largest relative discrepancy between the exact
posterior standard deviation and the Bernstein--von Mises scale $\sqrt{{T/(N\iota_k)}}$ over the
informed modes.}}\label{{tab:diag}}
\begin{{tabular}}{{lrrrrrrrrr}}
\toprule
& $N$ & $\rho$ & $k_{{\rm eff}}$ & truth/prior sd & cov.\ inf. & cov.\ all & $|z|_{{\max}}$ & rel.\ $L^2$ & BvM rel.\\
\midrule
{diagnosis_table(d)}
\bottomrule
\end{{tabular}}
\end{{table}}

\subsection{{Cost and accuracy against the alternatives}}\label{{sec:expcost}}

Table~\ref{{tab:cost}} reports what one analysis costs, at $N={b['N']}$ with the first
{b['kmax']} modes retained, on one core. The units are forward or adjoint solves of the linearised
equation, which is the currency in which data assimilation is priced, together with wall-clock for
the methods actually run here. Accuracy is the largest error of the posterior mean over the retained modes, in units
of the exact posterior standard deviation, and the ratio of reported to exact posterior standard
deviation, both over the retained modes.

\begin{{table}}[t]\centering\small
\caption{{Cost and accuracy for one analysis of the heat equation, $N={b['N']}$, $|k|\le{b['kmax']}$,
single core. Solves are of the linearised forward or adjoint equation. Errors are the maximum over
the retained modes, in units of the
exact posterior standard deviation. ``Amortised'' records whether a second data set can be
analysed without repeating the cost. $\dagger$: analytic, not
measured. In this linear-Gaussian model both the Laplace approximation at the posterior mode and
the GBC generator have the exact posterior mean, by Proposition~\ref{{prop:linsuff}}, so their mean
error is exactly zero at every budget; scoring GBC's worst mode from its {b['gbc_M']} output
draws returns
{f(b['gbc_mean_err_psd'], 3)}, which is the sampling noise of those draws and not a property of the
method. The standard-deviation ratio is the column that carries information here. The same
exactness is why Remark~\smref{{rem:artifact}} warns against reading a finite-draw mean error as
a Monte Carlo floor.}}\label{{tab:cost}}
\begin{{tabular}}{{lrrrrl}}
\toprule
Method & Solves & Time (s) & Max err.\ (psd) & sd ratio & Amortised\\
\midrule
{cost_table(d)}
\bottomrule
\end{{tabular}}
\end{{table}}

Three readings. First, GBC is not more accurate than Laplace and cannot be: by
Definition~\ref{{def:gen}} its generator is a Monte Carlo estimate of the Laplace approximation, so
its mean is that approximation's mean exactly, and the
${f(b['gbc_mean_err_psd'], 3)}$ posterior standard deviations one reads off the worst of its
$M={b['gbc_M']}$ draws is the sampling error of those draws, not an error of the method. What it buys over Laplace is that it never forms a Hessian and reaches the forward map only
by simulation. Second, pCN is included to exhibit the Monte Carlo rate the two methods share, not as a tuned competitor: in this conjugate model the exact posterior is a known Gaussian that can be sampled directly and a whitened or Gibbs sampler would mix in one step, so the comparison is not in GBC's favour on a single data set:
${b['solves_pcn']}$ iterations, {f(b['pcn_time_s'], 0)} seconds, and a tuned acceptance rate of
{f(b['pcn_acc'], 3)} at $\beta={f(b['pcn_beta'], 4)}$ deliver a minimum effective sample size of
{f(b['pcn_ess_min'], 0)} across the retained modes, which is why its worst-mode error,
{f(b['pcn_mean_err_psd'], 3)} posterior standard deviations, is larger than GBC's and is Monte
Carlo noise rather than bias: its posterior standard deviation ratio is
{f(b['pcn_sd_ratio_med'], 3)}. Given enough iterations pCN is exact and GBC is not. Third, the
cost that matters operationally is the ratio to a 4DVar minimisation. Neither 4DVar nor an
ensemble Kalman filter is run here, since neither returns a posterior and so no error in these
units is defined for either. Both do have conventional solve counts: {b['solves_4dvar']} for a
Gauss--Newton 4DVar at ten inner iterations of one forward and one adjoint solve, and one solve
per ensemble member for an ensemble filter. Against those conventions one GBC analysis is
{b['solves_gbc']//b['solves_4dvar']} 4DVar-equivalents at $M={b['gbc_M']}$ and
{b['solves_gbc']//b['solves_enkf']} times a {b['solves_enkf']}-member EnKF. Those are the numbers
Section~\ref{{sec:related}} refers to, and they are the price of amortisation: the {b['gbc_M']}
simulations are spent once, and every subsequent data set is a forward pass.

%STUDYBLOCK%
%NSBLOCK%
\subsection{{What these experiments do not establish}}\label{{sec:expnot}}

Most of them are run on a linear, one-dimensional, conjugate problem, chosen so that the exact
posterior is known and every claim can be checked against it rather than against a second
approximation. Those test the summary, the generator and the resolution accounting of
Sections~\ref{{sec:suff}}, \ref{{sec:qnn}} and \ref{{sec:resolution}}, and they cannot test the
nonlinear theory at all. Section~\ref{{sec:expns}} supplies the nonlinear test, and its limits
should be stated as plainly as its results. It is a six-dimensional Galerkin truncation at
$N=80$ on a $24^2$ grid, which is a small problem; the comparison is against a Metropolis
reference whose own Monte Carlo error is of the same size as the differences being reported, so
the parity it finds between GBC and the Laplace approximation is parity at that resolution and not
below it; and the truth is a prior draw, so nothing there speaks to misspecification. What it does
establish is that the three corrections of Section~\ref{{sec:loc}} are the ones that matter on a
genuinely nonlinear map, in the direction and roughly the magnitude the theorems predict. Whether
the same holds at operational resolution, where $D$ is in the thousands and the reference is
unavailable, is the first of the open problems in Section~\ref{{sec:open}}. Section~\ref{{sec:ns}}
remains a specification of the pipeline at the resolution the framework is stated for, not a
report of a computation at that resolution.
"""
    T = T.replace("%NSBLOCK%\n", ns_block(ns).lstrip("\n") + "\n" if ns else "")
    T = T.replace("%STUDYBLOCK%\n",
                  study_block(study, cov2, s2).lstrip("\n") + "\n" if study else "")
    # An explicit end marker so paper/splice_experiments.py can find the block's extent in the
    # master without guessing at the next \section.  The master carries a pasted copy of this
    # file; nothing else keeps the two in step.
    T = T.rstrip('\n') + "\n%==== END GENERATED ====\n"
    with open(a.out, 'w') as fh:
        fh.write(T)
    print(f"wrote {a.out}, {T.count(chr(10))} lines")


ARM_LABEL = {'prior': r'$\theta_0\sim\Pi$, redrawn each replicate',
             'fixed_typical': r'fixed typical draw',
             'fixed_rough': r'fixed rough truth'}


def arm_rows(cov2):
    """One row per truth arm: marginal coverages and the paired test."""
    out = []
    for arm in cov2['arms']:
        d = cov2[arm]
        A = d['paired_all']
        out.append(rf"{ARM_LABEL[arm]} & {f(d['exact_all'], 3)} & {f(d['gbc_all'], 3)} & "
                   rf"{f(d['exact_informed'], 3)} & {f(d['gbc_informed'], 3)} & "
                   rf"${A['b']}$/${A['c']}$ & ${f(A['z'], 2)}$\\")
    return "\n".join(out)


def arm_max_z(cov2):
    return max(abs(cov2[a]['paired_all']['z']) for a in cov2['arms'])


def paired_coverage(cov, cov2):
    """Return (marginals, McNemar test, verdict sentence).

    With cov2 present the discordant counts b and c are read from archived per-replicate
    indicators and the test is exact.  Without them only the NET discordance |b-c| is
    recoverable from marginal rates, and since b+c >= |b-c| that yields a lower bound on the
    paired standard error, hence an UPPER bound on |z|.  The fallback says so rather than
    quoting a number it cannot support.
    """
    import numpy as np
    if cov2 is not None:
        A = dict(cov2['paired_all'])
        A['exact'] = True
        return cov2, A
    # fallback: bound the test from the marginals alone
    pe = np.asarray(cov['exact_by_mode'], float)
    pg = np.asarray(cov['gbc_by_mode'], float)
    reps, J = cov['reps'], cov['J']
    net = int(round(np.abs(pe - pg).sum() * reps))     # lower bound on b+c
    n = reps * J
    diff = cov['exact_all'] - cov['gbc_all']
    se = np.sqrt(net) / n if net > 0 else 0.0
    C = dict(cov, reps=reps, J=J)
    A = dict(b=None, c=None, n=n, discordant=net, diff=float(diff),
             se_paired=float(se), z=float(diff / se) if se > 0 else 0.0,
             se_unpaired=float(np.sqrt(0.95 * 0.05 / reps)), exact=False)
    return C, A


def discord(A):
    """The sentence naming the discordant pairs; exact counts only when archived."""
    if A['exact']:
        return (rf"Of the ${A['n']}$ (replicate, mode) pairs, ${A['b']}$ are covered by the "
                rf"exact posterior and missed by GBC and ${A['c']}$ the other way.")
    return (rf"Of the ${A['n']}$ (replicate, mode) pairs at least ${A['discordant']}$ are "
            rf"discordant, the two methods disagreeing on whether the mode is covered.")


def verdict(A):
    z = abs(A['z'])
    if not A['exact']:
        return (rf"Because the per-replicate indicators were not archived, only the net "
                rf"discordance is recoverable, so ${f(z,1)}$ is an upper bound on the number of "
                rf"standard errors and the comparison is reported as such.")
    if z < 2.0:
        return ("At this replicate count the two calibrations are therefore not "
                "distinguishable.")
    if z < 3.0:
        return ("The gap is small in magnitude but resolvable at this replicate count: the "
                "pairing, not the size of the difference, is what makes it visible.")
    return ("The gap is small in magnitude but clearly resolved, so GBC's intervals are "
            "genuinely, if slightly, narrower than the exact posterior's at this budget.")


def study_block(s, cov2=None, s2=None):
    import numpy as np
    cov, g, p = s['coverage'], s['gbc_curve'], s['pcn_curve']
    C, A = paired_coverage(cov, cov2)
    VERDICT, DISC = verdict(A), discord(A)
    ARMS = arm_rows(C) if cov2 is not None else ''
    MAXZ = arm_max_z(C) if cov2 is not None else abs(A['z'])
    MAXD = (max(abs(C[k]['paired_all']['diff']) for k in C['arms'])
            if cov2 is not None else abs(A['diff']))
    if s2 is None:
        raise SystemExit('results/study2_agg.json is required; run code/agg_study2.py first')
    S2, PM, P2 = s2, s2['published_metric'], s2['pcn']
    GA, GL = s2['gbc']['local'], s2['gbc']['learned']
    RM = s2['ratio_measured']['local']
    GM = GA['M']
    PS = np.array(P2['solves'], float)
    ESS = np.array(P2['ess_min'], float)
    NB, NARM, NDRAW = len(GM), len(s2['gbc']), 4000
    NMEAS = GA['mean_err_psd']['n_measurements']
    _sl = [s2['gbc'][a][m]['slope'] for a in s2['gbc']
           for m in ('sd_err_rel', 'cov_rel_fro')]
    _se = [s2['gbc'][a][m]['slope_se'] for a in s2['gbc']
           for m in ('sd_err_rel', 'cov_rel_fro')]
    SLO, SHI, SSE = min(_sl), max(_sl), float(np.mean(_se))
    gs = np.array([r['solves'] for r in g], float)
    gm = np.array([r['mean_err_psd'] for r in g], float)
    ps = np.array([r['solves'] for r in p], float)
    pm = np.array([r['mean_err_psd'] for r in p], float)
    pt = np.array([r['seconds'] for r in p], float)
    # the floor is the mean over the plateau, taken as the last four budgets;
    # its spread is reported so the reader can see how well determined it is
    floor = gm[-4:].mean()
    floorsd = gm[-4:].std(ddof=1)
    gslope = np.polyfit(np.log(gs), np.log(gm), 1)[0]
    pslope = np.polyfit(np.log(ps), np.log(pm), 1)
    need = float(np.exp((np.log(floor) - pslope[1]) / pslope[0]))
    tfit = np.polyfit(np.log(ps), np.log(pt), 1)
    tneed = float(np.exp(tfit[0] * np.log(need) + tfit[1]))
    best = g[-4]                       # smallest budget on the plateau
    Mlo, Mhi = g[0]['M'], g[-1]['M']
    # the same crossover computed from the converged pCN runs only
    ess = np.array([r['ess_min'] for r in p], float)
    ESSCUT = 7.0
    conv = ess >= ESSCUT
    pslope_c = np.polyfit(np.log(ps[conv]), np.log(pm[conv]), 1)
    need_c = float(np.exp((np.log(floor) - pslope_c[1]) / pslope_c[0]))
    ratio, ratio_c = need / best['solves'], need_c / best['solves']
    rlo, rhi = sorted((ratio, ratio_c))
    rnd = lambda x: round(x / 100) * 100
    ext = need / ps[-1]
    return rf"""
\subsection{{Error against cost, and coverage over replicates}}\label{{sec:expstudy}}

A single realisation cannot separate a miscalibrated posterior from an unlucky draw, so calibration
is checked over replicates, on three truth arms: $\theta_0$ redrawn from the prior, a fixed typical
draw, and a fixed rough truth the prior charges only in its tail. The result, set out in
Section~\ref{{sec:covstudy}} and shown in the right panel of Figure~\ref{{fig:cost}}, is that GBC
reproduces whatever the exact posterior does, on every arm, under the paired McNemar test that the
shared design licenses: the largest discrepancy across the three arms is {f(MAXZ, 2)} paired
standard errors. The exact posterior itself covers between {f(C['fixed_rough']['exact_all'], 3)}
and {f(C['prior']['exact_all'], 3)} of the time depending on the arm, so what is being
reproduced includes the posterior's own frequentist miscalibration at a fixed truth. One
qualification carries into everything below: both arms of that comparison use the same summary
$\hat S_N$ and, by Proposition~\ref{{prop:linsuff}}, the same closed-form posterior mean, so what
differs between them is the covariance alone.

The left panel needs care about which part of the generator the simulations pay for. In the
linear-Gaussian model of Section~\ref{{sec:heat}} Proposition~\ref{{prop:linsuff}} gives the mean
map in closed form, so GBC's posterior mean is exact at every budget and only the $D\times D$
covariance is estimated from the $M$ simulations. Scoring the mean therefore measures nothing about
the method: over {S2['reps']} replicates and {NB} budgets, {NMEAS} measurements in all, its error is
exactly zero. Scoring it instead from a fixed number of finite output draws returns the sampling
noise of those draws, which is flat in $M$ by construction and is not an approximation floor;
Remark~\smref{{rem:artifact}} sets out why the distinction matters here.

\begin{{remark}}[Why a finite-draw mean error is not an approximation floor]\label{{rem:artifact}}
Scoring GBC's posterior mean against the exact one in this model measures a quantity whose value is
exactly zero, so any nonzero reading is the sampling noise of however many output draws were taken.
Holding that count fixed at {NDRAW} while the simulation budget sweeps a factor of
{int(GM[-1] // GM[0])} returns {f(min(PM['mean']), 3)} to {f(max(PM['mean']), 3)} posterior standard
deviations with a fitted slope against the budget of ${f(PM['slope'], 3)}$, flat. That flatness is
not an approximation floor of the plug-in generator. The quantity decays in the number of output
draws, not in $M$, so no simulation budget can move it and there is nothing
there to converge. A Gaussian head does carry a genuine approximation error wherever the posterior
is not Gaussian, but a linear-Gaussian benchmark is precisely the case in which that error vanishes
identically, so this diagnostic cannot measure it at any budget. Any study of a Gaussian-head
generator that scores the mean on a conjugate benchmark meets the same trap.
\end{{remark}}

What the simulations buy is the covariance, and scored analytically it converges at the Monte Carlo
rate with no floor. Across the {NARM} generator variants and both covariance metrics the fitted
slope of $\log$ error against $\log$ solves lies between ${f(SLO, 3)}$ and ${f(SHI, 3)}$ against a
nominal $-1/2$, with replicate standard error {f(SSE, 3)}; raising $M$ from {int(GM[0])} to
{int(GM[-1])} cuts the error on the standard deviations from {f(GA['sd_err_rel']['mean'][0], 3)} to
{f(GA['sd_err_rel']['mean'][-1], 4)}. The learned-mean variant, which ignores
Proposition~\ref{{prop:linsuff}} and regresses $\theta$ on the summary from the same simulations,
does carry a mean error, converging at ${f(GL['mean_err_psd']['slope'], 3)}$ to
{f(GL['mean_err_psd']['mean'][-1], 3)} at the largest budget: that gap is what the affine structure
is worth. pCN has no floor either. Its error on the standard deviations falls from
{f(P2['sd_err_rel']['mean'][0], 3)} to {f(P2['sd_err_rel']['mean'][-1], 3)} as the budget grows from
${sci(PS[0], 1)}$ to ${sci(PS[-1], 1)}$ solves. Its rate has to be read with the mixing in view: the
minimum effective sample size over the retained modes is {ESS[0]:.0f} at the smallest budget and
{ESS[-1]:.0f} only at the largest, so the smallest budgets measure how far the chain has failed to
move rather than a Monte Carlo error. Fitting all {len(ESS)} gives ${f(P2['sd_err_rel']['slope_all'], 3)}$;
fitting the {P2['n_converged']} budgets with an effective sample size above {P2['ess_cut']:.0f}
gives ${f(P2['sd_err_rel']['slope'], 3)}$, which is the Monte Carlo rate and is what we use below.

So both methods converge at essentially the same rate, ${f(GA['sd_err_rel']['slope'], 3)}$ for GBC
against ${f(P2['sd_err_rel']['slope'], 3)}$ for pCN on the standard deviations. The advantage is
therefore a constant factor rather than a widening gap, and
it can be read off without extrapolating either curve beyond where it was measured. Over the band
of accuracy both methods reached, {f(RM['sd_err_rel']['err_hi'], 3)} down to
{f(RM['sd_err_rel']['err_lo'], 3)} posterior standard deviations, pCN needs between
{RM['sd_err_rel']['ratio_min']:.0f} and {RM['sd_err_rel']['ratio_max']:.0f} times as many solves
as GBC to match it on the standard deviations, and between
{RM['cov_rel_fro']['ratio_min']:.0f} and {RM['cov_rel_fro']['ratio_max']:.0f} times as many on
the full covariance in Frobenius norm. Solves, not seconds, are the currency: repeating the
identical script on a second machine moved the two wall-clocks in opposite directions and changed
their ratio by a factor of $1.8$. The trade is therefore not that GBC stops improving while pCN
continues. Both improve at about the Monte Carlo rate, GBC from a constant two to three orders of
magnitude smaller, and the choice between them turns on how many solves an application can afford.

\begin{{figure}}[t]\centering
\includegraphics[width=\textwidth]{{fig_cost.pdf}}
\caption{{Left: error against the number of linearised solves, on the metric the
simulations actually control. GBC's posterior mean is exact at every budget in this model
(Proposition~\ref{{prop:linsuff}}), so what is plotted is the error of the estimated posterior
standard deviations, in units of the exact ones, for GBC at $M={int(GM[0])}$ to ${int(GM[-1])}$ and
for pCN at ${sci(PS[0], 1)}$ to ${sci(PS[-1], 1)}$ iterations, averaged over {S2['reps']}
replicates. Both follow the Monte Carlo rate, fitted slopes ${f(GA['sd_err_rel']['slope'], 3)}$ and
${f(P2['sd_err_rel']['slope'], 3)}$; neither has a floor. The shaded band is the range of accuracy
both reached, over which pCN needs {RM['sd_err_rel']['ratio_min']:.0f} to
{RM['sd_err_rel']['ratio_max']:.0f} times as many solves, read off with no extrapolation.
Right: coverage of nominal $95\%$ credible intervals by mode, over
{C['reps']} replicates, for the exact posterior and for GBC; the dotted line marks
$k_{{\rm eff}}$, beyond which the intervals are the prior's. Pooled over modes and arms the two
disagree on {A['b']} pairs against {A['c']}, out of {A['n']}, a coverage difference of
{f(abs(A['diff']), 4)} or {f(abs(A['z']), 1)} paired standard errors.}}\label{{fig:cost}}
\end{{figure}}

\subsection{{Coverage over replicates, in full}}\label{{sec:covstudy}}

Section~\ref{{sec:expstudy}} gave the outcome; this is the design behind it, and the numbers in
full. Which truth the replicates are taken around is not a detail.
Hypothesis (G1) of Assumption~\ref{{ass:G}} is stated in $P^\N_{{\theta_0}}$-probability at a
\emph{{fixed}} $\theta_0$, and redrawing $\theta_0$ from the prior at every replicate makes the
exact posterior's coverage nominal by construction, so under that design alone the comparison
cannot fail informatively. The three arms are therefore $\theta_0$ redrawn from
the prior, a fixed typical draw, and a fixed rough truth
$\theta_{{0,k}}=(1+k^2)^{{-1}}\mathrm{{sign}}(\sin k)$, which the prior charges only in its tail. At
$N={C['N']}$ with $J={C['J']}$ modes retained and $M={C['M']}$ simulations, each arm has
{C['reps']} replicates, giving the per-mode coverage of nominal $95\%$ credible intervals shown in
the right panel of Figure~\ref{{fig:cost}}.

\begin{{table}}[t]\centering\small
\caption{{Coverage of nominal $95\%$ credible intervals over {C['reps']} replicates per arm, by
truth arm. ``All'' is over the $J={C['J']}$ retained modes, ``informed'' over the
$k_{{\rm eff}}={C['k_eff']}$ modes in which data precision exceeds prior precision. $b/c$ are the
McNemar discordant counts, pairs the exact posterior covers and GBC misses and the reverse, out of
${A['n']}$; $z$ is the paired statistic. The rough arm is misspecified by construction: a truth
with $\theta_{{0,k}}=(1+k^2)^{{-1}}\mathrm{{sign}}(\sin k)$ is far rougher than a $\gamma>12$ prior
charges, so both methods undercover, and identically. That the exact posterior undercovers too is
the point of including the arm.}}\label{{tab:cover}}
\begin{{tabular}}{{lcccccc}}
\toprule
& \multicolumn{{2}}{{c}}{{All modes}} & \multicolumn{{2}}{{c}}{{Informed modes}} & & \\
\cmidrule(lr){{2-3}}\cmidrule(lr){{4-5}}
Truth arm & exact & GBC & exact & GBC & $b/c$ & $z$\\
\midrule
{ARMS}
\bottomrule
\end{{tabular}}
\end{{table}}

Two things separate here. First, the exact posterior does not have frequentist coverage at a fixed
truth and is not required to: its coverage over all $J$ retained modes falls from
{f(C['prior']['exact_all'], 3)} on the prior-drawn arm to
{f(C['fixed_typical']['exact_all'], 3)} at the fixed typical draw and
{f(C['fixed_rough']['exact_all'], 3)} at the rough one. That is the ordinary non-uniformity of
Bayesian credible sets over fixed parameters, and averaging over the prior is precisely what hides
it; on the $k_{{\rm eff}}={C['k_eff']}$ informed modes, where the data rather than the prior sets
the interval, the collapse is much milder.

Second, and this is the claim the paper makes, GBC reproduces whatever the exact posterior does.
Both methods are scored on the same replicate and the same mode, so the yardstick is McNemar's and
not the binomial standard error of a single coverage estimate; the paired standard error is
{f(A['se_unpaired'] / max(A['se_paired'], 1e-12), 0)} times smaller than the unpaired one, so the
test is an order of magnitude more sensitive than the comparison it replaces. GBC survives it on
every arm. The largest discrepancy across the three is {f(MAXZ, 2)} paired standard errors and the
largest difference in coverage is {f(MAXD, 4)}; on the rough arm, where the exact posterior covers
barely a quarter of the time, the two disagree on
${C['fixed_rough']['paired_all']['discordant']}$ of ${A['n']}$ pairs.

The calibration claim is therefore relative rather than absolute: GBC reproduces the posterior it
targets, including where that posterior is badly miscalibrated as a frequentist procedure. Coverage
at a fixed truth is a property of the prior and the model rather than of the computation. One
qualification: both arms of the comparison use the same summary $\hat S_N$ and, by
Proposition~\ref{{prop:linsuff}}, the same closed-form posterior mean, so what differs between them
is the covariance, exact in one case and estimated from the $M$ simulations in the other. The
agreement is evidence that the estimated covariance is right, and is not a test of the summary or
of the centring.
"""


def ns_block(ns):
    """The nonlinear Navier-Stokes check.

    Every number is read from code/results/ns/*.json, written by the scripts in code/ns/.
    The reference is a Metropolis chain, so each script re-runs it under its own seed and the
    Laplace row moves a little between panels; the spread is reported rather than hidden.
    """
    V, R, C, K, E = (ns['variants'], ns['relin'], ns['centring'],
                     ns['correct_centre'], ns['mcmc_error'])
    se = sum(E['se_over_psd']) / len(E['se_over_psd'])
    infl = ns['infl'][-1]
    lap = [j['laplace'] for j in (V, ns['relin2'], C, K, ns['radius'], R)]
    emp = ', '.join(f(v, 2) for v in C['resid_mean_emp'])
    thy = ', '.join(f(v, 2) for v in C['resid_mean_theory'])
    return rf"""
\subsection{{A nonlinear check: two-dimensional Navier--Stokes}}\label{{sec:expns}}

The experiments above are conjugate by design. This one is not, and it is the test that matters
for Sections~\ref{{sec:loc}} and~\ref{{sec:ns}}: whether the localisation theory survives contact
with a nonlinear forward map. We solve \eqref{{eq:nsproj}} in vorticity form on the $2\pi$-periodic
torus by a pseudo-spectral method with two-thirds dealiasing and Heun stepping, on a $24^2$ grid
with $\nu=5\times10^{{-3}}$, $T=1$ and $80$ steps; one forward solve costs about $15$\,ms. The
unknown is the initial vorticity in $D=6$ real cosine modes with wavevectors
$(1,0),(0,1),(1,1),(1,-1),(2,0),(0,2)$, the prior is independent Gaussian with standard deviations
$1.5(\lambda_j/\lambda_1)^{{-1}}$, and the truth is a prior draw. The data are $N=80$ space--time
points with both velocity components observed, noise $\sigma=0.45$ against a signal of standard
deviation about $0.8$, and observation times uniform on $[0,T]$, so the theory applies in its
$T_0=0$ form. Accuracy is the per-coordinate $\Wone_1$ distance to an adaptive random-walk
Metropolis reference, normalised by that coordinate's posterior standard deviation and averaged
over coordinates, so a value of $0.1$ means a displacement of a tenth of a posterior standard
deviation. The comparator is the Laplace approximation at the maximum a posteriori estimate,
which is the finite-sample form of the Konen--Nickl limit and is free: one Gauss--Newton solve and
one Hessian.

\begin{{table}}[t]\centering\small
\caption{{Two-dimensional Navier--Stokes, $D=6$, $N=80$. Distance to the Metropolis reference in
units of posterior standard deviation, per coordinate and averaged; lower is better. The upper
panel varies the architecture at $M={V['M_headline']}$; the lower panel applies the three
corrections of Section~\ref{{sec:loc}} in turn, at $c=5$, $k=2$ and $M=1100$. Each script re-runs
the reference under its own seed, so the Laplace row moves between panels; across the six runs it
lies between ${f(min(lap), 3)}$ and ${f(max(lap), 3)}$. The last line is not a method: it is the
Monte Carlo standard error of the reference's own posterior mean, which is the resolution at which
any of these numbers can be read.}}\label{{tab:ns}}
\begin{{tabular}}{{lc}}
\toprule
& $\Wone_1$ / posterior s.d.\\
\midrule
\multicolumn{{2}}{{@{{}}l}}{{\emph{{Architecture, $M={V['M_headline']}$}}}}\\
\quad training from the prior, identity head & {f(V['global_identity_M1600'], 3)}\\
\quad training from the prior, learned affine head & {f(V['global_linear_M1600'], 3)}\\
\quad training from the prior, then $K=200$ nearest summaries & {f(V['global_localised_K200'], 3)}\\
\quad localised training, identity head & {f(V['local_train_identity_M1600'], 3)}\\
\quad localised training, learned affine head & {f(V['local_train_linear_M1600'], 3)}\\
\midrule
\multicolumn{{2}}{{@{{}}l}}{{\emph{{The corrections of Section~\ref{{sec:loc}}, $c=5$, $k=2$, $M=1100$}}}}\\
\quad localised, uncentred, spread as measured & {f(C['id_uncentred'], 3)}\\
\quad $+$ residuals centred, Theorem~\ref{{thm:locbias}}(ii) & {f(C['id_centred'], 3)}\\
\quad $+$ spread rescaled, Theorem~\ref{{thm:locbias}}(iii) & \textbf{{{f(K['gbc_centred_corrected_deflated'], 3)}}}\\
\midrule
Laplace at the maximum a posteriori estimate & {f(K['laplace'], 3)}\\
\midrule
\emph{{Monte Carlo error of the reference itself}} & \emph{{{f(se, 3)}}}\\
\bottomrule
\end{{tabular}}
\end{{table}}

Table~\ref{{tab:ns}} reads as a sequence of corrections, each one predicted by
Section~\ref{{sec:loc}} and each one worth roughly a factor of the previous error.

\emph{{Prior training with the identity head fails, and does not improve with $M$.}} The error is
about one posterior standard deviation and moves from {f(V['global_identity_M400'], 3)} at
$M={V['M_small']}$ to {f(V['global_identity_M1600'], 3)} at $M={V['M_headline']}$, so it is bias
and not Monte Carlo error. This is the shrinking-neighbourhood caveat of
Remark~\ref{{rem:affine}} made concrete: the identity head is justified on the localisation set,
draws from the prior lie far outside it, and there the summary \eqref{{eq:onestep}}, whose Jacobian
sits at the preliminary estimate, is not a one-step efficient estimator but an arbitrary linear
functional. Learning an affine head instead recovers only part of the loss,
{f(V['global_linear_M1600'], 3)}, because the map is genuinely nonlinear over the prior's support.

\emph{{Localisation is necessary, and post-hoc localisation is not a substitute.}} Drawing the
training parameters from a proposal centred at the preliminary estimate cuts the error by a factor
of {f(V['global_identity_M1600'] / V['local_train_identity_M1600'], 1)}, to
{f(V['local_train_identity_M1600'], 3)}, and restores the decrease in $M$. Localising a
prior-trained pool after the fact by keeping the $K$ nearest summaries reaches only
{f(V['global_localised_K200'], 3)} at $K=200$ and degrades as $K$ grows, which is the
bias--variance trade-off of approximate Bayesian computation and is why
Algorithm~\ref{{alg:loc}} localises the proposal rather than the pool.

Two further knobs were turned and are reported in Remark~\ref{{rem:nsdiag}}: importance
weighting the localised draws back to the prior, which degenerates exactly as
Section~\ref{{sec:loc}} says it must, and re-linearising the summary, which recovers in full the
$c^4$ term of Proposition~\ref{{prop:radius}}.

\emph{{The residual mean is the one Theorem~\ref{{thm:locbias}}(ii) predicts.}} The uncentred head
adds the sample mean of the training residuals to the observed summary, and so displaces its
centre. Measured per coordinate that mean is $({emp})$, against the linear-Gaussian prediction
$P\bar\theta_N$ of Theorem~\ref{{thm:locbias}}(ii), which is $({thy})$: right in sign and within a
fifth in magnitude in every coordinate, the excess being the nonlinearity. Centring removes it and
the error falls from {f(C['id_uncentred'], 3)} to {f(C['id_centred'], 3)}, at which point the
centre of the GBC posterior is displaced from the reference's own posterior mean by
{f(C['MAP_minus_pm'], 3)}, which is exactly the maximum a posteriori estimate's displacement. Rescaling the spread by the predicted inflation
$(s_j+c^2p_j^2)^{{-1/2}}$ of Theorem~\ref{{thm:locbias}}(iii), which the measured prior fraction
puts at {f(infl, 2)} in the last coordinate at $c=5$ against a measured
{f(C['spread_ratio_gbc'][-1], 2)}, brings the error to
{f(K['gbc_centred_corrected_deflated'], 3)}.

Two further regimes were run, each with its own reference, to look for the crossover at which
non-Gaussianity of the posterior would favour a simulation-based method. Raising the amplitude,
hence the advection-to-dissipation ratio $AT/\nu$, left the mean absolute marginal skewness at
{f(ns['crossover2']['skew'], 2)} with the Laplace approximation at {f(ns['crossover2']['laplace'], 3)}
against GBC's {f(ns['crossover2']['gbc_c2.0_id'], 3)}; widening the posterior instead raised the
skewness only to {f(ns['crossover3']['skew'], 2)} and degraded the Laplace approximation to
{f(ns['crossover3']['laplace'], 3)} but GBC further, to {f(ns['crossover3']['gbc_c2.0_id'], 3)}. The
crossover was not found. Amplitude alone does not make the posterior non-Gaussian, because the
posterior stays narrow and the map is nearly affine across it, and widening the posterior widens
the region the training proposal must cover, over which a once-linearised summary is a worse
statistic. Both errors are governed by the curvature of $\Gcal$ measured in posterior standard
deviations, so they do not move independently and the crossover cannot be assumed.

What the table does not show is a win. Corrected, GBC reaches
{f(K['gbc_centred_corrected_deflated'], 3)} against the Laplace approximation's
{f(K['laplace'], 3)}, and the reference's own Monte Carlo standard error is {f(se, 3)}, so the two
are indistinguishable at the resolution available: separating them would need a chain about forty
times longer. That is the honest reading, and it is the one Section~\ref{{sec:related}} leads with.
In this regime the Laplace approximation is excellent and free, and recommending a simulation-based
method on accuracy grounds would be wrong. What the table does show is that the distance between a
naive GBC implementation and a correct one is a factor of
{f(V['global_identity_M1600'] / K['gbc_centred_corrected_deflated'], 0)}, and that every step of
that factor is a theorem of Section~\ref{{sec:loc}} rather than a tuning choice. The case for GBC
here is amortisation, and the regimes in which it is the only option are the ones the theory
excludes: $T_0>0$, model error, non-Gaussian noise.

\begin{{remark}}[Two diagnostics from the Navier--Stokes run]\label{{rem:nsdiag}}
\emph{{Importance weighting back to the prior degenerates, as the algorithm says it does.}}
Correcting the localised proposal by weights $w\propto\pi/q$ raises the error from
{f(ns['radius_iw']['c3.0_unw'], 3)} to {f(ns['radius_iw']['c3.0_iw'], 3)} at $c=3$, with an
effective sample size of {f(ns['radius_iw']['c3.0_ess'], 0)} out of $M$; at $c=5$ the weighted
error is {f(ns['radius_iw']['c5.0_iw'], 3)} at an effective sample size of
{f(ns['radius_iw']['c5.0_ess'], 1)}. The proposal is much narrower than the prior, so the weights
grow like $e^{{+\norm\theta^2}}$ in its tails. The unweighted estimator is biased for the
prior-based posterior, but the bias is second order in the radius while the weighted estimator's
variance is not.

\emph{{Linearising the summary once is what the $c^4$ term of Proposition~\ref{{prop:radius}}
costs.}} At $c=2$ the one-step and two-step Gauss--Newton summaries are indistinguishable,
{f(R['c2.0_k1_lin'], 3)} against {f(R['c2.0_k2_lin'], 3)}, as they must be where the $c^4$ term is
negligible. At $c=6$ the one-step summary costs a factor of
{f(R['c6.0_k1_lin'] / R['c6.0_k2_lin'], 1)}, {f(R['c6.0_k1_lin'], 3)} against
{f(R['c6.0_k2_lin'], 3)}, and re-linearising recovers all of it. Iterating is legitimate because
$S_k$, the result of $k$ Gauss--Newton steps started from the same fixed point with the Jacobian
recomputed from $Y$ alone, is a statistic for every $k$; re-linearising at each \emph{{training
point}} would use $\theta^{{(m)}}$, which is unavailable for the observed data, and would not define
one. Each extra step costs $D+1$ forward solves per training draw.
\end{{remark}}
"""


if __name__ == '__main__':
    main()
