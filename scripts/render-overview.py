#!/usr/bin/env python3
"""Render reproducible scientific illustrations, not RYBA interface screenshots.

Usage: python scripts/render-overview.py --ir TS1.out --goat SP_171.out
       --ensemble SP_171.finalensemble.xyz
Requires numpy, scipy, matplotlib. Uploaded ORCA files stay local.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Polygon
from scipy.signal import find_peaks

BG = '#121c22'
PANEL = '#19262d'
LINE = '#34444b'
TEXT = '#eef1ed'
MUTED = '#a7b9bd'
TEAL = '#78c5b8'
GOLD = '#e3bc7c'
ROOT = Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12,
                     'text.color': TEXT, 'axes.labelcolor': MUTED,
                     'xtick.color': MUTED, 'ytick.color': MUTED,
                     'axes.edgecolor': LINE, 'savefig.facecolor': BG})


def canvas(kicker, title, subtitle):
    fig = plt.figure(figsize=(16, 10), dpi=150, facecolor=BG)
    fig.text(.045, .942, kicker, color=TEAL, size=11, weight='bold')
    fig.text(.045, .878, title, size=29, weight='bold')
    fig.text(.045, .831, subtitle, color=MUTED, size=12)
    return fig


def panel(fig, x, y, w, h):
    fig.add_artist(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.008,rounding_size=0.012',
                                 transform=fig.transFigure, facecolor=PANEL,
                                 edgecolor=LINE, linewidth=.8, zorder=0))


def axes_style(ax):
    ax.set_facecolor(PANEL)
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(length=0, pad=10, labelsize=10)
    ax.grid(axis='y', color=LINE, linewidth=.65, alpha=.65)
    ax.set_axisbelow(True)


def parse_xyz(path):
    lines = path.read_text().splitlines()
    frames, energies, symbols = [], [], None
    i = 0
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
        n = int(lines[i])
        energies.append(float(lines[i + 1].split()[0]))
        rows = [r.split() for r in lines[i + 2:i + 2 + n]]
        current = [r[0] for r in rows]
        if symbols is None:
            symbols = current
        assert symbols == current, 'Inconsistent ensemble atom ordering'
        frames.append(np.array([[float(v) for v in r[1:4]] for r in rows]))
        i += n + 2
    return symbols, frames, np.array(energies)


def align(moving, reference, core):
    mc, rc = moving[core].mean(0), reference[core].mean(0)
    u, _, vt = np.linalg.svd((moving[core] - mc).T @ (reference[core] - rc))
    u[:, -1] *= np.linalg.det(u @ vt)
    return (moving - mc) @ (u @ vt) + rc


def bonds(symbols, xyz):
    # Connectivity inferred solely from distances; no invented bond orders.
    radii = {'C': .76, 'N': .71, 'O': .66, 'H': .31}
    return [(i, j) for i in range(len(symbols)) for j in range(i)
            if .4 < np.linalg.norm(xyz[i] - xyz[j]) < 1.22 * (radii[symbols[i]] + radii[symbols[j]])]


def molecule(ax, symbols, xyz, edges, ghost=False):
    colors = {'C': '#b7c3c8', 'N': '#6f9fe7', 'O': '#e77b78'}
    operations = [(float((xyz[i, 2] + xyz[j, 2]) / 2), 'bond', (i, j))
                  for i, j in edges if symbols[i] != 'H' and symbols[j] != 'H']
    operations += [(float(xyz[i, 2]), 'atom', i) for i, e in enumerate(symbols) if e != 'H']
    for _, kind, val in sorted(operations):
        if kind == 'bond':
            i, j = val
            x, y = xyz[[i, j], 0], xyz[[i, j], 1]
            ax.plot(x, y, lw=5.7 if not ghost else 5, color='#60747e' if not ghost else TEAL,
                    alpha=1 if not ghost else .26, solid_capstyle='round')
            if not ghost:
                ax.plot(x, y, lw=2.5, color='#b3c0c6', alpha=.6, solid_capstyle='round')
        else:
            c = xyz[val, :2]
            radius = .20 if symbols[val] == 'C' else .23
            ax.add_patch(Circle(c, radius, facecolor=colors[symbols[val]] if not ghost else TEAL,
                                edgecolor='#25363e' if not ghost else TEAL,
                                linewidth=.7, alpha=1 if not ghost else .26))
            if not ghost:
                ax.add_patch(Circle(c + [-.045, .055], radius * .47,
                                    facecolor='white', edgecolor='none', alpha=.22))


def render_goat(goat, ensemble):
    text = goat.read_text()
    block = text.rsplit('# Final ensemble info #', 1)[1].split('Conformers below')[0]
    rows = re.findall(r'^\s*(\d+)\s+([-\d.]+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s*$', block, re.M)
    data = np.array([[float(x) for x in r] for r in rows])
    symbols, frames, energies = parse_xyz(ensemble)
    assert len(data) == len(frames) == 39
    assert np.all(data[:, 0] == np.arange(len(frames)))
    assert np.allclose((energies - energies.min()) * 627.509474, data[:, 1], atol=.0006)
    assert abs(data[:, 3].sum() - 100) < .1
    assert re.search(r'Ensemble temperature\s+\.\.\. 298.15 K', text)
    core = np.arange(6)  # Six carbons of the shared aromatic ring, file atom order.
    ref, moving = frames[0], align(frames[1], frames[0], core)
    rmsd = float(np.sqrt(np.mean(np.sum((ref[core] - moving[core])**2, axis=1))))
    heavy = np.array([i for i, e in enumerate(symbols) if e != 'H'])
    # One orthographic camera for BOTH conformers; rotation only, no deformation.
    center = np.vstack([ref[heavy], moving[heavy]]).mean(0)
    _, _, vt = np.linalg.svd(np.vstack([ref[heavy], moving[heavy]]) - center, full_matrices=False)
    view = vt.T
    a, b = (ref - center) @ view, (moving - center) @ view
    if a[0, 0] < a[10, 0]:
        a[:, 0] *= -1
        b[:, 0] *= -1
    fig = canvas('RYBA / GOAT EXPLORER', 'One core. Many conformations.',
                 'Two conformers aligned on a shared aromatic ring, alongside the reported ensemble populations.')
    panel(fig, .045, .198, .565, .565)
    panel(fig, .642, .198, .313, .565)
    fig.text(.065, .727, 'GHOST OVERLAY', size=11, weight='bold', color=MUTED)
    fig.text(.065, .696, 'Conformer 0 + conformer 1', size=14)
    ax = fig.add_axes([.055, .271, .545, .392])
    ax.set_aspect('equal')
    ax.set_axis_off()
    both = np.vstack([a[heavy], b[heavy]])
    ax.set_xlim(both[:, 0].min() - .9, both[:, 0].max() + .9)
    ax.set_ylim(both[:, 1].min() - .8, both[:, 1].max() + .8)
    ax.add_patch(Polygon(a[core, :2], closed=True, fill=True, facecolor=GOLD, alpha=.055,
                         edgecolor=GOLD, linestyle='--', linewidth=1.2))
    edges = bonds(symbols, ref)
    assert set(edges) == set(bonds(symbols, frames[1])), 'Conformer connectivity differs'
    molecule(ax, symbols, b, edges, ghost=True)
    molecule(ax, symbols, a, edges)
    ring = a[core, :2]
    ring_center = ring.mean(0)
    ax.add_patch(Polygon((ring - ring_center) * 1.18 + ring_center, closed=True,
                         fill=False, edgecolor=GOLD, linestyle=(0, (3, 4)),
                         linewidth=1.2, alpha=.65))
    fig.text(.065, .232, f'Aligned core: C1–C6  ·  RMSD {rmsd:.3f} Å  ·  heavy atoms shown', size=10, color=MUTED)
    fig.text(.663, .727, 'POPULATION', size=11, weight='bold', color=MUTED)
    fig.text(.663, .696, '39 conformers / 298.15 K', size=14)
    ax = fig.add_axes([.688, .304, .222, .334])
    axes_style(ax)
    colors = [GOLD, TEAL] + ['#487872'] * (len(data) - 2)
    ax.bar(data[:, 0], data[:, 3], width=.72, color=colors)
    ax.set_ylim(0, 15)
    ax.set_xlim(-1, 39)
    ax.set_xticks([0, 10, 20, 30, 38])
    ax.set_yticks([0, 5, 10, 15])
    ax.set_ylabel('Population / %', labelpad=10, size=10)
    ax.set_xlabel('Conformer ID', labelpad=12, size=10)
    fig.text(.663, .232, 'Top 10: 68.67% of the ensemble', size=10, color=MUTED)
    fig.text(.065, .137, 'CONFORMER 0', color=GOLD, size=10, weight='bold')
    fig.text(.065, .101, '0.000 kcal/mol   ·   13.25%', size=17)
    fig.text(.383, .137, 'CONFORMER 1 / GHOST', color=TEAL, size=10, weight='bold')
    fig.text(.383, .101, '+0.111 kcal/mol   ·   10.98%', size=17)
    fig.text(.045, .039, 'SP_171.out + SP_171.finalensemble.xyz  /  Scientific data visualisation', size=9, color=MUTED)
    fig.text(.955, .039, 'Core alignment changes the view only.', size=9, color=MUTED, ha='right')
    dest = ROOT / 'assets/img/overview-goat-ensemble.png'
    fig.savefig(dest, dpi=150)
    plt.close(fig)
    return {'conformers': len(data), 'temperature_K': 298.15, 'selected_source_ids': [0, 1],
            'alignment_atom_ids_1_based': [1, 2, 3, 4, 5, 6], 'core_rmsd_A': rmsd,
            'relative_energies_kcal_mol': data[:2, 1].tolist(),
            'reported_populations_percent': data[:, 3].tolist(),
            'notes': 'Populations copied from final GOAT table, not recomputed; atom ordering and energies checked against XYZ. Proper-rotation rigid core fit; hydrogens hidden; no bond orders inferred.'}


def render_ir(path):
    text = path.read_text()
    block = text.rsplit('IR SPECTRUM', 1)[1].split('THERMOCHEMISTRY')[0]
    rows = re.findall(r'^\s*(\d+):\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+', block, re.M)
    data = np.array([[float(x) for x in r] for r in rows])
    vib = text.rsplit('VIBRATIONAL FREQUENCIES', 1)[1].split('NORMAL MODES')[0]
    imaginary = re.findall(r'^\s*(\d+):\s+(-[\d.]+) cm\*\*-1', vib, re.M)
    assert len(data) == 119 and len(imaginary) == 1
    assert imaginary[0] == ('6', '-147.16')
    assert np.all(data[:, 1] > 0)
    freq, intensity = data[:, 1], data[:, 3]
    x = np.linspace(0, 4000, 16001)
    fwhm = 12.0
    # Area-normalised Lorentzian broadening of the final IR table, scale 1.000.
    half = fwhm / 2
    y = np.sum(intensity[:, None] * (half / np.pi) /
               ((x[None, :] - freq[:, None])**2 + half**2), axis=0)
    y /= y.max()
    fig = canvas('RYBA / IR ANALYSIS', 'Every vibration has a signature.',
                 'Calculated IR bands from the final frequency job in TS1.out. Positive-frequency modes are shown.')
    panel(fig, .045, .226, .91, .538)
    fig.text(.065, .723, 'CALCULATED IR SPECTRUM', size=11, weight='bold', color=MUTED)
    fig.text(.935, .723, 'Lorentzian / FWHM 12 cm⁻¹', size=11, color=TEAL, ha='right')
    ax = fig.add_axes([.105, .322, .807, .335])
    axes_style(ax)
    ax.vlines(freq, 0, intensity / intensity.max() * .89, color=GOLD, lw=.8, alpha=.65)
    ax.fill_between(x, 0, y, color=TEAL, alpha=.09)
    ax.plot(x, y, color=TEAL, lw=1.8)
    ax.set_xlim(4000, 0)
    ax.set_ylim(0, 1.22)
    ax.set_yticks([0, .25, .5, .75, 1.0])
    ax.set_ylabel('Normalised intensity', size=11, labelpad=12)
    ax.set_xlabel('Wavenumber / cm⁻¹', size=11, labelpad=12)
    peaks, _ = find_peaks(y, height=.13, distance=120)
    selected = sorted(peaks, key=lambda k: y[k], reverse=True)
    labels = []
    for k in selected:
        if all(abs(x[k] - x[j]) > 110 for j in labels):
            labels.append(k)
        if len(labels) == 4:
            break
    for k in labels:
        ax.annotate(f'{x[k]:.0f}', (x[k], y[k]), xytext=(0, 13), textcoords='offset points',
                    color=TEXT, ha='center', size=10)
    fig.text(.065, .264, 'Broadened bands', color=TEAL, size=10)
    fig.text(.211, .264, 'Harmonic stick spectrum', color=GOLD, size=10)
    fig.text(.935, .264, 'Frequency scale 1.000', color=MUTED, size=10, ha='right')
    fig.text(.065, .158, '119 REAL MODES', color=TEAL, size=10, weight='bold')
    fig.text(.065, .119, 'Final frequency calculation', size=16)
    fig.text(.440, .158, 'ONE IMAGINARY MODE', color=GOLD, size=10, weight='bold')
    fig.text(.440, .119, '−147.16 cm⁻¹ · mode 6', size=16)
    fig.text(.045, .039, 'TS1.out  /  Scientific data visualisation  /  Positive modes only; no experimental spectrum implied.', color=MUTED, size=9)
    dest = ROOT / 'assets/img/overview-ir-spectrum.png'
    fig.savefig(dest, dpi=150)
    plt.close(fig)
    return {'source_job': 'last IR SPECTRUM / last VIBRATIONAL FREQUENCIES',
            'positive_ir_modes': len(data), 'imaginary_frequency_cm_1': -147.16,
            'imaginary_source_mode_id': 6, 'frequency_scale': 1.0,
            'broadening': 'area-normalised Lorentzian, FWHM 12 cm^-1; curve normalised to its maximum',
            'strongest_stick_frequency_cm_1': float(freq[np.argmax(intensity)])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ir', type=Path, required=True)
    parser.add_argument('--goat', type=Path, required=True)
    parser.add_argument('--ensemble', type=Path, required=True)
    args = parser.parse_args()
    summary = {'kind': 'Scientific illustrations generated from supplied ORCA data; not application screenshots.',
               'sources': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (args.ir, args.goat, args.ensemble)},
               'ir': render_ir(args.ir), 'goat': render_goat(args.goat, args.ensemble)}
    dest = ROOT / 'assets/data/overview-provenance.json'
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
