from tools import seminator, end

tools = {
    "best": seminator("best", ) + end,
    "spot#tgba": seminator("spot", "--via-tgba") + end,
    "pldi#tgba": seminator("pldi", "--via-tgba") + end,
    "spot#tba": seminator("spot", "--via-tba") + end,
    "pldi#tba": seminator("pldi", "--via-tba") + end,
    "spot#sba": seminator("spot", "--via-sba") + end,
    "pldi#sba": seminator("pldi", "--via-sba") + end,
    ## Other variants
    "entry.nopower"  : seminator("best", "--powerset-on-cut=0 --cut-on-SCC-entry") + end,
    "entry.power"    : seminator("best", "--powerset-on-cut=1 --cut-on-SCC-entry") + end,
    "always.nopower" : seminator("best", "--powerset-on-cut=0 --cut-always") + end,
    "always.power"   : seminator("best", "--powerset-on-cut=1 --cut-always") + end,
}