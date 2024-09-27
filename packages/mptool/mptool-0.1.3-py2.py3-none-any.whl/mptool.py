#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cobra
import gurobipy as grb
import networkx as nx
import numpy as np
import os
import sys
import time

from itertools import combinations
from pathlib import Path
from warnings import warn


def load_cobra_model(path):
    """Loads a single COBRA model from SBML, JSON, or MATLAB file."""
    if not isinstance(path, str) and len(path) > 1:
        raise TypeError('Only accepts path to a single model')
    return load_cobra_models(path).pop()


def load_cobra_models(paths, suffixes=('sbml', 'xml', 'json', 'mat')):
    """ Loads one or more COBRA models from SBML, JSON, or MATLAB files.

    Args:
        path (Iterable): Paths to models or directories containing models.
        suffixes (Iterable): File endings to use (sbml, xml, json, or mat).

    Returns:
        list: COBRA models.
    """

    if isinstance(paths, str):
        paths = [paths]

    cobra_models = []

    while paths:
        path = paths.pop(0)

        # Get model files if path is a directory
        if os.path.isdir(path):
            paths.extend(_get_cobra_model_paths(path))
            continue

        # Check suffix
        suffix = path.split('.')[-1]
        if suffix not in suffixes:
            continue

        # Try to load model
        if suffix in ('xml', 'sbml'):
            try:
                cobra_model = cobra.io.read_sbml_model(path)
            except cobra.io.sbml3.CobraSBMLError:
                warn('Failed to read {} as SBML file'.format(path))
                continue
        elif suffix == 'json':
            try:
                cobra_model = cobra.io.load_json_model(path)
            except ValueError:
                warn('Failed to read {} as JSON file'.format(path))
                continue
        elif suffix == 'mat':
            try:
                cobra_model = cobra.io.load_matlab_model(path)
            except ValueError:
                warn('Failed to read {} as MATLAB file'.format(path))
                continue

        cobra_models.append(cobra_model)

    return cobra_models


def _get_cobra_model_paths(path, suffixes=['sbml', 'xml', 'json', 'mat']):
    """Returns a list of paths to SBML, JSON, and MATLAB files in directory."""
    return [os.path.join(path, x) for x in os.listdir(path)
            if x.split('.')[-1] in suffixes]


def load_set(path):
    """Loads a set of strings from file (one string per line)."""
    with open(path, 'r') as f:
        return set(l.strip() for l in f)


def save_set(s, path):
    """Writes a set of strings to file (one string per line)."""
    with open(path, 'w') as f:
        for x in sorted(s):
            f.write(x + '\n')


def load_sets(path):
    """Loads a set of frozensets of strings from CSV file."""
    with open(path, 'r') as f:
        return set(frozenset(l.strip().split(',')) for l in f)


def save_sets(sets, path):
    """Writes sets of strings to CSV file."""
    with open(path, 'w') as f:
        for x in sorted([sorted(s) for s in sets],
                        key=lambda x: (len(x), x[0])):
            f.write(','.join(x) + '\n')


def load_bounds(path):
    """Loads bounds from CSV file to dict."""
    bounds = {}
    with open(path, 'r') as f:
        for line in f:
            r, lb, ub = line.strip().split(',')
            bounds[r] = float(lb), float(ub)
    return bounds


def save_bounds(bounds, path):
    """Writes bounds from dict to CSV file."""
    with open(path, 'w') as f:
        for r in sorted(bounds):
            lb, ub = [str(x) for x in bounds[r]]
            f.write(','.join([r, lb, ub]) + '\n')


def find_mps(model, subset=set(), method='iterative', graph=True, random=False,
             bounds={}, tighten=True, tol=1e-9, inf=1000, threads=0, max_mps=0,
             max_t=0, verbose=False, export=False, output_dir=''):
    """Enumerates or samples MPs in the subset using either direct or iterative
    minimization. The iterative method can be accelerated by using a graph or
    the order of MPs can be randomized (but not both). Enumeration with the
    iterative method also finds MCs.

    Args:
        model (Model): COBRA or Gurobi model to use.
        subset (Iterable): The subset of reactions that can be part of MPs. The
            reactions ca be given as IDs, Gurobi variables, or COBRA reactions.
            If empty, all reactions in the model are included in the subset.
        method (str): Minimization method to use (iterative or direct).
        graph (bool): Use graph to accelerate enumeration (only iterative)?
        random (bool): Randomize order of MPs (only iterative)?
        bounds (dict): Flux bounds to replace the flux bounds in the model. A
            dict with reaction IDs as keys and tuples of flux bounds as values.
        tighten (bool): Use flux variability analysis to tighten bounds?
        tol (float): Numerical tolerance (the minimum, 1e-9, is recommended).
        inf (float): Largest allowed flux bound ("infinity").
        threads (int): Threads to use for optimizer (0 for all cores).
        max_mps (int): Maximum number of MPs to find (0 for no limit, must be
            non-zero for random sampling if no time limit is specified).
        max_t (float): Maximum time in seconds (0 for no limit, must be
            non-zero for random sampling if no MP limit is specified).
        verbose (bool): Print information as MPs are found?
        export (bool): Write data to files (log, subset, bounds, MPs, and MCs)?
        output_dir (str): Directory for file export.

    Returns:
        mps (set): MPs found (each MP is a frozenset of reaction IDs).
        mcs (set): MCs found (each MC is a frozenset of reaction IDs).
        complete (bool): Were all MPs found (cannot be checked for random)?

    Raises:
        ValueError: If arguments are invalid or incompatible.
        TypeError: If model is not COBRA or Gurobi model.
        AssertionError: If model is infeasible.
    """

    # Timestamp (with microseconds) to uniquely identify enumeration
    t = time.time()
    ts = time.strftime('%Y%m%d_%H%M%S{}'.format(str(t).split('.')[-1]),
                       time.localtime(t))

    # Create the output directory if it doesn't exist
    if output_dir != '':
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Create or copy Gurobi model
    if isinstance(model, cobra.Model):
        model = create_lp(model)
    elif isinstance(model, grb.Model):
        model.update()
        model = model.copy()
        model.ModelName = model.ModelName.replace('_copy', '')
    else:
        raise TypeError('Only COBRA and Gurobi models are supported')

    # Check for other invalid or incompatible arguments
    if method not in ('direct', 'iterative'):
        raise ValueError('Method {} not supported'.format(method))
    if method == 'direct' and random:
        random = False
        warn('Direct method is incompatible with randomization (turned off)')
    if method == 'direct' and graph:
        graph = False
        warn('Graph not implemented for direct method (turned off)')
    if random and not (max_t or max_mps):
        raise ValueError('Randomization requires time limit or sample size')
    if graph and random:
        graph = False
        warn('Graph and randomization are incompatible (turned off graph')

    # Set Gurobi parameters
    model.setParam('OutputFlag', False)
    model.setParam('Threads', threads)
    if max_t:
        model.setParam('TimeLimit', max_t)
    for p in ('OptimalityTol', 'FeasibilityTol', 'IntFeasTol'):
        model.setParam(p, tol)

    # Set bounds and apply maximal flux bound
    for v in model.getVars():
        if bounds:
            v.lb, v.ub = bounds[v.varName]
        model.update()
        v.lb, v.ub = np.max([v.lb, -inf]), np.min([v.ub, inf])

    # Check feasibility
    model.setObjective(grb.LinExpr())
    model.optimize()
    assert model.status == 2, 'Infeasible model'

    # Convert subset to model variables
    if subset:
        s = set()
        for x in subset:
            if isinstance(x, grb.Var):
                # Necessary to get variable by name because model was copied
                s.add(model.getVarByName(x.varName))
            elif isinstance(x, cobra.Reaction):
                s.add(model.getVarByName(x.id))
            elif isinstance(x, str):
                s.add(model.getVarByName(x))
            else:
                warn('Subset can only contain strings, variables or reactions')
        subset = s
    else:
        subset = set(model.getVars())

    if verbose:
        print(model.ModelName)
        print('Network size:', len(model.getVars()))
        print('Subset size:', len(subset))

    if export:
        # Write subset to timestamped file
        filename = '_'.join([model.ModelName, ts, 'subset.txt'])
        save_set([v.varName for v in subset],
                  os.path.join(output_dir, filename))

    # Get bounds and tighten if specified
    if tighten:
        # Run flux variability analysis to get tight bounds
        if verbose:
            print('\nFlux variability analysis...')
        bounds = fva(model, verbose=verbose)
    else:
        bounds = {v.varName: (v.lb, v.ub) for v in model.getVars()}

    if export:
        # Write bounds to timestamped file
        filename = '_'.join([model.ModelName, ts, 'bounds.csv'])
        save_bounds(bounds, os.path.join(output_dir, filename))

    # Find blocked and essential reactions in subset (finds all if FVA is used)
    blocked = set()
    essential = set()
    for v in model.getVars():
        b = v.lb, v.ub
        if v in subset:
            if not np.any(b):
                blocked.add(v)
            elif np.all(b) and len(set(np.sign(b))) == 1:
                essential.add(v)

    # Remove blocked and essential reactions from subset
    subset -= blocked | essential

    # Make subset irreversible
    if verbose:
        print('\nMaking subset irreversible...')
    subset = make_irreversible(model, subset)

    if verbose:
        print('\nNetwork size:', len(model.getVars()))
        print('Subset size:', len(subset))
        print('\nFinding MPs...')

    if export:
        # Open log file and write header
        suffix = 'incomplete_log.csv'
        if random:
            suffix = 'random_' + suffix
        filename = '_'.join([model.ModelName, ts, suffix])
        log = open(os.path.join(output_dir, filename), 'w')
        log.write('mps,mcs,mp_size,subset_size,network_size,dt\n')
    else:
        log = None

    # Start timer
    t0 = time.time()

    # Enumerate MPs
    if method == 'iterative':
        if random:
            mcs = None
            complete = None
            mps = _find_mps_iter_rand(model, subset, tol, threads, max_mps,
                                      max_t, log, verbose)
        else:
            mps, mcs, complete = _find_mps_iter(model, subset, graph, random,
                                                tol, threads, max_mps, max_t,
                                                log, verbose)
    elif method == 'direct':
        mcs = None
        mps, complete = _find_mps_dir(model, subset, max_mps, max_t, log,
                                      verbose)

    # Record runtime
    dt = time.time() - t0

    if export:
        # Close log file
        log.close()

    if verbose:
        if complete:
            print('\nEnumeration complete!')
        elif max_t and dt >= max_t:
            print('\nTime limit reached.')
        elif mps and len(mps) == max_mps:
            print('\nMaximum number of MPs reached.')
        print('Runtime: {:.2f} s'.format(dt))

    # Add essential reactions to MPs and MCs
    if essential:
        if verbose:
            print('\nAdding essential reactions to MPs and MCs...')

        if mps:
            mps = set(mp | essential for mp in mps)
        else:
            mps = set([frozenset(essential)])

        if mcs is not None:
            mcs |= set(frozenset([v]) for v in essential)

    # Convert MPs and MCs from variables to reaction IDs
    if mps:
        mps = set(frozenset(v.varName for v in mp) for mp in mps)
    if mcs:
        mcs = set(frozenset(v.varName for v in mc) for mc in mcs)

    status = 'complete' if complete else 'incomplete'

    if mps:
        if verbose:
            # Print MP statistics
            unique = set(v for mp in mps for v in mp)
            lengths = [len(mp) for mp in mps]
            print('\nMPs: {}'.format(len(mps)))
            print('Reactions in MPs: {}'.format(len(unique)))
            print('Mean MP size: {:.2f}'.format(np.mean(lengths)))

        if export:
            # Write MPs to file
            suffix = status + '_mps.csv'
            if random:
                suffix = 'random_' + suffix
            filename = '_'.join([model.ModelName, ts, suffix])
            save_sets(mps, os.path.join(output_dir, filename))

    if mcs:
        if verbose:
            # Print MC statistics
            unique = set(v for mc in mcs for v in mc)
            lengths = [len(mc) for mc in mcs]
            print('\nMCs: {}'.format(len(mcs)))
            print('Reactions in MCs: {}'.format(len(unique)))
            print('Mean MC size: {:.2f}'.format(np.mean(lengths)))

        if export:
            # Write MCs to file
            suffix = status + '_mcs.csv'
            if random:
                suffix = 'random_' + suffix
            filename = '_'.join([model.ModelName, ts, suffix])
            save_sets(mcs, os.path.join(output_dir, filename))

    if complete and export:
        # Rename log file if enumeration complete
        suffix = 'incomplete_log.csv'
        if random:
            suffix = 'random_' + suffix
        path = '_'.join([model.ModelName, ts, suffix])
        if path in os.listdir('.'):
            filename = path.replace('incomplete', 'complete')
            os.rename(path, os.path.join(output_dir, filename))

    return mps, mcs, complete


def _find_mps_iter(model, subset, graph, random, tol, threads, max_mps, max_t,
                   log, verbose):
    """Finds MPs and MCs in subset using iterative minimization."""

    # Create global binary integer program (BIP)
    global_bip = grb.Model('global_bip')
    global_bip.setParam('OutputFlag', False)
    global_bip.setParam('Threads', threads)
    if max_t:
        global_bip.setParam('TimeLimit', max_t)

    # Get subset bounds
    ub = {v: v.ub for v in subset}

    # Find MPs and MCs
    mps = set()
    mcs = set()
    g = nx.Graph()
    q = []
    n = model.numVars
    t0 = time.time()

    while True:
        # Get clique from queue or use full subset
        try:
            s = q.pop()
        except IndexError:
            s = subset

        # Set bounds
        for v in subset:
            if v in s:
                v.ub = ub[v]
            else:
                v.ub = 0

        # Set BIP
        if s == subset:
            bip = global_bip
        else:
            bip = grb.Model('bip')
            bip.setParam('OutputFlag', False)
            bip.setParam('Threads', threads)
            bip.setParam('Presolve', 0)
            if max_t:
                dt = time.time() - t0
                if dt >= max_t:
                    break
                else:
                    bip.setParam('TimeLimit', max_t - dt)
            for mp in mps:
                if mp < s:
                    _constrain_indicators(bip, mp, '>', 1)

        # Start with empty cut
        cut = set()

        while True:
            if verbose and s == subset:
                # Indicate that full model is being solved
                print('\n*')

            # Find new non-minimal cut
            while True:
                # Remove previous cut
                if cut is not None:
                    for v in cut:
                        v.ub = ub[v]

                cut = _find_cut(bip, model)

                # Record time
                dt = time.time() - t0

                if cut is None:
                    break

                # Check time and update time limits
                if max_t:
                    if dt >= max_t:
                        break
                    else:
                        bip.setParam('TimeLimit', max_t - dt)
                        model.setParam('TimeLimit', max_t - dt)

                # Apply new cut
                for v in cut:
                    v.ub = 0

                # Prevent cut from being found again if it is minimal
                model.optimize()
                if model.status != 2:
                    _constrain_indicators(bip, cut, '<', len(cut) - 1)
                    if cut and s == subset:
                        # Save minimal cut
                        mcs.add(cut)
                        if verbose:
                            print('MC', len(mcs),
                                  sorted([v.varName for v in cut]))
                else:
                    break

            if cut is None or (max_t and dt >= max_t):
                break

            # Find new MP
            mp = _find_mp_iter(model, s - cut, False, tol)

            # Record time
            dt = time.time() - t0

            # Check and save MP
            if not mp:
                break
            assert mp not in mps, 'MP already found (check numerical issues)'
            mps.add(mp)

            if verbose:
                print('MP', len(mps), sorted([v.varName for v in mp]))

            if log:
                line = [len(mps), len(mcs), len(mp), len(s), n, dt]
                log.write(','.join([str(x) for x in line]))
                log.write('\n')

            # Check time and update time limits
            if max_t:
                if dt >= max_t:
                    break
                else:
                    bip.setParam('TimeLimit', max_t - dt)
                    model.setParam('TimeLimit', max_t - dt)

            if len(mps) == max_mps:
                break

            # Require MP to be covered by subsequent cuts
            _constrain_indicators(bip, mp, '>', 1)
            if bip != global_bip:
                _constrain_indicators(global_bip, mp, '>', 1)

            # Update graph with MP and find new edges and cliques
            if graph and s == subset:
                # Add new edges to graph
                edges = [e for e in combinations([v.varName for v in mp], 2)
                         if not g.has_edge(*e)]
                g.add_edges_from(edges)

                # Add new cliques to queue
                cliques = []
                for c in nx.find_cliques(g):
                    x = set(model.getVarByName(n) for n in c)
                    if x == mp:
                        continue
                    for e in edges:
                        if set(e) < set(c):
                            cliques.append(x)
                            break
                if verbose:
                    print('New edges:', len(edges))
                    print('New cliques:', len(cliques))

                q.extend(cliques)

                if q:
                    # Start processing queue
                    break

        if (max_t and dt >= max_t) or len(mps) == max_mps:
            complete = False
            break
        elif s == subset and (cut is None or not mp):
            complete = True
            break

    return mps, mcs, complete


def _find_mps_iter_rand(model, subset, tol, threads, max_mps, max_t, log,
                        verbose):
    """Finds MPs and MCs in subset using randomized iterative minimization."""

    # Get subset bounds
    ub = {v: v.ub for v in subset}

    # Find MPs and MCs
    mps = set()

    n = model.numVars
    t0 = time.time()
    dt = 0

    while True:
        model.update()
        mp = _find_mp_iter(model, subset, True, tol)
        if not mp:
            break

        # Record time
        dt = time.time() - t0

        # Check and save MP
        if mp not in mps:
            mps.add(mp)
            if log:
                line = [len(mps), np.nan, len(mp), len(subset), n, dt]
                log.write(','.join([str(x) for x in line]))
                log.write('\n')
            if verbose:
                print(len(mps), sorted([v.varName for v in mp]))
        else:
            warn('Same MP sampled several times, consider enumeration instead')

        if (max_t and dt >= max_t) or (max_mps and len(mps) == max_mps):
            break

        if max_t:
            model.setParam('TimeLimit', max_t - dt)

    return mps


def _find_mps_dir(model, subset, max_mps, max_t, log, verbose):
    """Finds MPs in subset using direct minimization."""

    # Add binary indicators for all variables
    _add_indicators(model, subset)

    mps = set()
    n = model.numVars
    t0 = time.time()

    while True:
        # Find new MP
        mp = _find_mp_dir(model, subset)

        # Record time
        dt = time.time() - t0

        # Check and save MP
        if not mp:
            break
        assert mp not in mps, 'Same MP found twice (check numerical issues)'
        mps.add(mp)

        if log:
            line = [len(mps), np.nan, len(mp), len(subset), n, dt]
            log.write(','.join([str(x) for x in line]))
            log.write('\n')

        if verbose:
            print(len(mps), sorted([v.varName for v in mp]))

        # Check time and update time limits
        if max_t:
            if dt >= max_t:
                break
            else:
                model.setParam('TimeLimit', max_t - dt)

        if len(mps) == max_mps:
            break

        # Prevent MP from being found again
        _constrain_indicators(model, mp, '<', len(mp) - 1)

    if (max_t and dt >= max_t) or len(mps) == max_mps:
        complete = False
    else:
        complete = True

    return mps, complete


def create_lp(cobra_model, parameters={}, attributes={}):
    """Creates a Gurobi LP model from a COBRA model.

    Args:
        cobra_model: COBRA model.
        parameters: Gurobi parameters.
        attributes: Gurobi attributes.

    Returns:
        Gurobi model.
    """

    lp = grb.Model(cobra_model.id)

    # Add variables and get constraints
    constr = {m: [] for m in cobra_model.metabolites if m._reaction}
    for r in cobra_model.reactions:
        x = lp.addVar(r.lower_bound, r.upper_bound, r.objective_coefficient,
                      'continuous', r.id)
        for m, c in r.metabolites.items():
            constr[m].append((c, x))

    lp.update()

    # Add constraints
    for m in constr:
        c = grb.LinExpr(constr[m])
        lp.addConstr(c, '=', m._bound, m.id)

    # Set parameters and attributes
    lp.setParam('OutputFlag', False)
    for k, v in parameters.items():
        lp.setParam(k, v)
    for k, v in attributes.items():
        lp.setAttr(k, v)

    lp.update()

    return lp


def make_irreversible(model, subset=set()):
    """Makes reactions in subset of model positive and irreversible.

    Args:
        model: COBRA or Gurobi model.
        subset: Iterable containing reactions to make irreversible or their IDs
                (if empty, all reactions in model are made irreversible).

    Returns:
        Subset with irreversible reactions.
    """
    if isinstance(model, cobra.Model):
        return _make_irreversible_cobra(model, subset)
    elif isinstance(model, grb.Model):
        return _make_irreversible_gurobi(model, subset)


def _make_irreversible_cobra(model, subset):
    """Makes reactions in subset of COBRA model positive and irreversible."""

    if not subset:
        subset = set(model.reactions)
    else:
        subset = set(subset)
        for x in subset:
            if isinstance(x, str):
                subset.remove(x)
                subset.add(model.reactions.get_by_id(x))

    new_reactions = []

    for r in list(subset):
        if r.lower_bound < 0:
            if r.upper_bound > 0:
                # Create new reverse reaction
                r_rev = cobra.Reaction(r.id + '_rev')
                r_rev.add_metabolites(
                    {m: -c for m, c in r.metabolites.items()})
                r_rev.bounds = np.max([0, -r.upper_bound]), -r.lower_bound
                new_reactions.append(r_rev)
                subset.add(r_rev)
            else:
                # Reverse existing reaction
                r.bounds = np.max([0, -r.upper_bound]), -r.lower_bound
                r.add_metabolites(
                    {m: -2 * c for m, c in r.metabolites.items()})
                # Remove reaction to avoid reported bug with Gurobi 9
                model.remove_reactions([r])
                r.id += '_rev'
                new_reactions.append(r)
        if r.upper_bound > 0:
            # Make existing reaction irreversible
            r.lower_bound = np.max([0, r.lower_bound])

    model.repair()
    model.add_reactions(new_reactions)

    return subset


def _make_irreversible_gurobi(model, subset):
    """Makes reactions in subset of Gurobi model positive and irreversible."""

    model.update()

    if not subset:
        subset = set(model.getVars())
    else:
        subset = set(subset)
        for x in subset:
            if isinstance(x, str):
                subset.remove(x)
                subset.add(model.getVarByName(x))

    to_reverse = []

    for r in list(subset):
        if r.ub > 0:
            # Make existing reaction irreversible
            r.lb = np.max([0, r.lb])
        if r.lb < 0:
            if r.ub > 0:
                # Create new reverse reaction
                r_rev = model.addVar(np.max([0, -r.ub]), -r.lb, r.obj, r.VType,
                                     r.varName + '_rev')
                to_reverse.append((r, r_rev))
            else:
                # Reverse existing reaction
                r.varName += '_rev'
                r.lb, r.ub = np.max([0, -r.ub]), -r.lb
                for c in model.getConstrs():
                    model.chgCoeff(c, r, -model.getCoeff(c, r))

    model.update()

    for (r, r_rev) in to_reverse:
        for c in model.getConstrs():
            model.chgCoeff(c, r_rev, -model.getCoeff(c, r))
            subset.add(r_rev)

    model.update()

    return subset


def fva(model, verbose=False):
    """Flux variability analysis (FVA).

    Args:
        model (Model): Gurobi model to use.
        verbose (bool): Print information?

    Returns:
        bounds (dict): Reaction IDs are keys and flux bounds are values.
        solutions (dict): Tuples of reaction ID and objective sense are keys
            and flux bounds are values.
    """

    model.update()

    # Set empty objective
    obj = model.getObjective()
    model.setObjective(grb.LinExpr())

    # Check feasibility
    model.optimize()
    assert model.status == 2, 'Infeasible model'

    bounds = {}

    for i, v in enumerate(model.getVars()):
        # Add to objective
        v.obj = 1

        # Minimize
        model.ModelSense = 1
        model.optimize()
        vmin = v.x

        # Maximize
        model.ModelSense = -1
        model.optimize()
        vmax = v.x

        # Save bounds
        bounds[v.varName] = (vmin, vmax)

        # Remove from objective
        v.obj = 0

        if verbose:
            print(i, v.varName, bounds[v.varName])

    # Reset original objective
    model.setObjective(obj)

    return bounds


def _add_indicators(model, variables):
    """Adds binary indicators and couples them to variables if possible."""

    ind_constr = {}
    model_vars = set(v.varName for v in model.getVars())

    for v in variables:
        b_id = v.varName + '_ind'
        if b_id not in model_vars:
            b = model.addVar(vtype='B', name=b_id)
            if v.varName in model_vars:
                ind_constr[v] = [(1, v), (-v.ub, b)]

    model.update()

    if ind_constr:
        for v, c in ind_constr.items():
            model.addConstr(grb.LinExpr(c), '<', 0)


def _constrain_indicators(model, variables, operator, rhs):
    """Constrains binary indicators of given variables."""
    _add_indicators(model, variables)
    c = [(1, model.getVarByName(v.varName + '_ind')) for v in variables]
    model.addConstr(grb.LinExpr(c), operator, rhs)


def _find_mp_dir(model, subset):
    """Finds an MP in the subset using direct minimization."""
    c = [model.getVarByName(v.varName + '_ind') for v in subset]
    w = np.ones(len(c))
    model.setObjective(grb.LinExpr(w, c), 1)
    model.optimize()
    if model.status == 2:
        return frozenset(v for v in subset
                         if model.getVarByName(v.varName + '_ind').x > 0.5)
    else:
        return None


def _find_mp_iter(model, subset, random, tol):
    """Finds an MP in the subset using iterative minimization."""

    # Random number generator
    rng = np.random.default_rng()

    # Get candidate reactions and their upper bounds
    c = set(subset)
    ub = {v: v.ub for v in c}

    # Check feasibility
    model.setObjective(grb.LinExpr())
    model.optimize()
    if model.status != 2:
        mp = None

    else:
        mp = set()
        z = set()

        while c:
            # Deactivate a random candidate reaction
            # x = rng.choice(tuple(c))
            # Workaround for memory leak in rng.choice
            x = tuple(c)[rng.integers(0, len(c))]
            c.remove(x)
            x.ub = 0

            if random and x in z:
                continue

            # Minimize subset fluxes
            w = np.ones(len(c))
            model.setObjective(grb.LinExpr(w, c), 1)
            model.optimize()

            if model.status != 2:
                # Reactivate candidate reaction and add to MP
                x.ub = ub[x]
                mp.add(x)
            else:
                # Get reactions without flux from candidate set
                z = set(v for v in c if np.abs(v.x) < tol)
                if not random:
                    c -= z
                    for v in z:
                        v.ub = 0

    # Reset upper bounds
    for v in subset:
        v.ub = ub[v]

    if mp:
        mp = frozenset(mp)

    return mp


def _find_cut(bip, model):
    """Finds a new cut that disables all known MPs."""
    c = bip.getVars()
    w = np.ones(len(c))
    bip.setObjective(grb.LinExpr(w, c), 1)
    bip.optimize()
    if bip.status == 2:
        return frozenset(model.getVarByName(b.varName[:-4])
                         for b in bip.getVars() if b.x > 0.5)
    else:
        return None


if __name__ == '__main__':
    # Set parameters
    method = 'iterative'
    graph = True
    random = False
    bounds = {}
    tighten = True
    inf = 1000
    tol = 1e-9
    threads = 0
    max_mps = 0
    max_t = 0
    verbose = True
    export = True

    # Load COBRA model
    cobra_model = load_cobra_model(sys.argv[1])

    # Try to load bounds
    try:
        bounds = load_bounds(sys.argv[2])
    except IndexError:
        bounds = {}

    # Choose random subset
    # Using numpy.random.choice once for convenience despite memory leak issue
    n = int(len(cobra_model.reactions) / 6)
    subset = np.random.choice(cobra_model.reactions, n, replace=False)
    subset = set([r.id for r in subset])

    # Find MPs and MCs
    mps, mcs, complete = find_mps(cobra_model, subset=subset, method=method,
                                  graph=graph, random=random, bounds=bounds,
                                  tighten=tighten, inf=inf, tol=tol,
                                  max_mps=max_mps, max_t=max_t,
                                  verbose=verbose, export=export)
