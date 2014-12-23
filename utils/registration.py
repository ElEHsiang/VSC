import numpy as np
from scipy.ndimage import affine_transform, geometric_transform, shift, rotate, zoom


def registration(source, destation):
    S = np.copy(source)
    D = np.copy(destation)

    x_trans = 0
    y_trans = 0
    rot =  0
    scale = 1
    x_trans_all = 0
    y_trans_all = 0
    rot_all = 0

    for i in range(5):
        x_trans, y_trans = optimize_trans(S, D, x_start=-5, x_end=5, y_start=-5, y_end=5)
        x_trans_all += x_trans
        y_trans_all += y_trans
        shift(S, (x_trans, y_trans), output=S)

        rot = optimize_rot(S, D, -45, 45)
        rot_all += rot
        rotate(S, rot, output=S)
    S[S < 0.01] = 0
    return S

def optimize_trans(source, destation, x_start, x_end, y_start, y_end):
    S = source
    D = destation
    x_trans = 0
    y_trans = 0

    diff_energy = 9999999
    for x in range(x_start, x_end + 1):
        for y in range(y_start, y_end + 1):
            diff = shift(S, (x, y)) - D
            e = np.sum(np.abs(diff))
            if e < diff_energy:
                diff_energy = e
                x_trans = x
                y_trans = y
    return (x_trans, y_trans)

def optimize_rot(source, destation, rot_start, rot_end):
    S = source
    D = destation
    rot = 0
    
    diff_energy = 9999999
    for r in range(rot_start, rot_end + 1):
        diff = rotate(S, r, reshape=False) - D
        e = np.sum(np.abs(diff))
        if e < diff_energy:
            diff_energy = e
            rot = r
    return rot

def optimize_scale(source, destation, scale_start, scale_end):
    """find best scale for zooming the source with same ratio each axis"""
    S = source
    D = destation
    x, y = S.shape
    scale = 1
    
    diff_energy = 9999999
    for s in range(scale_start, scale_end + 1):
        if s >= 1:
            zoomed = zoom(S, s)
            x_offset, y_offset = (zoomed.shape - S.shpae)/2
            zoomed = zoomed[np.ix_([x_offset, x_offset + S.shape[0]], [y_offset, y_offset + S.shape[1]])]
            diff = S - zoomed
            e = np.sum(np.abs(diff))
            if e < diff_energy:
                diff_energy = e
                scale = s

        if s < 1:
            zoomed = zoom(S, s)
            x_offset, y_offset = (S.shpae - zoomed.shape)/2
            S_temp = S[np.ix_([x_offset, x_offset + zoomed.shpae[0]], [y_offset, y_offset + zoomed.shpae[1]])]
            diff = S_temp - zoomed
            e = np.sum(np.abs(diff))
            if e < diff_energy:
                diff_energy = e
                scale = s
    return scale

def transform(source, x_trans=0, y_trans=0, rot=0, scale=1):
    S = np.copy(source)

    shift(S, (x_trans, y_trans), output=S)
    S[S<0.01] = 0
    rotate(S, rot, output=S, reshape=false)
    S[S<0.01] = 0
    result = zoom(S, scale)

    return result
    
