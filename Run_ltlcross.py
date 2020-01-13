# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.3.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from ltlcross_wrapper import Modulizer
from tools import sem_pipelines
from owl_servers import OwlServerManager, get_ldba_pipeline

# %%
owl_m = OwlServerManager()
owl_m.new_server("owl#s", get_ldba_pipeline(mode="s"))
owl_m.new_server("owl#a", get_ldba_pipeline(mode="a"))

owl_pipelines = {}
for mode, cmd in owl_m.get_clients().items():
    owl_pipelines[f"yes.{mode}"] = f"{cmd} | autfilt --small --tgba > %O"
    owl_pipelines[f"no.{mode}"] = f"{cmd} > %O"

# %%
tools = sem_pipelines.copy()
tools.update(owl_pipelines)

# %%
for s in ["literature","random"]:
    m = Modulizer(tools, f"formulae/{s}_nd.ltl", 
                  name=f"{s}_nd", tmp_dir=f"data/{s}_nd.parts",
                  processes=6, timeout="30")
    m.run()
    !mv {s}_nd.* data

# %%
spot_pipeline = {"yes.ltl2tgba#det": "ltl2tgba -D -f %f | seminator > %O"}
tools = spot_pipeline.copy()
tools.update(owl_pipelines)

# %%
for s in ["literature","random"]:
    for t in ["det","sd"]:
        name = f"{s}_{t}"
        m = Modulizer(tools, f"formulae/{name}.ltl", 
                      name=name, tmp_dir=f"data/{name}.parts",
                      processes=6, timeout="120")
        m.run()
        !mv {name}* data

# %%
owl_m.terminate_all()
