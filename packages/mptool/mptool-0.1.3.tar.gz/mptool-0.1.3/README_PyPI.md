# Enumeration and sampling of minimal pathways in metabolic (sub)networks

Minimal pathways (MPs) are minimal sets of reactions that need to be active (have non-zero flux) in a metabolic (sub)network to satisfy all constraints on the network as a whole [1]. They can also be defined as the set of *support-minimal* flux patterns from elementary flux vectors (EFVs) [2].

An MP can be found by direct minimization of a mixed-integer linear program (MILP) or by iterative minimization of multiple linear programs (LPs). Enumeration of MPs is implemented using both of these approaches, in the iterative case by computing minimal cut sets (MCSs) in a separate binary integer program (BIP) [3]. For iterative minimzation, enumeration can be accelerated by using a graph defined by the known MPs to predict unknown MPs, or it can be randomized to allow random sampling of MPs in cases where complete enumeration is inconvenient or infeasible.

## Installation


The minimal requirements (`cobra`, `gurobipy`, `networkx`, `numpy`, and `pytest`) are installed automatically when `mptool` is installed through pip:
```
pip install mptool
```
The [Gurobi Optimizer](https://www.gurobi.com/) (tested with versions ≥9.0.1)) needs to be installed separately (free academic licenses).

## Citation

If you use `mptool` for a scientific publication please cite [our paper](https://www.biorxiv.org/content/10.1101/2020.07.31.230177v2) [1].

## References

[1] O. Øyås and J. Stelling. "Scalable metabolic pathway analysis". *biorXiv* (2020).

[2] S. Klamt et al. "From elementary flux modes to elementary flux vectors: Metabolic pathway analysis with arbitrary linear flux constraints". *PLoS Computational Biology* 13.4 (2017).

[3] H.S. Song et al. "Sequential computation of elementary modes and minimal cut sets in genome-scale metabolic networks using alternate integer linear programming". *Bioinformatics* 33.15 (2017).

[4] Z.A. King et al. "BiGG Models: A platform for integrating, standardizing, and sharing genome-scale models" *Nucleic Acids Research* 44.D1 (2016).

[5] A. Noronha et al. "The Virtual Metabolic Human database: integrating human and gut microbiome metabolism with nutrition and disease" *Nucleic Acids Research* 47.D1 (2018).