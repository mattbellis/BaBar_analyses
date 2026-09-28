"""
Diagnostics for BtuTupleMaker daughter-index bookkeeping (BNV Lambda0 LambdaC ntuples).

How the indices are supposed to work
------------------------------------
For a composite block X, ``Xd{i}Lund`` gives the Lund ID of the i-th daughter and
``Xd{i}Idx`` gives its position *in the block for that particle type*
(pi+-  -> pi block, K_S0 -> K_S block, Lambda0 -> Lambda0 block, ...).
For blocks listed in ``ntpBlockToTrk`` (pi K mu e p), ``{block}TrkIdx`` then points
into TRK, which is where the PID selector bitmaps live.

    K_Sd1Idx --> pi block --> piTrkIdx --> TRK (piSelectorsMap, pSelectorsMap, ...)

BtuTupleMaker fills blocks in the order they are declared in the tcl. When it fills
a block and meets a daughter that is not already in the daughter's list, it *appends*
the daughter and records the new index. If the daughter's block has already been
written, that appended candidate never reaches the ntuple, and you get
``Xd{i}Idx >= n{daughter block}``. That's what happens here with the ``pi`` block
declared before ``K_S``.

Usage in a notebook
-------------------
    import awkward as ak
    import bnv_index_diagnostics as bid

    data = ak.from_parquet(infilename)
    uds  = data[data['spmode'] == '998']

    bid.index_check(uds)                   # table: every parent/daughter link, % out of range
    bid.print_event(uds[0])                # decay tree for one event, flags broken links
    bid.print_trk_matches(uds[0], 'K_S')   # which TRK pairs really make each K_S
    m = bid.match_to_trk(uds, 'K_S')       # same thing, vectorised over all events
    bid.plot_match(m)
    bid.plot_index_overflow(uds, 'K_S')
"""

import numpy as np
import awkward as ak
import pandas as pd
import matplotlib.pyplot as plt

M_PI, M_K, M_P = 0.13957, 0.493677, 0.938272

# abs(Lund) -> ntuple block name used in bnv_analysis_lam0lamc.tcl
LUND_TO_BLOCK = {
    211: "pi", 321: "K", 2212: "p", 11: "e", 13: "mu", 22: "gamma",
    111: "pi0", 310: "K_S", 3122: "Lambda0", 4122: "LambdaC", 521: "B", 511: "B",
}

# Order used when walking decay trees / looping over composites
COMPOSITE_BLOCKS = ["B", "LambdaC", "Lambda0", "K_S", "pi0"]


# ----------------------------------------------------------------------------
# small helpers
# ----------------------------------------------------------------------------
def _fields(d):
    return set(d.fields)


def _n_slots(fields, block, max_slots=10):
    """Number of daughter slots (d1, d2, ...) stored for a block."""
    n = 0
    while f"{block}d{n+1}Idx" in fields and n < max_slots:
        n += 1
    return n


def _block_len(d, block):
    """Length of a block (per event). Uses the stored n{block} counter."""
    return d[f"n{block}"]


def cartesian(d, block):
    """px, py, pz from BtuTupleMaker's p3 / costh / phi (lab frame)."""
    p, ct, phi = d[f"{block}p3"], d[f"{block}costh"], d[f"{block}phi"]
    st = np.sqrt(np.maximum(1.0 - ct * ct, 0.0))  # ufunc, works on jagged arrays
    return p * st * np.cos(phi), p * st * np.sin(phi), p * ct


def trk_charge(lund):
    """Charge from a TRK/charged-block Lund ID (leptons have opposite sign convention)."""
    lund = np.asarray(lund)
    s = np.sign(lund)
    lep = np.isin(np.abs(lund), [11, 13])
    return np.where(lep, -s, s)


# ----------------------------------------------------------------------------
# 1. Global check: how often does each daughter index fall off the end of its block?
# ----------------------------------------------------------------------------
def index_check(data, parents=None):
    """
    For every composite block, daughter slot and daughter type, count how many
    daughter indices are >= the number of entries in the daughter's block.

    Returns a pandas DataFrame. Any row with n_out_of_range > 0 is a broken link.
    """
    fields = _fields(data)
    parents = parents or [b for b in COMPOSITE_BLOCKS if f"n{b}" in fields]
    rows = []
    for parent in parents:
        for i in range(1, _n_slots(fields, parent) + 1):
            lund = data[f"{parent}d{i}Lund"]
            idx = data[f"{parent}d{i}Idx"]
            for code in np.unique(np.abs(ak.to_numpy(ak.flatten(lund)))):
                if code == 0:
                    continue
                target = LUND_TO_BLOCK.get(int(code))
                row = dict(parent=parent, slot=f"d{i}", dau_lund=int(code), target_block=target)
                sel = np.abs(lund) == code
                row["n_daughters"] = int(ak.sum(sel))
                if target is None or f"n{target}" not in fields:
                    row.update(n_out_of_range=np.nan, frac_out_of_range=np.nan,
                               n_events_affected=np.nan, note="no block for this Lund")
                    rows.append(row)
                    continue
                ntarget, _ = ak.broadcast_arrays(_block_len(data, target), idx)
                bad = sel & (idx >= ntarget)
                nbad = int(ak.sum(bad))
                row.update(
                    n_out_of_range=nbad,
                    frac_out_of_range=nbad / max(row["n_daughters"], 1),
                    n_events_affected=int(ak.sum(ak.any(bad, axis=1))),
                    note="BROKEN" if nbad else "ok",
                )
                rows.append(row)
    df = pd.DataFrame(rows)
    with pd.option_context("display.float_format", "{:.3f}".format):
        return df


# ----------------------------------------------------------------------------
# 2. One event: walk the decay tree and flag every broken link
# ----------------------------------------------------------------------------
def _cand_summary(d, block, j):
    f = _fields(d)
    parts = []
    for key, fmt in (("Mass", "m={:.4f}"), ("p3", "p={:.3f}"), ("costh", "cth={:+.3f}"),
                     ("phi", "phi={:+.3f}"), ("MCIdx", "MCIdx={}")):
        name = f"{block}{key}"
        if name in f:
            parts.append(fmt.format(d[name][j]))
    if f"{block}TrkIdx" in f:
        parts.append(f"TrkIdx={d[f'{block}TrkIdx'][j]}")
    return "  ".join(parts)


def print_event(d, top="B", show_trk=True, max_top=None):
    """
    Print the decay tree(s) of one event (one record of the awkward array),
    following d{i}Idx links and checking each one against the daughter block length.
    """
    f = _fields(d)
    counts = {b: int(d[f"n{b}"]) for b in LUND_TO_BLOCK.values() if f"n{b}" in f}
    counts.update({"TRK": int(d["nTRK"])} if "nTRK" in f else {})
    print("block sizes:", "  ".join(f"{k}={v}" for k, v in counts.items()))
    ntop = counts.get(top, 0)
    for j in range(ntop if max_top is None else min(ntop, max_top)):
        _walk(d, top, j, depth=0, f=f, counts=counts, show_trk=show_trk)
        print()


def _walk(d, block, j, depth, f, counts, show_trk):
    pad = "    " * depth
    lund = d[f"{block}Lund"][j] if f"{block}Lund" in f else ""
    print(f"{pad}{block}[{j}] lund={lund}  {_cand_summary(d, block, j)}")

    # link to TRK for charged final-state blocks
    if show_trk and f"{block}TrkIdx" in f:
        t = int(d[f"{block}TrkIdx"][j])
        ok = 0 <= t < counts.get("TRK", 0)
        msg = f"TRK[{t}] " + (_cand_summary(d, "TRK", t) if ok else "<-- OUT OF RANGE")
        print(f"{pad}    -> {msg}")

    for i in range(1, _n_slots(f, block) + 1):
        dl = int(d[f"{block}d{i}Lund"][j])
        if dl == 0:
            continue
        di = int(d[f"{block}d{i}Idx"][j])
        target = LUND_TO_BLOCK.get(abs(dl))
        n = counts.get(target, 0)
        if target is None or di < 0 or di >= n:
            print(f"{pad}    d{i}: lund={dl:6d} -> {target}[{di}]   "
                  f"<-- OUT OF RANGE (n{target}={n})")
        else:
            _walk(d, target, di, depth + 1, f, counts, show_trk)


# ----------------------------------------------------------------------------
# 3. Recover the real tracks: match a 2-body composite to pairs of TRK by momentum
# ----------------------------------------------------------------------------
_HYPOTHESES = {
    "K_S": [(M_PI, M_PI)],
    "Lambda0": [(M_P, M_PI), (M_PI, M_P)],  # try both assignments
}


def print_trk_matches(d, parent="K_S", ntop=5):
    """For each candidate in `parent`, list the TRK pairs whose momentum sum is closest."""
    px, py, pz = (ak.to_numpy(a) for a in cartesian(d, parent))
    tx, ty, tz = (ak.to_numpy(a) for a in cartesian(d, "TRK"))
    tp = ak.to_numpy(d["TRKp3"])
    q = trk_charge(ak.to_numpy(d["TRKLund"]))
    hyps = _HYPOTHESES.get(parent, [(M_PI, M_PI)])
    ntrk = len(tx)
    for k in range(len(px)):
        rows = []
        for a in range(ntrk):
            for b in range(a + 1, ntrk):
                if q[a] * q[b] >= 0:
                    continue  # need opposite charges
                dp = np.sqrt((tx[a] + tx[b] - px[k])**2 + (ty[a] + ty[b] - py[k])**2
                             + (tz[a] + tz[b] - pz[k])**2)
                psum2 = (tx[a] + tx[b])**2 + (ty[a] + ty[b])**2 + (tz[a] + tz[b])**2
                masses = []
                for m1, m2 in hyps:
                    e = np.sqrt(tp[a]**2 + m1**2) + np.sqrt(tp[b]**2 + m2**2)
                    masses.append(np.sqrt(max(e * e - psum2, 0)))
                rows.append((a, b, dp, *masses))
        cols = ["trk_a", "trk_b", "dp"] + [f"m({m1:.3f},{m2:.3f})" for m1, m2 in hyps]
        df = pd.DataFrame(rows, columns=cols).sort_values("dp").head(ntop)
        stored = [int(d[f"{parent}d{i}Idx"][k]) for i in (1, 2)]
        print(f"{parent}[{k}]  p={d[f'{parent}p3'][k]:.4f}  stored d1Idx,d2Idx={stored}")
        print(df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        print()


def match_to_trk(data, parent="K_S"):
    """
    Vectorised version over many events. For each `parent` candidate, find the
    opposite-charge TRK pair whose summed 3-momentum is closest to the candidate's.

    Returns an awkward Array (one entry per event, one sub-entry per candidate) with
    fields: trk_a, trk_b, dp_best, dp_second, mass (pi pi or best p pi hypothesis),
    stored_d1Idx, stored_d2Idx, n_dau_block.
    Use ak.flatten(result.dp_best) etc. for histograms.
    """
    tx, ty, tz = cartesian(data, "TRK")
    q = ak.Array(trk_charge(ak.to_numpy(ak.flatten(data["TRKLund"]))))
    q = ak.unflatten(q, ak.num(data["TRKLund"]))
    trk = ak.zip({"x": tx, "y": ty, "z": tz, "p": data["TRKp3"], "q": q,
                  "i": ak.local_index(data["TRKp3"])})
    pairs = ak.combinations(trk, 2, fields=["a", "b"])
    pairs = pairs[pairs.a.q * pairs.b.q < 0]

    px, py, pz = cartesian(data, parent)
    cand = ak.zip({"x": px, "y": py, "z": pz})

    # (event, candidate, pair)
    c, pr = ak.unzip(ak.cartesian([cand, pairs], nested=True))
    dp = np.sqrt((pr.a.x + pr.b.x - c.x)**2 + (pr.a.y + pr.b.y - c.y)**2
                 + (pr.a.z + pr.b.z - c.z)**2)

    order = ak.argsort(dp, axis=-1)
    dp_sorted = dp[order]
    best = pr[order][:, :, :1]
    dp_best = ak.firsts(dp_sorted, axis=-1)
    dp_second = ak.firsts(dp_sorted[:, :, 1:], axis=-1)
    best = ak.firsts(best, axis=-1)

    psum2 = ((best.a.x + best.b.x)**2 + (best.a.y + best.b.y)**2 + (best.a.z + best.b.z)**2)
    hyps = _HYPOTHESES.get(parent, [(M_PI, M_PI)])
    masses = []
    for m1, m2 in hyps:
        e = np.sqrt(best.a.p**2 + m1**2) + np.sqrt(best.b.p**2 + m2**2)
        masses.append(np.sqrt(np.maximum(e * e - psum2, 0)))
    mass = masses[0]
    if len(masses) == 2:  # Lambda0: take the assignment closer to PDG mass
        mass = ak.where(abs(masses[0] - 1.11568) < abs(masses[1] - 1.11568), masses[0], masses[1])

    dau_block = LUND_TO_BLOCK.get(abs(int(ak.flatten(data[f"{parent}d1Lund"])[0])), "pi")
    nb, _ = ak.broadcast_arrays(data[f"n{dau_block}"], data[f"{parent}d1Idx"])
    return ak.zip({
        "trk_a": best.a.i, "trk_b": best.b.i,
        "dp_best": dp_best, "dp_second": dp_second, "mass": mass,
        "stored_d1Idx": data[f"{parent}d1Idx"], "stored_d2Idx": data[f"{parent}d2Idx"],
        "n_dau_block": nb,
    })


# ----------------------------------------------------------------------------
# 4. Plots
# ----------------------------------------------------------------------------
def plot_match(m, parent="K_S", bins=60):
    """Histograms from match_to_trk: how unambiguous is the TRK match?"""
    dpb = ak.to_numpy(ak.drop_none(ak.flatten(m.dp_best)))
    dps = ak.to_numpy(ak.drop_none(ak.flatten(m.dp_second)))
    mass = ak.to_numpy(ak.drop_none(ak.flatten(m.mass)))
    broken = ak.to_numpy(ak.flatten((m.stored_d1Idx >= m.n_dau_block)
                                    | (m.stored_d2Idx >= m.n_dau_block)))

    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    lb = np.linspace(-4, 1, bins)
    ax[0].hist(np.log10(dpb + 1e-6), bins=lb, histtype="step", lw=1.5, label="best pair")
    ax[0].hist(np.log10(dps + 1e-6), bins=lb, histtype="step", lw=1.5, label="2nd best pair")
    ax[0].set_xlabel(r"$\log_{10}|\Delta\vec p|$  [GeV]")
    ax[0].set_ylabel("candidates")
    ax[0].legend()
    ax[0].set_title(f"{parent} vs TRK pairs")

    ax[1].hist(mass, bins=bins, histtype="step", lw=1.5)
    ax[1].set_xlabel("best-pair invariant mass [GeV]")
    ax[1].set_title("mass of matched TRK pair")

    ax[2].bar(["index OK", "index out of range"], [np.sum(~broken), np.sum(broken)],
              color=["#4C72B0", "#C44E52"])
    ax[2].set_title(f"stored {parent} daughter indices")
    fig.tight_layout()
    return fig


def plot_index_overflow(data, parent="K_S", slot=1):
    """Stored daughter index vs size of the daughter block, one point per candidate."""
    lund = data[f"{parent}d{slot}Lund"]
    idx = data[f"{parent}d{slot}Idx"]
    target = LUND_TO_BLOCK[abs(int(ak.flatten(lund)[0]))]
    n, _ = ak.broadcast_arrays(data[f"n{target}"], idx)
    x, y = ak.to_numpy(ak.flatten(n)), ak.to_numpy(ak.flatten(idx))

    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    hi = max(x.max(), y.max()) + 1
    h = ax[0].hist2d(x, y, bins=[np.arange(hi + 1) - 0.5] * 2, cmin=1, cmap="viridis")
    ax[0].plot([0, hi], [0, hi], "r--", lw=1)
    ax[0].set_xlabel(f"n{target}")
    ax[0].set_ylabel(f"{parent}d{slot}Idx")
    ax[0].set_title("above the red line = points past end of block")
    fig.colorbar(h[3], ax=ax[0])

    ax[1].hist(y - x, bins=np.arange((y - x).min(), (y - x).max() + 2) - 0.5)
    ax[1].axvline(-0.5, color="r", ls="--")
    ax[1].set_xlabel(f"{parent}d{slot}Idx - n{target}   (>= 0 is broken)")
    fig.tight_layout()
    return fig
