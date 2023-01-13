#encoding: utf8

# YOUR NAME: Tiago Gomes Carvalho
# YOUR NUMBER: 104142

# COLLEAGUES WITH WHOM YOU DISCUSSED THIS ASSIGNMENT:
# - Raquel Paradinha 102491

import itertools

from bayes_net import *
from constraintsearch import *
from semantic_network import *


class MySN(SemanticNetwork):

    def __init__(self):
        SemanticNetwork.__init__(self)

    def is_object(self,user,obj):
        if obj in [d.relation.entity1 for d in self.query_local(user=user) if isinstance(d.relation, Association) and d.relation.card == None]:
            return True
        
        if obj in [d.relation.entity2 for d in self.query_local(user=user) if isinstance(d.relation, Association) and d.relation.card == None]:
            return True
        
        if obj in [d.relation.entity1 for d in self.query_local(user=user) if isinstance(d.relation, Member)]:
            return True
        
        return False

    def is_type(self,user,type):
        delc = [d.relation.entity1 for d in self.query_local(user=user) if isinstance(d.relation, Subtype)]
        delc += [d.relation.entity1 for d in self.query_local(user=user) if isinstance(d.relation, Association) and d.relation.card != None]
        delc += [d.relation.entity2 for d in self.query_local(user=user) if isinstance(d.relation, Association) and d.relation.card != None]
        
        if type in set(delc):
            return True
        
        return False

    def infer_type(self,user,obj):
        delc = [d for d in self.query_local(user=user,e1=obj) if isinstance(d.relation, Member)]
        if delc != []:
            return delc[0].relation.entity2

        for assoc in [d.relation.name for d in self.query_local(user=user,e1=obj) if isinstance(d.relation, Association) and d.relation.card == None]:
            for a in [d.relation.name for d in self.query_local(user=user,rel=assoc) if isinstance(d.relation, Association) and d.relation.card != None]:
                sign = self.infer_signature(user=user,assoc=a)
                if sign != None:
                    return sign[0]
                    
        for assoc in [d.relation.name for d in self.query_local(user=user,e2=obj) if isinstance(d.relation, Association) and d.relation.card == None]:
            for a in [d.relation.name for d in self.query_local(user=user,rel=assoc) if isinstance(d.relation, Association) and d.relation.card != None]:
                sign = self.infer_signature(user=user,assoc=a)
                if sign != None:
                    return sign[1]
        
        if self.is_object(user, obj):
            return '__unknown__'

        return None
 
    def infer_signature(self,user,assoc):
        delc = [d for d in self.query_local(user=user,rel=assoc)]
        if delc == []:
            return None

        for d in delc:
            if isinstance(d.relation, Association) and d.relation.card != None:
                return (d.relation.entity1, d.relation.entity2)

        tipos_e1 = set()
        for d in delc:
            tipos_e1.add(self.infer_type(user, d.relation.entity1))
        
        if len(tipos_e1) != 1:
            e1 = '__unknown__'
        else:
            e1 = tipos_e1.pop()
        
        tipos_e2 = set()
        for d in delc:
            tipos_e2.add(self.infer_type(user, d.relation.entity2))
        if len(tipos_e2) != 1:
            e2 = '__unknown__'
        else:
            e2 = tipos_e2.pop()

        return (e1, e2)
    


class MyBN(BayesNet):

    def __init__(self):
        BayesNet.__init__(self)
        # ADD CODE HERE IF NEEDED
        pass

    def markov_blanket(self,var):
        markov_blanket = []
        
        for mtrue, _, _ in self.dependencies[var]:
            markov_blanket += mtrue
        
        for v, dependencies in self.dependencies.items():
            if v == var:
                continue
            for mtrue, _, _ in dependencies:
                if var in mtrue:
                    markov_blanket.append(v)
        
        for child in [child for child, dependencies in self.dependencies.items() if any(var in mtrue for mtrue, _, _ in dependencies) and v != var]:
            for mtrue, _, _ in self.dependencies[child]:
                if var not in mtrue:
                    markov_blanket += mtrue
        
        return list(set(markov_blanket))


class MyCS(ConstraintSearch):

    def __init__(self,domains,constraints):
        ConstraintSearch.__init__(self,domains,constraints)
        pass

    def propagate(self,domains,var):
        def getEdges(var):
            edges = []
            for edge in self.constraints:
                if edge[1] == var:
                    edges.append(edge)
            return edges

        def updateDomain(src, dest, constr):
            updatedDomain = []
            for value in domains[src]:
                for y in domains[dest]:
                    if constr(src, value, dest, y):
                        updatedDomain.append(value)
                        break
            return updatedDomain

        updatedDomain = []
        edges = getEdges(var)

        while edges:
            src, dest = edges.pop(0)
            constraint = self.constraints[src, dest]
            updatedDomain = updateDomain(src, dest, constraint)
            if len(updatedDomain) < len(domains[src]):
                domains[src] = updatedDomain
                edges += getEdges(src)


    def higherorder2binary(self,ho_c_vars,unary_c):
        def makeConstaintAuxVar(i):
            return lambda a, auxVal, v, varVal: varVal == auxVal[i] and unary_c(auxVal)

        def makeConstaintVarAux(i):
            return lambda v, varVal, a, auxVal: varVal == auxVal[i] and unary_c(auxVal)

        def updateDomains():
            product = itertools.product(*[self.domains[var] for var in ho_c_vars])
            domains = []
            for x in product:
                if unary_c(x):
                    domains.append(tuple(x))
            return domains

        auxVariable = "".join(ho_c_vars)
        self.domains[auxVariable] = updateDomains()

        for i in range(len(ho_c_vars)):
            self.constraints[auxVariable, ho_c_vars[i]] = makeConstaintAuxVar(i)
            self.constraints[ho_c_vars[i], auxVariable] = makeConstaintVarAux(i)
