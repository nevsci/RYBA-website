#!/usr/bin/env python3
"""Render three overview figures from an unmodified saved RYBA project archive.

Usage: python scripts/render-project-overview.py /path/to/project.ryba.zip
Requires numpy, scipy and matplotlib (shared styling in render-overview.py).
Raw project state and embedded output files are never written to the website.
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re
from zipfile import ZipFile

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.patches import Circle
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('overview_style', Path(__file__).with_name('render-overview.py'))
style = importlib.util.module_from_spec(spec)
spec.loader.exec_module(style)
BG, PANEL, TEXT, MUTED, TEAL, GOLD = (getattr(style, k) for k in ('BG', 'PANEL', 'TEXT', 'MUTED', 'TEAL', 'GOLD'))


def project_xyz(text):
    lines = text.strip().splitlines()
    n = int(lines[0])
    rows = [r.split() for r in lines[2:2 + n]]
    assert len(rows) == n
    return [r[0] for r in rows], np.array([[float(v) for v in r[1:4]] for r in rows])


def result_xyz(result):
    index = result['preferredGeometryIndex']
    atoms = result['geometries'][index]['atoms']
    return [a['symbol'] for a in atoms], np.array([[a[k] for k in ('x', 'y', 'z')] for a in atoms])


def camera(xyz, yaw=0, pitch=.18):
    c, s = np.cos(yaw), np.sin(yaw)
    ry = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    c, s = np.cos(pitch), np.sin(pitch)
    rx = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    return (xyz - xyz.mean(0)) @ (rx @ ry).T


def principal_view(xyz, symbols):
    heavy = [i for i, s in enumerate(symbols) if s != 'H']
    _, _, vt = np.linalg.svd(xyz[heavy] - xyz[heavy].mean(0), full_matrices=False)
    view = vt.T
    view[:, -1] *= np.linalg.det(view)
    return (xyz - xyz.mean(0)) @ view


def fit_molecule(ax, xyz, symbols, margin=.65, hydrogens=True):
    shown = xyz if hydrogens else xyz[[i for i, s in enumerate(symbols) if s != 'H']]
    ax.set_xlim(shown[:, 0].min() - margin, shown[:, 0].max() + margin)
    ax.set_ylim(shown[:, 1].min() - margin, shown[:, 1].max() + margin)
    ax.set_aspect('equal')
    ax.set_axis_off()


def draw_molecule(ax, symbols, xyz, edges, hydrogens=True, size=1, bond_width=7):
    palette = {'C': '#9faeb8', 'H': '#e3e8e8', 'N': '#6e9fe3', 'O': '#e77577', 'F': '#91c66c'}
    shown = {i for i, s in enumerate(symbols) if hydrogens or s != 'H'}
    objects = [(float((xyz[i, 2] + xyz[j, 2]) / 2), 'bond', (i, j, order))
               for i, j, order in edges if i in shown and j in shown]
    objects += [(float(xyz[i, 2]), 'atom', i) for i in shown]
    for rank, (depth, kind, value) in enumerate(sorted(objects)):
        if kind == 'bond':
            i, j, order = value
            points = xyz[[i, j], :2]
            d = points[1] - points[0]
            length = np.linalg.norm(d)
            perp = np.array([-d[1], d[0]]) / max(length, 1e-8)
            offsets = [-.10, .10] if order == 2 else [0]
            width = bond_width * (.63 if order == 2 else 1)
            for offset in offsets:
                p = points + offset * perp
                ax.plot(p[:, 0], p[:, 1], lw=width, color='#465b67', solid_capstyle='round')
                ax.plot(p[:, 0], p[:, 1], lw=width * .62, color='#a6b9c0', solid_capstyle='round')
                ax.plot(p[:, 0] - .015, p[:, 1] + .022, lw=width * .20,
                        color='#d2dddd', alpha=.42, solid_capstyle='round')
        else:
            c = xyz[value, :2]
            radius = size * (.17 if symbols[value] == 'H' else .28)
            color = np.array(mcolors.to_rgb(palette[symbols[value]]))
            sphere_layer = 3 + rank * .001
            ax.add_patch(Circle(c, radius, facecolor=color * .42, edgecolor='#102029',
                                linewidth=.7, zorder=sphere_layer))
            # Concentric offset disks supply a deterministic soft ball-and-stick finish.
            for k in range(12):
                fraction = (k + 1) / 13
                r = radius * (1 - fraction * .72)
                light = np.clip(color * (.61 + fraction * .51) + fraction * .11, 0, 1)
                cc = c + np.array([-.18, .23]) * radius * fraction
                ax.add_patch(Circle(cc, r, facecolor=light, edgecolor='none',
                                    zorder=sphere_layer + (k + 1) * .00001))


def inferred_edges(symbols, xyz):
    return [(i, j, 1) for i, j in style.bonds(symbols, xyz)]


def render_geometry(state):
    mol = state['input']['project']['molecule']
    symbols, xyz = project_xyz(mol['xyzText'])
    connectivity = mol['connectivity']
    assert symbols == connectivity['atomSymbols']
    edges = [(b['a'], b['b'], b['order']) for b in connectivity['bonds']]
    assert len(symbols) == 23 and len(edges) == 22
    counts = Counter(symbols)
    assert counts == {'C': 8, 'H': 11, 'F': 1, 'O': 3}
    coords = camera(xyz, yaw=-.32, pitch=.30)
    # In-plane camera roll only; input distances and assigned bond orders stay intact.
    angle = np.radians(17)
    roll = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
    coords = coords @ roll.T
    assert np.allclose(np.linalg.norm(xyz[:, None] - xyz[None, :], axis=2),
                       np.linalg.norm(coords[:, None] - coords[None, :], axis=2))
    fig = style.canvas('RYBA / GEOMETRY WORKSHOP', 'Build, inspect and refine.',
                       'The saved Geometry Workshop structure, rendered directly from its coordinates and assigned connectivity.')
    style.panel(fig, .045, .201, .625, .562)
    style.panel(fig, .701, .201, .254, .562)
    fig.text(.065, .722, 'Fum_ketone', size=16, weight='bold')
    fig.text(.065, .688, 'C₈H₁₁FO₃ / saved molecular structure', size=11, color=MUTED)
    ax = fig.add_axes([.067, .265, .584, .389])
    fit_molecule(ax, coords, symbols, margin=.8)
    draw_molecule(ax, symbols, coords, edges, size=1.13, bond_width=10)
    fig.text(.065, .234, 'Carbon', color='#bdc8ce', size=10)
    fig.text(.137, .234, 'Hydrogen', color='#e3e8e8', size=10)
    fig.text(.227, .234, 'Oxygen', color='#e77577', size=10)
    fig.text(.307, .234, 'Fluorine', color='#91c66c', size=10)
    fig.text(.722, .720, 'STRUCTURE AT A GLANCE', size=10, color=MUTED, weight='bold')
    for y, number, label in [(.642, '23', 'atoms'), (.545, '22', 'assigned connections'), (.448, '3', 'double bonds')]:
        fig.text(.724, y, number, size=26, color=TEAL, weight='bold')
        fig.text(.782, y + .003, label, size=11)
    fig.text(.724, .334, f"Charge {mol['charge']}  ·  multiplicity {mol['multiplicity']}", size=11, color=MUTED)
    fig.text(.724, .269, 'Hydrogens and bond orders\nretained from the project.', size=10, color=MUTED, linespacing=1.7)
    measurements = {(3, 4): float(np.linalg.norm(xyz[3] - xyz[4])),
                    (2, 9): float(np.linalg.norm(xyz[2] - xyz[9]))}
    fig.text(.065, .143, 'SAVED GEOMETRY', size=10, weight='bold', color=TEAL)
    fig.text(.065, .105, f'C4=C5  {measurements[3, 4]:.3f} Å', size=18)
    fig.text(.414, .143, 'CARBONYL DISTANCE', size=10, weight='bold', color=TEAL)
    fig.text(.414, .105, f'C3=O10  {measurements[2, 9]:.3f} Å', size=18)
    fig.text(.045, .039, 'Saved RYBA project / Scientific data visualisation / Coordinates preserved; no geometry optimisation applied.', size=9, color=MUTED)
    fig.savefig(ROOT / 'assets/img/overview-geometry-render.png', dpi=150)
    plt.close(fig)
    return {'molecule_name': mol['name'], 'atom_count': 23, 'formula': 'C8H11FO3',
            'assigned_connections': 22, 'double_bonds': 3,
            'distances_A': {'C4-C5': measurements[3, 4], 'C3-O10': measurements[2, 9]},
            'notes': 'Unmodified saved input coordinates and assigned connectivity; hydrogens shown. Camera rotations only.'}


def render_uvvis(state):
    result = next(r for r in state['results'] if r['name'] == 'TTT-wHPBE')
    transitions = result['transitions']
    assert len(transitions) == 10
    assert all(t['multiplicity'] == 'singlet' and t['context'] == 'vertical' for t in transitions)
    settings = state['analysis']['spectrum']
    assert settings['shape'] == 'gaussian' and settings['fwhm'] == .3 and settings['normalize']
    energy = np.array([t['eV'] for t in transitions])
    nm = np.array([t['nm'] for t in transitions])
    strength = np.array([t['fosc'] for t in transitions])
    # Verify the saved parser values against the embedded length-gauge absorption table.
    table = result['rawText'].rsplit('ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS', 1)[1]
    table = table.split('ABSORPTION SPECTRUM VIA TRANSITION VELOCITY DIPOLE MOMENTS')[0]
    parsed = re.findall(r'^\s*0-1A\s+->\s+\d+-1A\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)', table, re.M)
    assert len(parsed) == 10
    assert np.allclose(np.array(parsed, float)[:, [0, 2, 3]], np.column_stack([energy, nm, strength]))
    wave = np.linspace(250, 800, 6601)
    sigma = settings['fwhm'] / (2 * np.sqrt(2 * np.log(2)))
    photon_energy = 1239.841984 / wave
    y = np.sum(strength[:, None] * np.exp(-.5 * ((photon_energy[None, :] - energy[:, None]) / sigma)**2), axis=0)
    y /= y.max()
    fig = style.canvas('RYBA / UV–VIS SPECTROSCOPY', 'From transitions to a spectrum.',
                       'TTT-wHPBE / ten calculated singlet transitions, with the Gaussian broadening saved in the project.')
    style.panel(fig, .045, .226, .91, .538)
    fig.text(.065, .723, 'CALCULATED ABSORPTION', size=11, weight='bold', color=MUTED)
    fig.text(.935, .723, 'Gaussian / FWHM 0.30 eV', size=11, color=TEAL, ha='right')
    ax = fig.add_axes([.105, .322, .785, .335])
    style.axes_style(ax)
    ax.fill_between(wave, 0, y, color=TEAL, alpha=.09)
    ax.plot(wave, y, color=TEAL, lw=2)
    ax.set_xlim(250, 800)
    ax.set_ylim(0, 1.2)
    ax.set_yticks([0, .25, .5, .75, 1])
    ax.set_xticks([250, 300, 400, 500, 600, 700, 800])
    ax.set_xlabel('Wavelength / nm', size=11, labelpad=12)
    ax.set_ylabel('Normalised intensity', size=11, labelpad=12)
    right = ax.twinx()
    right.spines[['top', 'left']].set_visible(False)
    right.tick_params(length=0, pad=10, labelsize=10)
    right.set_ylim(0, 1.2)
    right.set_yticks([0, .25, .5, .75, 1])
    right.vlines(nm, 0, strength, color=GOLD, lw=1.1, alpha=.75)
    right.set_ylabel('Oscillator strength / f', size=11, labelpad=12, color=GOLD)
    top = int(np.argmax(y))
    ax.annotate(f'{wave[top]:.0f} nm', (wave[top], y[top]), xytext=(0, 16), textcoords='offset points', ha='center', size=11)
    fig.text(.065, .264, 'Broadened spectrum', color=TEAL, size=10)
    fig.text(.249, .264, 'Electronic transitions', color=GOLD, size=10)
    fig.text(.935, .264, 'TTT-wHPBE', color=MUTED, size=10, ha='right')
    fig.text(.065, .158, 'DOMINANT TRANSITION / S1', size=10, weight='bold', color=TEAL)
    fig.text(.065, .119, f'{nm[0]:.1f} nm  ·  f = {strength[0]:.4f}', size=17)
    fig.text(.502, .158, 'CALCULATION CONTEXT', size=10, weight='bold', color=TEAL)
    fig.text(.502, .119, 'def2-TZVP / SMD(acetonitrile)', size=17)
    fig.text(.045, .039, 'Saved RYBA project / Scientific data visualisation / Normalised Gaussian profile; broadening applied in energy space.', size=9, color=MUTED)
    fig.savefig(ROOT / 'assets/img/overview-uvvis-render.png', dpi=150)
    plt.close(fig)
    return {'result_name': result['name'], 'transition_count': 10,
            'source_table': 'transition electric dipole moments (length gauge)',
            'fwhm_eV': .3, 'shape': 'Gaussian in photon energy, sampled on a wavelength axis; normalised maximum',
            'display_range_nm': [250, 800], 'transition_energies_eV': energy.tolist(),
            'transition_wavelengths_nm': nm.tolist(), 'oscillator_strengths': strength.tolist(),
            'notes': 'Saved energies, wavelengths and strengths checked against embedded raw ORCA table. Display range chosen for legibility; no spectral shift or frequency scaling.'}


def render_thermochemistry(state):
    pathway = state['analysis']['pathway']
    settings = pathway['energy']
    assert settings['recipe'] == 'gibbs' and settings['recordIndex'] == -1
    assert settings['units'] == 'kcal/mol' and settings['standardState'] == 'printed'
    states = pathway['series'][0]['states']
    assert len(states) == 7
    byid = {r['id']: r for r in state['results']}
    results = [byid[s['components'][0]['resultId']] for s in states]
    assert all(len(s['components']) == 1 and s['components'][0]['coefficient'] == 1 for s in states)
    g = []
    for r in results:
        record = r['thermochemistry'][-1]
        assert record['temperature'] == 298.15 and record['pressure'] == 1
        printed = re.findall(r'Final Gibbs free energy\s+\.\.\.\s+([-\d.]+)', r['rawText'])
        assert np.isclose(float(printed[-1]), record['freeEnergyG'], atol=1e-9, rtol=0)
        g.append(record['freeEnergyG'])
    refindex = next(i for i, s in enumerate(states) if s['id'] == settings['referenceStateId'])
    assert refindex == 0
    relative = (np.array(g) - g[refindex]) * 627.509474
    barriers = [float(relative[i] - relative[i - 1]) for i, s in enumerate(states) if s['role'] == 'ts']
    fig = style.canvas('RYBA / THERMOCHEMISTRY', 'Give energies a clear profile.',
                       'Seven states from the saved reaction pathway / Gibbs energies at 298.15 K, relative to the closed form.')
    style.panel(fig, .045, .198, .91, .566)
    fig.text(.065, .727, 'REACTION FREE-ENERGY PROFILE', size=11, weight='bold', color=MUTED)
    fig.text(.935, .727, 'ΔG / kcal mol⁻¹', size=11, color=TEAL, ha='right')
    # One structure directly above each plateau, retaining saved result/geometry assignments.
    plot_left, plot_width = .105, .807
    for i, (r, s) in enumerate(zip(results, states)):
        syms, xyz = result_xyz(r)
        # Source files have different atom orders. Orient each intact geometry
        # independently; never fit unmatched atom indices to one another.
        coords = principal_view(xyz, syms)
        edges = inferred_edges(syms, xyz)
        nitrogen = [j for j, symbol in enumerate(syms) if symbol == 'N']
        def carbon_neighbors(j):
            return sum(syms[b if a == j else a] == 'C' for a, b, _ in edges if j in (a, b))
        indoline_n = max(nitrogen, key=carbon_neighbors)
        if coords[indoline_n, 0] < 0:
            coords[:, [0, 2]] *= -1  # Proper 180-degree camera rotation.
        assert np.allclose(np.linalg.norm(xyz[:, None] - xyz[None, :], axis=2),
                           np.linalg.norm(coords[:, None] - coords[None, :], axis=2))
        cx = plot_left + plot_width * ((i + .5) / 7)
        ax = fig.add_axes([cx - .052, .559, .104, .123])
        fit_molecule(ax, coords, syms, margin=.7, hydrogens=False)
        draw_molecule(ax, syms, coords, edges, hydrogens=False, size=.88, bond_width=2.5)
    ax = fig.add_axes([plot_left, .292, plot_width, .244])
    style.axes_style(ax)
    ax.set_xlim(-.5, 6.5)
    ax.set_ylim(-3, 34.5)
    ax.set_yticks([0, 10, 20, 30])
    ax.set_xticks(range(7), [s['label'] for s in states])
    ax.tick_params(axis='x', labelsize=10)
    ax.set_ylabel('ΔG / kcal mol⁻¹', size=11, labelpad=12)
    width = .18
    for i, value in enumerate(relative):
        color = GOLD if states[i]['role'] == 'ts' else TEAL
        ax.plot([i - width, i + width], [value, value], color=color, lw=3.2, solid_capstyle='round')
        ax.text(i, value + 1.6, f'{value:.1f}', ha='center', color=color, size=11, weight='bold')
        if i < 6:
            ax.plot([i + width, i + 1 - width], [value, relative[i + 1]], color=TEAL, alpha=.65, lw=1.4)
    fig.text(.508, .226, 'Reaction coordinate', size=10, color=MUTED, ha='center')
    fig.text(.065, .137, 'FORWARD ACTIVATION FREE ENERGIES', size=10, color=GOLD, weight='bold')
    fig.text(.065, .100, '  /  '.join(f'{b:.1f}' for b in barriers) + ' kcal/mol', size=18)
    fig.text(.601, .137, 'CALCULATION CONTEXT', size=10, color=TEAL, weight='bold')
    fig.text(.601, .100, 'ωB97X-3c / SMD(acetonitrile)', size=16)
    fig.text(.045, .039, 'Saved RYBA project / Scientific data visualisation / Final printed Gibbs records; heavy-atom structures shown.', size=9, color=MUTED)
    fig.savefig(ROOT / 'assets/img/overview-thermochemistry-render.png', dpi=150)
    plt.close(fig)
    return {'recipe': 'Final printed Gibbs free energy, no additional correction', 'temperature_K': 298.15,
            'pressure_atm': 1, 'units': 'kcal/mol', 'reference': states[refindex]['label'],
            'state_labels': [s['label'] for s in states], 'result_names': [r['name'] for r in results],
            'geometry_indices': [r['preferredGeometryIndex'] for r in results],
            'gibbs_Eh': g, 'relative_gibbs_kcal_mol': relative.tolist(),
            'forward_barriers_kcal_mol': barriers,
            'notes': 'Final saved Gibbs values checked against last raw printed records. Same saved state order and geometry assignments; rigid rotations/translations only. Thumbnail connections inferred by distance; no invented bond orders.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    args = parser.parse_args()
    with ZipFile(args.project) as archive:
        manifest = json.loads(archive.read('manifest.json'))
        raw = archive.read('state.json')
    asset = next(a for a in manifest['assets'] if a['path'] == 'state.json')
    assert hashlib.sha256(raw).hexdigest() == asset['sha256']
    assert len(raw) == asset['bytes']
    state = json.loads(raw)
    assert state['format'] == 'ryba-workspace'
    summary = {'kind': 'Scientific data visualisations from a saved RYBA project, not interface screenshots.',
               'source_archive_sha256': hashlib.sha256(args.project.read_bytes()).hexdigest(),
               'source_state_sha256': asset['sha256'], 'source_app_version': state['appVersion'],
               'geometry': render_geometry(state), 'uvvis': render_uvvis(state),
               'thermochemistry': render_thermochemistry(state)}
    (ROOT / 'assets/data/project-overview-provenance.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
