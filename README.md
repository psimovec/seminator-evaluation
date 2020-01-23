# Seminator 2 evaluation

This repository stores scripts and data to evaluate the performance of [Seminator 2](https://github.com/mklokocka/seminator/releases/tag/v2). There is a [docker image](https://github.com/adl/seminator-docker) that is prepared to run this evaluation. It contains a copy of Seminator, Spot, Owl, GOAL, Roll, and Jupyter besides these scripts and data.

## Content
We provide evaluation of Seminator performing 2 tasks:
1. conversion of _non-deterministic generalized Büchi automata (TGBA)_ into _semi-deterministic generalized Büchi automata_ (also known as limit-deterministic Büchi automata).
2. complementation of Büchi automata

For both tasks, we start from LTL formulas that we convert to TGBA. The reasons behind this are that (1.) LTL is a convenient formalism for describing properties, (2.) `ltl2ldba` can take only LTL fromulas as input and it is basically the only relevant competitor for Seminator for conversion of properties to sDBA.

## Requirements
In order to reproduce the results, your mashine has to fullfill several requirements that are listed below. Or, you can use the [docker image](https://github.com/adl/seminator-docker) which meets all the requirements.
* [Jupyter](https://jupyter.org/)
* [ltlcross_wrapper 0.7](https://github.com/xblahoud/ltlcross_wrapper/tag/v0.7) that is a Python wrapper around `ltlcross` from Spot.
* [pandas 0.24+](https://pandas.pydata.org/)
* [Seminator 2](https://github.com/mklokocka/seminator/releases/tag/v2) has to be installed in your `PATH` as `seminator`
* [Seminator 1.1](https://github.com/mklokocka/seminator/releases/tag/v1.1.0) has to be installed in your `PATH` as `seminator-1.1`
* [Seminator 1.2](https://github.com/mklokocka/seminator/releases/tag/v1.2.0) has to be installed in your `PATH` as `seminator-1.2`
* [Spot](https://spot.lrde.epita.fr/) with Python bindings has to be installed in your `PATH`
* [Owl library](https://owl.model.in.tum.de/) version 19.06.03 has to be installed and at least the commands `owl-server` and `owl-client` has to be accessible in your `PATH`.
* other complementation tools should ge installed in the directory `coplement/other_tools`:
  - [ROLL](https://iscasmc.ios.ac.cn/roll/doku.php)
  - [GOAL v. 20200107](http://goal.im.ntu.edu.tw/release/GOAL-20200107.zip) with the [Fribourg plugin](http://goal.im.ntu.edu.tw/wiki/doku.php?id=goal:extensions#fribourg_construction).

## Formulas
We use 2 sources of formulas: random formulas and formulas that appeared in previous benchmarks. We further divide these formulas into categories based on type of automata that Spot's `ltl2tgba` produces from the corresponding formula. We have 3 types:
 * `det` : `ltl2tgba` already creates automaton, that is deterministic
 * `sd`  : `ltl2tgba` produces automaton, that is not deterministic, but it is already semi-deterministic
 * `nd`  : `ltl2tgba` produces automaton that is not semi-deterministic
 
You can find the sets of formulas in the directory [formulae](formulae) and you can see how they were generated (or regenerated them) in the notebook [Formulae](Formulae.ipynb).

## LTL to semi-deterministic automata benchmarks
The comparison compares the performance of Seminator 2 to earlier versions of Seminator (1.1, and 1.2) and to `ltl2ldgba` from Owl. We present only data, where Spot's simplification routines were applied to _all_ automata, including those produced by Owl. In defaults settings, these simplification routines are used in Seminator, while are not used in Owl.

The data can be recomputed using the notebook [semi-determinization/Run_ltlcross.ipynb](semi-determinization/Run_ltlcross.ipynb) and are already precomputed in this repository (in directory `semi-determinization/data`). However, the running times for these benchmarks are small so takes only about 2 minutes to recompute them.

We visualize the data using `ltlcross_wrapper` in 3 notebooks.
* [semi-determinization/Results-owl-best.ipynb](semi-determinization/Results-owl-best.ipynb) compares 3 versions of Seminator (1.1, 1.2, and 2) with Owl on formulas such that `ltl2tgba` translates them into automaton that is not semi-deterministic. The `owl-best` stands for the following: we have run Owl with both `ltl2ldgba -a` and `ltl2ldgba -s` applied the Spot's simplifications on both of them, and choose the better result as the best automaton that we are able to produce using Owl.
* [semi-determinization/Results-owl-best-sd.ipynb](semi-determinization/Results-owl-best-sd.ipynb) compares Seminator 2 with Owl (in the same setting as above) on formulas such that `ltl2tgba` produces automaton that is already semi-deterministic and thus Seminator does not do much work. Again, we use the _best-for-Owl_ approach.
* [semi-determinization/Results.ipynb](semi-determinization/Results.ipynb) (not used in the paper) Same as [semi-determinization/Results-owl-best.ipynb](semi-determinization/Results-owl-best.ipynb) but we now use only the default settings for Owl and apply Spot's simplification routines on it to get the automata for Owl.

## Complementation
Notebooks and data in directory `complement` benchmark the performance of complementation implemented in Seminator to other complementation algorithms. The precomputed data are stored in the directory `complement/data`. You can recompute the data using the notebook [complement/Run_ltlcross](complement/Run_ltlcross.ipynb). 

However, compute all the presented results takes **several hours**.
The data are already precomputed in the directory `complement/data` so you can explore them using these notebooks:
* [complement/Results_BA](complement/Results_BA.ipynb), the notebook used to produce plots & tables presented in the paper.
* [complement/Seminator_variants](complement/Seminator_variants.ipynb) gives more insight into how different configuration of the first step (converting nondeterministic automaton into semi-deterministic one) affects the result. It also shows how often is each pipeline of seminator successfull in being chosen as the best one (data stored in `complement/data.seminator_variants`).
* [complement/GOAL-variants](complement/GOAL-variants.ipynb) served as a basis to choose the best possible configuration of the complementation in GOAL (data stored in `complement/data.goal_variants`).