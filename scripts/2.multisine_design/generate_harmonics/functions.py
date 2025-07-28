"""
This functions are translate from the MATLAB script developed by Fabio La Mantia
"""
import numpy as np
from typing import Callable

def multi_ac_interferelinear(f, dist):
    """
    f : array‐like of shape (N,) or (N,1)
    dist : scalar
    returns y : array of shape (M,3)
    """
    f = np.asarray(f).reshape(-1)
    N = f.size

    # Build Mf matrix
    Mf = np.zeros((N, N))
    for kk in range(N):
        for jj in range(N):
            if f[jj] >= f[kk]:
                Mf[jj, kk] = f[kk] + f[jj]
            else:
                Mf[jj, kk] = f[kk] - f[jj]

    y = []
    # Loop over k = 0..N-2 (MATLAB 1..N-1)
    for k in range(N - 1):
        # remove k-th element
        fm = np.delete(f, k)
        VA = f[k] - fm

        # remove k-th row & col from Mf
        Mm = np.delete(np.delete(Mf, k, axis=0), k, axis=1)
        MA = f[k] - Mm

        # loops over kk, jj = 0..N-2
        for kk in range(N - 1):
            if abs(VA[kk]) <= dist:
                y.append([f[k], fm[kk], 0])
            for jj in range(N - 1):
                if abs(MA[jj, kk]) <= dist:
                    y.append([f[k], fm[kk], fm[jj]])

    return np.array(y)


def multi_ac_design(
    f: np.ndarray,
    nn: int,
    max_iter: int,
    interfere: Callable[[np.ndarray, float, float], np.ndarray],
    dist: float,
    minfreq: float
) -> np.ndarray:
    """
    f         : 1D array of sorted frequencies
    nn        : step‐width for local search
    max_iter  : maximum outer iterations
    interfere : function(f, dist, minfreq) → array of interfering triplets
    dist      : interference threshold
    minfreq   : minimum allowed frequency
    returns   : final array of frequencies
    """
    f = np.asarray(f).reshape(-1)
    ok = False
    it = 0

    while not ok and it <= max_iter:
        N = f.size
        Test  = np.zeros(N-1, dtype=int)
        Testp = np.zeros(nn,  dtype=int)
        Testm = np.zeros(nn,  dtype=int)

        I = interfere(f, dist)
        if I.size == 0:
            ok = True
            break

        it += 1
        # Count how often each f[N-k] appears in any row of I
        for k in range(1, N):
            for row in I:
                if f[N-k] in row:
                    Test[k-1] += 1

        Ind  = int(np.argmax(Test))    # 0-based index of worst offender
        Testz = I.shape[0]             # baseline # of interferences
        ok1   = False

        while not ok1:
            Ind1 = int(np.argmax(Test))

            # Evaluate +k and –k shifts
            for k in range(1, nn+1):
                # plus shift
                fp = f.copy()
                fp[N-1-Ind1] += k
                Ip = interfere(fp, dist)
                Testp[k-1] = Ip.shape[0]

                # minus shift
                fm = f.copy()
                fm[N-1-Ind1] -= k
                if fm[N-1-Ind1] < dist + 1:
                    Testm[k-1] = Testz
                else:
                    Im = interfere(fm, dist)
                    Testm[k-1] = Im.shape[0]

            # pick the shift with minimum new interference
            arr  = np.concatenate((Testm, Testp))
            Ind2 = int(np.argmin(arr))
            Test[Ind1] = 0

            # Decide action
            if (Testz <= Testp).all() and (Testz <= Testm).all() and (Test == 0).all():
                # remove frequency
                print(f"frequency {f[N-1-Ind]:.3f} Hz removed")
                f = np.delete(f, N-1-Ind)
                nn += 1
                ok1 = True

            elif (np.any(Testz > Testp) or np.any(Testz > Testm)) and Ind2 >= nn:
                # positive shift
                kchg = Ind2 - nn + 1
                f[N-1-Ind1] += kchg
                ok1 = True

            elif (np.any(Testz > Testp) or np.any(Testz > Testm)) and Ind2 < nn:
                # negative shift
                kchg = Ind2 + 1
                f[N-1-Ind1] -= kchg
                ok1 = True

        f = np.sort(f)
        print(f"remaining interferences: {Testz}")

    return f