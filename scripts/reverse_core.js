// Bayesian reverse birth-death reconstruction, a JS port of eukaryotes/reverse.py.
// Given observed copy numbers m (per family), features x, loss/duplication/origination
// weights and a prior over ancestral copy numbers, returns P(ancestor had the family).

const LOGFACT = (() => { const t = [0]; for (let i = 1; i < 64; i++) t.push(t[i - 1] + Math.log(i)); return t; })();
const lbinom = (n, k) => LOGFACT[n] - LOGFACT[k] - LOGFACT[n - k];
const LOG_HALF = Math.log(0.5);

function logsumexp(arr, len) {
  let mx = -Infinity;
  for (let i = 0; i < len; i++) if (arr[i] > mx) mx = arr[i];
  if (mx === -Infinity) return -Infinity;
  let s = 0;
  for (let i = 0; i < len; i++) s += Math.exp(arr[i] - mx);
  return mx + Math.log(s);
}

function alphaBeta(lam, mu) {
  const r = lam - mu;
  let a, b;
  if (Math.abs(r) < 1e-6) { a = b = lam / (1 + lam); }
  else { const em1 = Math.expm1(r), den = lam * (em1 + 1) - mu; a = mu * em1 / den; b = lam * em1 / den; }
  const eps = 1e-12;
  return [Math.min(Math.max(a, eps), 1 - eps), Math.min(Math.max(b, eps), 1 - eps)];
}

// log P(m | n) for n >= 1
function logTrans(n, m, la, lb, l1a, l1b, buf) {
  if (m === 0) return n * la;
  const top = Math.min(n, m);
  for (let j = 1; j <= top; j++) {
    buf[j - 1] = lbinom(n, j) + j * l1a + (n - j) * la + lbinom(m - 1, j - 1) + j * l1b + (m - j) * lb;
  }
  return logsumexp(buf, top);
}

// Per-family linear predictors (without offsets) for a weight set.
function linear(x, F, P, w) {
  const out = new Float64Array(F);
  for (let f = 0; f < F; f++) { let s = 0; for (let p = 0; p < P; p++) s += x[f * P + p] * w[p]; out[f] = s; }
  return out;
}

function makePrior(refCounts, F, K) {
  // refCounts: array of Int arrays (length F), counts capped at K
  const S = refCounts.length, logPrior = new Float64Array(F * (K + 1));
  for (let f = 0; f < F; f++) {
    let present = 0, sum = 0;
    for (let s = 0; s < S; s++) { const v = refCounts[s][f]; if (v > 0) { present++; sum += v; } }
    const pPresent = (present + 0.5) / (S + 1);
    const mean = present > 0 ? sum / present : 1;
    const q = 1 / Math.max(mean, 1);
    let z = 0; const g = [];
    for (let k = 1; k <= K; k++) { const v = q * Math.pow(1 - q, k - 1); g.push(v); z += v; }
    logPrior[f * (K + 1)] = Math.log(1 - pPresent);
    for (let k = 1; k <= K; k++) logPrior[f * (K + 1) + k] = Math.log(pPresent * g[k - 1] / z);
  }
  return logPrior;
}

// Joint log table: log P(m_f | n) + log prior(n); returns marginal and optionally posteriors.
function evaluate(m, linLam, linMu, linNu, logPrior, F, K, offsets, wantPosterior) {
  const [aLam, aMu, aNu] = offsets;
  const row = new Float64Array(K + 1), buf = new Float64Array(K);
  let total = 0;
  const pPresent = wantPosterior ? new Float64Array(F) : null;
  for (let f = 0; f < F; f++) {
    const mf = m[f];
    const lam = Math.exp(aLam + linLam[f]), mu = Math.exp(aMu + linMu[f]), nu = Math.exp(aNu + linNu[f]);
    const [a, b] = alphaBeta(lam, mu);
    const la = Math.log(a), lb = Math.log(b), l1a = Math.log1p(-a), l1b = Math.log1p(-b);
    const base = f * (K + 1);
    row[0] = (mf > 0 ? Math.log(-Math.expm1(-nu)) + mf * LOG_HALF : -nu) + logPrior[base];
    for (let n = 1; n <= K; n++) row[n] = logTrans(n, mf, la, lb, l1a, l1b, buf) + logPrior[base + n];
    const lse = logsumexp(row, K + 1);
    total += lse;
    if (pPresent) pPresent[f] = 1 - Math.exp(row[0] - lse);
  }
  return { logMarginal: total, pPresent };
}

// Nelder-Mead over the three offsets, maximising the marginal likelihood.
async function fitOffsets(fn, start, onProgress, iters = 120) {
  const n = 3;
  let simplex = [start.slice()];
  for (let i = 0; i < n; i++) { const p = start.slice(); p[i] += 0.8; simplex.push(p); }
  let vals = simplex.map(fn);
  for (let it = 0; it < iters; it++) {
    const order = vals.map((v, i) => i).sort((i, j) => vals[i] - vals[j]);
    simplex = order.map((i) => simplex[i]); vals = order.map((i) => vals[i]);
    const c = [0, 0, 0];
    for (let i = 0; i < n; i++) for (let d = 0; d < n; d++) c[d] += simplex[i][d] / n;
    const worst = simplex[n];
    const at = (t) => c.map((cd, d) => cd + t * (worst[d] - cd));
    const xr = at(-1), fr = fn(xr);
    if (fr < vals[0]) { const xe = at(-2), fe = fn(xe); if (fe < fr) { simplex[n] = xe; vals[n] = fe; } else { simplex[n] = xr; vals[n] = fr; } }
    else if (fr < vals[n - 1]) { simplex[n] = xr; vals[n] = fr; }
    else {
      const xc = at(0.5), fc = fn(xc);
      if (fc < vals[n]) { simplex[n] = xc; vals[n] = fc; }
      else { for (let i = 1; i <= n; i++) { simplex[i] = simplex[i].map((v, d) => simplex[0][d] + 0.5 * (v - simplex[0][d])); vals[i] = fn(simplex[i]); } }
    }
    if (onProgress && it % 6 === 0) { onProgress(it / iters); await new Promise((r) => setTimeout(r, 0)); }
    if (Math.abs(vals[n] - vals[0]) < 1e-3) break;
  }
  return simplex[0];
}

function auroc(scores, labels) {
  const idx = scores.map((s, i) => i).sort((i, j) => scores[i] - scores[j]);
  let rank = 0, sumPos = 0, nPos = 0, nNeg = 0, i = 0;
  while (i < idx.length) {
    let j = i; while (j + 1 < idx.length && scores[idx[j + 1]] === scores[idx[i]]) j++;
    const r = (i + j) / 2 + 1;
    for (let k = i; k <= j; k++) { if (labels[idx[k]]) { sumPos += r; nPos++; } else nNeg++; }
    i = j + 1;
  }
  return nPos && nNeg ? (sumPos - nPos * (nPos + 1) / 2) / (nPos * nNeg) : NaN;
}

if (typeof module !== "undefined") module.exports = { makePrior, linear, evaluate, fitOffsets, auroc, alphaBeta, logTrans };
