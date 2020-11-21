#import owl_servers

make_tgba   = 'ltl2tgba --deterministic -f %f'
end         = 'autfilt -F $docas --small -H > %O' 
end         = '> %O' # saves result to file

end = '| autfilt --small --tgba > %O' # optimizes and saves result to file
def seminator_cmd(reductions=True, options="",optimalizations=True,version=""):
    if version == "":
        reductions = "--postprocess=1" if reductions else "--postprocess=0"
    else:
        reductions = "" if reductions else "-s0"
    konec = end if optimalizations else "| cat > %O"
    return f"{make_tgba} | seminator{version} {options} {reductions} {konec}"



def empc_cmd(special_transitions=False):
    special_transitions = '' if not special_transitions else '--ashu-slim-exploration-nonempty-breakpoint true'
    return f"docastom=`mktemp`;docas=`mktemp`;{make_tgba}>$docastom; java -jar ~/automaty/epmc-ashu-v7.jar formula2automaton --ashu-input-type hoa --ashu-input-file $docastom {special_transitions} --ashu-automaton-type slim --ashu-output-file $docas;  {end}"


def empc_cmd(special_transitions=False):
    special_transitions = '' if not special_transitions else '--ashu-slim-exploration-nonempty-breakpoint true'
    return f"rnd=$RANDOM;{make_tgba}>tomat$rnd.hoa; java -jar ~/automaty/epmc-ashu-v7.jar formula2automaton --ashu-input-type hoa --ashu-input-file tomat$rnd.hoa {special_transitions} --ashu-automaton-type slim --ashu-output-file epmc$rnd.hoa; cat epmc$rnd.hoa {end}"





def empc_cmd(special_transitions=False, version=11):
    special_transitions = '' if not special_transitions else '--ashu-slim-exploration-nonempty-breakpoint true'
    return f"rnd=$RANDOM;{make_tgba}>tomat$rnd.hoa; java -jar ~/automaty/epmc-ashu-v{version}.jar formula2automaton --ashu-input-type hoa --ashu-input-file tomat$rnd.hoa {special_transitions} --ashu-automaton-type slim --ashu-output-file epmc$rnd.hoa;autfilt --small --tgba -F epmc$rnd.hoa > %O"

def empc_cmd(special_transitions=False, no_epsilon=True, accepting=False, optimalizations=True ,version=11):
    # version 8 has --ashu-use-epsilon-transitions disabled by default 
    accepting = '' if not accepting else '--ashu-slim-exploration-special-accepting true'
    special_transitions = '' if not special_transitions else '--ashu-slim-exploration-nonempty-breakpoint true'
    end = "autfilt --small --tgba -F $docas > %O" if optimalizations else "cat $docas > %O"
    #no_epsilon = "--ashu-use-epsilon-transitions"+('' if not no_epsilon else ' true')
    return f"docastom=`mktemp`;docas=`mktemp`;{make_tgba}>$docastom; java -jar ~/automaty/epmc-ashu-v{version}.jar formula2automaton --ashu-input-type hoa --ashu-input-file $docastom {special_transitions} {accepting} --ashu-automaton-type slim --ashu-output-file $docas;autfilt --small --tgba -F $docas > %O"

def empc_cmd(special_transitions=False, no_epsilon=True, accepting=False, optimalizations=True ,version=11):
    # version 8 has --ashu-use-epsilon-transitions disabled by default 
    accepting = '' if not accepting else '--ashu-slim-exploration-special-accepting true'
    special_transitions = '' if not special_transitions else '--ashu-slim-exploration-nonempty-breakpoint true'
    end = "autfilt --small --tgba -F $docas > %O" if optimalizations else "cat $docas > %O"
    #no_epsilon = "--ashu-use-epsilon-transitions"+('' if not no_epsilon else ' true')
    return f"docastom=`mktemp`;docas=`mktemp`;{make_tgba}>$docastom; java -jar ~/automaty/epmc-ashu-v{version}.jar formula2automaton --ashu-input-type hoa --ashu-input-file $docastom {special_transitions} {accepting} --ashu-automaton-type slim --ashu-output-file $docas;{end}"
# sem_pipelines = {
#     "yes.seminator#def" : seminator_cmd(),
#     "no.seminator#def"  : seminator_cmd(reductions=False),
#     "yes.seminator#tgba": seminator_cmd(options="--via-tgba"),
#     "no.seminator#tgba" : seminator_cmd(reductions=False, options="--via-tba"),
#     "yes.seminator#tba" : seminator_cmd(options="--via-tgba"),
#     "no.seminator#tba"  : seminator_cmd(reductions=False, options="--via-tba"),
#     "yes.seminator#sba" : seminator_cmd(options="--via-sba"),
#     "no.seminator#sba"  : seminator_cmd(reductions=False, options="--via-sba"),
#     "yes.seminator-1-1" : seminator_cmd(version="-1.1"),
#     "no.seminator-1-1"  : seminator_cmd(reductions=False, version="-1.1"),
#     "yes.seminator-1-2" : seminator_cmd(version="-1.2"),
#     "no.seminator-1-2"  : seminator_cmd(reductions=False, version="-1.2"),
# }
    
    
sem_pipelines = {
    #"yes.seminator#def" : seminator_cmd(),
    #"no.seminator#def"  : seminator_cmd(reductions=False),
    #"yes.seminator#tgba": seminator_cmd(options="--via-tgba"),
    #"no.seminator#tgba" : seminator_cmd(reductions=False, options="--via-tba"),

    #"yes.seminator#tba" : seminator_cmd(options="--via-tgba"),
    #"no.seminator#tba"  : seminator_cmd(reductions=False, options="--via-tba"),
    #"yes.seminator#sba" : seminator_cmd(options="--via-sba"),
    #"no.seminator#sba"  : seminator_cmd(reductions=False, options="--via-sba"),
    "yes.seminator#slim": seminator_cmd(options="--slim --pure"),
    "yes.seminator#weakslim" : seminator_cmd( options="--slim --weak --pure"),
    "yes.empc#specialslim":empc_cmd(special_transitions=True),
    "yes.empc#slim":empc_cmd(),
    "yes.empc#specialslim#acc":empc_cmd(special_transitions=True, accepting=True),
    "yes.empc#slim#acc":empc_cmd(accepting=True),
    "no.seminator#slim": seminator_cmd(optimalizations=False, options="--slim --pure"),
    "no.seminator#weakslim" : seminator_cmd(optimalizations=False, options="--slim --weak --pure"),
    "no.empc#specialslim":empc_cmd(optimalizations=False, special_transitions=True),
    "no.empc#slim":empc_cmd(optimalizations=False),
    "no.empc#specialslim#acc":empc_cmd(optimalizations=False, special_transitions=True, accepting=True),
    "no.empc#slim#acc":empc_cmd(optimalizations=False, accepting=True),
}
#ahoj={
#     "no.empc#slim" : f"rnd=$RANDOM;{make_tgba}>tomat$rnd.hoa; java -jar ~/automaty/epmc-ashu-v7.jar formula2automaton --ashu-input-type hoa --ashu-input-file tomat$rnd.hoa --ashu-automaton-type slim --ashu-output-file epmc$rnd.hoa; cat epmc$rnd.hoa {end}",
    
    
    
    
#    "no.empc#slim" : f"docastom=`mktemp`;docas=`mktemp`;{make_tgba}>$docastom; java -jar ~/automaty/epmc-ashu-v7.jar formula2automaton --ashu-input-type hoa --ashu-input-file $docastom --ashu-automaton-type slim --ashu-output-file $docas;autfilt -F $docas --small -H {end}",
    
#}