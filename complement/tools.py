tmp_name = "$LCW_TMP.in.hoa"
tmp_out = "$LCW_TMP.out.hoa"

roll_jar = "other_tools/roll-library/ROLL.jar"

goal_root = "other_tools/GOAL-20200506"
goal_bin = "$LCW_GOAL_BIN"

tgba = "ltl2tgba -D %f | "
sba  = "ltl2tgba -D -B %f "

save_to_file = f" > {tmp_name}"

autfilt_no  = f"; err=$?; rm -f {tmp_name}; mv -f {tmp_out} %O; exit $err"
autfilt_yes = f" && autfilt --small --tgba {tmp_out} > %O; err=$?; rm -f {tmp_name} {tmp_out}; exit $err"


buechic_cmd = f"java -jar {roll_jar} complement {tmp_name} -v 0 -table -syntactic -out {tmp_out}"
buechic     = sba + save_to_file + " && " + buechic_cmd


def goal_cmd(algo, options=""):
    return f"{goal_bin} batch '$temp = complement -m {algo} {options} `echo {tmp_name}`; save -c HOAF $temp `echo {tmp_out}`;'"

def goal_pipeline(algo, options=""):
    return f"{sba} {save_to_file} && {goal_cmd(algo, options)}"

def seminator(algo, sem_options=""):
    return f"{tgba} seminator --complement={algo} {sem_options} "

fribourg = goal_pipeline("fribourg")
goal_det = goal_pipeline("piterman","-eq -sp")

simpl = " | autfilt --small --tgba "
end = ">%O"

tools = {
    # GOAL & Fribourg in GOAL
    "no.goal#pit"     : goal_det + autfilt_no ,
    "yes.goal#pit"    : goal_det + autfilt_yes,
    "no.goal#fri"     : fribourg + autfilt_no ,
    "yes.goal#fri"    : fribourg + autfilt_yes,
    # Buechic
    "no.roll"    : buechic + autfilt_no ,
    "yes.roll"   : buechic + autfilt_yes,
    # Autfilt
    "no.spot"      : tgba + "autfilt --complement --tgba > %O",
    "no.spot_DPA"  : tgba + "autfilt --complement > %O",
    "yes.spot"     : tgba + "autfilt --complement --tgba --small > %O",
    "yes.spot_DPA" : tgba + "autfilt --complement --small > %O",
    # Seminator + sDBA complementation
    "yes.seminator#spot" : seminator("spot", "--cut-always") + end,
    "no.seminator#spot"  : seminator("spot", "--cut-always --postprocess-comp=0") + end,
    "yes.seminator#pldi" : seminator("pldi", "--cut-always") + end,
    "no.seminator#pldi"  : seminator("pldi", "--cut-always --postprocess-comp=0") + end,
    "yes.seminator#best" : seminator("best", "--cut-always") + end,
    "no.seminator#best"  : seminator("best", "--cut-always --postprocess-comp=0") + end,
}
benchmark_names = [f"{s}_{t}" for s in ["literature","random"] for t in ["det","sd","nd"]]
