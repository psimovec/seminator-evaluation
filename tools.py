#import owl_servers

make_tgba   = 'ltl2tgba --deterministic -f %f'
end         = ' > %O' # saves result to file

def seminator_cmd(reductions=True, options="", version=""):
    if version == "":
        reductions = "--postprocess=1" if reductions else "--postprocess=0"
    else:
        reductions = "" if reductions else "-s0"
    return f"{make_tgba} | seminator{version} {options} {reductions} {end}"
        
sem_pipelines = {
    "yes.seminator#def" : seminator_cmd(),
    "no.seminator#def"  : seminator_cmd(reductions=False),
    "yes.seminator#tgba": seminator_cmd(options="--via-tgba"),
    "no.seminator#tgba" : seminator_cmd(reductions=False, options="--via-tba"),
    "yes.seminator#tba" : seminator_cmd(options="--via-tgba"),
    "no.seminator#tba"  : seminator_cmd(reductions=False, options="--via-tba"),
    "yes.seminator#sba" : seminator_cmd(options="--via-sba"),
    "no.seminator#sba"  : seminator_cmd(reductions=False, options="--via-sba"),
    "yes.seminator-1-1" : seminator_cmd(version="-1.1"),
    "no.seminator-1-1"  : seminator_cmd(reductions=False, version="-1.1"),
    "yes.seminator-1-2" : seminator_cmd(version="-1.2"),
    "no.seminator-1-2"  : seminator_cmd(reductions=False, version="-1.2"),
}
        