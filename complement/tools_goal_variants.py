from tools import end, goal_pipeline, autfilt_no, autfilt_yes, cleanup, goal_det

tools = {
    # Default for experiments
    "no.goal#pit"     : goal_det + autfilt_no  + cleanup,
    "yes.goal#pit"    : goal_det + autfilt_yes + cleanup,
    # Othe goal variants (only with simplifications)
    "pure.yes": goal_det + autfilt_yes + cleanup,
    "ht.yes"  : goal_pipeline("piterman", "-ht") + autfilt_yes + cleanup, # history trees
    "eq.yes"  : goal_pipeline("piterman", "-eq") + autfilt_yes + cleanup, # local equivalency check
    "sp.yes"  : goal_pipeline("piterman", "-sp") + autfilt_yes + cleanup, # Simplify parity acceptance
    "ro.yes"  : goal_pipeline("piterman", "-ro") + autfilt_yes + cleanup, # Reduce transitions
    # ht variants
    "hteq.yes"  : goal_pipeline("piterman", "-ht -eq") + autfilt_yes + cleanup,
    "htsp.yes"  : goal_pipeline("piterman", "-ht -sp") + autfilt_yes + cleanup,
    "htro.yes"  : goal_pipeline("piterman", "-ht -ro") + autfilt_yes + cleanup,
    # eq variants
    "eqsp.yes"  : goal_pipeline("piterman", "-eq -sp") + autfilt_yes + cleanup,
    "eqro.yes"  : goal_pipeline("piterman", "-eq -ro") + autfilt_yes + cleanup,
    # spro
    "spro.yes"  : goal_pipeline("piterman", "-sp -ro") + autfilt_yes + cleanup,
    # 3 combinations
    "eqspro.yes"  : goal_pipeline("piterman", "-eq -sp -ro") + autfilt_yes + cleanup,
    "htspro.yes"  : goal_pipeline("piterman", "-ht -sp -ro") + autfilt_yes + cleanup,
    "hteqro.yes"  : goal_pipeline("piterman", "-ht -eq -ro") + autfilt_yes + cleanup,
    # all 4
    "hteqrosp.yes"  : goal_pipeline("piterman", "-ht -eq -ro -sp") + autfilt_yes + cleanup,
}