tmp_name = "$LCW_TMP.in.hoa"
tmp_out = "$LCW_TMP.out.hoa"

roll_jar = "other_tools/roll-library/ROLL.jar"

goal_root = "other_tools/GOAL-20200107"
goal_bin = "$LCW_GOAL_BIN"

tgba = "ltl2tgba -D %f | "
sba  = "ltl2tgba -D %f | autfilt -B | "

save_to_file = f"cat > {tmp_name}"

autfilt_no  = f" && cat {tmp_out} > %O"
autfilt_yes = f" && autfilt --small --tgba {tmp_out} > %O"
cleanup = f" ;rm -f {tmp_name} {tmp_out}"


buechenic_cmd = f"java -jar {roll_jar} complement {tmp_name} -v 0 -table -syntactic -out {tmp_out}"
buechenic     = sba + save_to_file + " && " + buechenic_cmd


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
    "no.goal#pit"     : goal_det + autfilt_no  + cleanup,
    "yes.goal#pit"    : goal_det + autfilt_yes + cleanup,
    "no.goal#fri"     : fribourg + autfilt_no  + cleanup,
    "yes.goal#fri"    : fribourg + autfilt_yes + cleanup,
    # Buechenic
    "no.buechenic"    : buechenic + autfilt_no  + cleanup,
    "yes.buechenic"   : buechenic + autfilt_yes + cleanup,
    # Autfilt
    "no.autfilt"      : tgba + "autfilt --complement --tgba > %O",
    "no.autfilt_DPA"  : tgba + "autfilt --complement > %O",
    "yes.autfilt"     : tgba + "autfilt --complement --tgba --small > %O",
    "yes.autfilt_DPA" : tgba + "autfilt --complement --small > %O",
    # Seminator + sDBA complementation
    "yes.ncsb#spot" : seminator("spot", "--cut-always") + end,
    "no.ncsb#spot"  : seminator("spot", "--cut-always --postprocess-comp=0") + end,
    "yes.ncsb#pldi" : seminator("pldi", "--cut-always") + end,
    "no.ncsb#pldi"  : seminator("pldi", "--cut-always --postprocess-comp=0") + end,
    "yes.ncsb#best" : seminator("best", "--cut-always") + end,
    "no.ncsb#best"  : seminator("best", "--cut-always --postprocess-comp=0") + end,
}
benchmark_names = [f"{s}_{t}" for s in ["literature","random"] for t in ["det","sd","nd"]]
