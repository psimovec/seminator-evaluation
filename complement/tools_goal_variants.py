from tools import end, goal_pipeline, autfilt_no, autfilt_yes, goal_det

tools = {
    # Default for experiments
    "no.goal#pit"     : goal_det + autfilt_no ,
    "yes.goal#pit"    : goal_det + autfilt_yes,
    # Othe goal variants (only with simplifications)
    "pure.yes": goal_det + autfilt_yes,
    "ht.yes"  : goal_pipeline("piterman", "-ht") + autfilt_yes, # history trees
    "eq.yes"  : goal_pipeline("piterman", "-eq") + autfilt_yes, # local equivalency check
    "sp.yes"  : goal_pipeline("piterman", "-sp") + autfilt_yes, # Simplify parity acceptance
    "ro.yes"  : goal_pipeline("piterman", "-ro") + autfilt_yes, # Reduce transitions
    # ht variants
    "hteq.yes"  : goal_pipeline("piterman", "-ht -eq") + autfilt_yes,
    "htsp.yes"  : goal_pipeline("piterman", "-ht -sp") + autfilt_yes,
    "htro.yes"  : goal_pipeline("piterman", "-ht -ro") + autfilt_yes,
    # eq variants
    "eqsp.yes"  : goal_pipeline("piterman", "-eq -sp") + autfilt_yes,
    "eqro.yes"  : goal_pipeline("piterman", "-eq -ro") + autfilt_yes,
    # spro
    "spro.yes"  : goal_pipeline("piterman", "-sp -ro") + autfilt_yes,
    # 3 combinations
    "eqspro.yes"  : goal_pipeline("piterman", "-eq -sp -ro") + autfilt_yes,
    "htspro.yes"  : goal_pipeline("piterman", "-ht -sp -ro") + autfilt_yes,
    "hteqro.yes"  : goal_pipeline("piterman", "-ht -eq -ro") + autfilt_yes,
    # all 4
    "hteqrosp.yes"  : goal_pipeline("piterman", "-ht -eq -ro -sp") + autfilt_yes,
}