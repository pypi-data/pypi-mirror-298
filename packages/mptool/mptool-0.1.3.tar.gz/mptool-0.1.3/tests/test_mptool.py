# -*- coding: utf-8 -*-

import cobra
import glob
import mptool as mpt
import numpy as np
import pytest


@pytest.fixture
def cobra_model_paths():
    return glob.glob('tests/models/e_coli_core*')


def test_load_cobra_model(cobra_model_paths):
    cobra_model = mpt.load_cobra_model(cobra_model_paths[0])
    assert isinstance(cobra_model, cobra.Model)


def test_load_cobra_models(cobra_model_paths):
    cobra_models = mpt.load_cobra_models(cobra_model_paths)
    assert len(cobra_models) == 3


def test_load_cobra_models_sbml(cobra_model_paths):
    cobra_models = mpt.load_cobra_models(cobra_model_paths,
                                         suffixes=('sbml', 'xml'))
    assert len(cobra_models) == 1


def test_load_cobra_models_json(cobra_model_paths):
    cobra_models = mpt.load_cobra_models(cobra_model_paths, suffixes=('json'))
    assert len(cobra_models) == 1


def test_load_cobra_models_mat(cobra_model_paths):
    cobra_models = mpt.load_cobra_models(cobra_model_paths, suffixes=('mat'))
    assert len(cobra_models) == 1


def test_save_load_set(tmpdir):
    path = tmpdir.join('test.txt').strpath
    s1 = set(['a', 'b', 'c'])
    mpt.save_set(s1, path)
    s2 = mpt.load_set(path)
    assert s1 == s2


def test_save_load_sets(tmpdir):
    path = tmpdir.join('test.txt').strpath
    s1 = set([frozenset(['a', 'b', 'c']), frozenset(['d', 'e', 'f'])])
    mpt.save_sets(s1, path)
    s2 = mpt.load_sets(path)
    assert s1 == s2


def test_save_load_bounds(tmpdir):
    path = tmpdir.join('test.txt').strpath
    b1 = {'a': (0, 1), 'b': (-1, 1)}
    mpt.save_bounds(b1, path)
    b2 = mpt.load_bounds(path)
    assert b1 == b2


@pytest.fixture
@pytest.mark.dependency(depends=['test_load_cobra_model'])
def cobra_model():
    cobra_model = mpt.load_cobra_model('tests/models/e_coli_core.json')
    cobra_model.reactions.BIOMASS_Ecoli_core_w_GAM.bounds = 0.1, 0.1
    cobra_model.reactions.ATPM.bounds = 0, 0
    return cobra_model


def test_create_lp(cobra_model):
    lp = mpt.create_lp(cobra_model)
    a1 = lp.getA().toarray()
    a2 = cobra.util.create_stoichiometric_matrix(cobra_model)
    b1 = {v.varName: (v.lb, v.ub) for v in lp.getVars()}
    b2 = {r.id: r.bounds for r in cobra_model.reactions}
    assert np.array_equal(a1, a2) and b1 == b2


@pytest.fixture
@pytest.mark.dependency(depends=['test_create_lp'])
def model(cobra_model):
    return mpt.create_lp(cobra_model)


def test_make_irreversible_cobra(cobra_model, subset):
    b1 = {r.id: r.bounds for r in cobra_model.reactions}
    new_subset = mpt.make_irreversible(cobra_model, subset=subset)
    b2 = {r.id: r.bounds for r in cobra_model.reactions}
    for x in subset:
        lb, ub = b1[x]
        if ub:
            assert b2[x] == (0, ub)
        if lb:
            assert b2[x + '_rev'] == (0, -lb)
    assert len(b2) == len(b1) + len(new_subset) - len(subset)


def test_make_irreversible_gurobi(model, subset):
    b1 = {v.varName: (v.lb, v.ub) for v in model.getVars()}
    new_subset = mpt.make_irreversible(model, subset=subset)
    b2 = {v.varName: (v.lb, v.ub) for v in model.getVars()}
    for x in subset:
        lb, ub = b1[x]
        if ub:
            assert b2[x] == (0, ub)
        if lb:
            assert b2[x + '_rev'] == (0, -lb)
    assert len(b2) == len(b1) + len(new_subset) - len(subset)
    

@pytest.fixture
@pytest.mark.dependency(depends=['test_save_load_bounds'])
def bounds(enum_id):
    return mpt.load_bounds('tests/data/' + enum_id + '_bounds.csv')


def test_fva(model, bounds):
    fva_bounds = mpt.fva(model)
    for k in fva_bounds:
        assert fva_bounds[k] == pytest.approx(bounds[k])


@pytest.fixture
def enum_id():
    return 'e_coli_core_20240923_152734142542'


@pytest.fixture
@pytest.mark.dependency(depends=['test_save_load_set'])
def subset(enum_id):
    return mpt.load_set('tests/data/' + enum_id + '_subset.txt')


@pytest.fixture
@pytest.mark.dependency(depends=['test_save_load_sets'])
def true_mps(enum_id):
    return mpt.load_sets('tests/data/' + enum_id + '_complete_mps.csv')


@pytest.fixture
@pytest.mark.dependency(depends=['test_save_load_sets'])
def true_mcs(enum_id):
    return mpt.load_sets('tests/data/' + enum_id + '_complete_mcs.csv')


def test_find_mps_direct(model, subset, bounds, true_mps):
    mps, mcs, complete = mpt.find_mps(model, subset=subset, method='direct',
                                      graph=False, bounds=bounds,
                                      tighten=False)
    assert mps == true_mps and mcs is None and complete


def test_find_mps_iterative(model, subset, bounds, true_mps, true_mcs):
    mps, mcs, complete = mpt.find_mps(model, subset=subset, method='iterative',
                                      graph=False, bounds=bounds,
                                      tighten=False)
    assert mps == true_mps and mcs == true_mcs and complete


def test_find_mps_iterative_graph(model, subset, bounds, true_mps, true_mcs):
    mps, mcs, complete = mpt.find_mps(model, subset=subset, method='iterative',
                                      graph=True, bounds=bounds,
                                      tighten=False)
    assert mps == true_mps and mcs == true_mcs and complete


def test_find_mps_iterative_random(model, subset, bounds, true_mps):
    mps, mcs, complete = mpt.find_mps(model, subset=subset, method='iterative',
                                      graph=False, random=True, bounds=bounds,
                                      tighten=False, max_t=5)
    assert mps <= true_mps and mcs is None and complete is None
