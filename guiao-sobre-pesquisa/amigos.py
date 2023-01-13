from constraintsearch import *

amigos = ["Andre", "Bernardo", "Claudio"]

def amigos_constaint(a1, coisas1, a2, coisas2):
    bic1, chap1 = coisas1
    bic2, chap2 = coisas2
    if bic1 == bic2 or chap1 == chap2:
        return False
    
    if bic1 == chap1 or bic2 == chap2 or a1 in coisas1 or a2 in coisas2 or (chap1 == "Claudio" and bic1 != "Bernardo") or (chap2 == "Claudio" and bic2 != "Bernardo"):
        return False

    return True


def make_constaint_graph(amigos):
    return { (a1, a2): amigos_constaint for a1 in amigos for a2 in amigos if a1!=a2}

def make_domain(amigos):
    return {a: [(bic, chap) for bic in amigos for chap in amigos] for a in amigos}
    
cs = ConstraintSearch(make_domain(amigos), make_constaint_graph(amigos))
print(cs.search())