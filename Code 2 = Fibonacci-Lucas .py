#!/usr/bin/env python
# coding: utf-8

# In[17]:


import sympy as sp
x, n, k = sp.symbols("x n k")

def v(n):
    return x**n - (-1)**n*x**-n

def u(n):
    return x**n + (-1)**n*x**-n

def function(expr):
    expansion = sp.expand(expr)
    if isinstance(expansion, sp.Pow):
        raise Exception("Failed to expand given expression:", expansion)

    # analyse all the powers of x available
    defaulters = []
    terms_with_powers = [[],[]]
    twp_constants = [[],[]]

    output = sp.S.Zero

    if expansion.is_constant():
        args = [expansion]
    else:
        args = expansion.args
    for i in args:
        var = 0 if i.subs({x:0}) == 0 else 1
        if i.is_constant():
            output += i
        elif isinstance(i, sp.Mul) and not isinstance(i/i.subs({x:1}), sp.Pow):
            terms_with_powers[var].append(1 if i.subs({x:0}) == sp.S.Zero else -1)
            twp_constants[var].append(i.subs({x:1}))
        elif isinstance(i, sp.Symbol):
            terms_with_powers[var].append(1)
            twp_constants[var].append(1)
        elif isinstance(i, sp.Pow):
            terms_with_powers[var].append(i.args[1])
            twp_constants[var].append(1)
        elif isinstance(i, sp.Mul):
            constant = i.subs({x:1})
            terms_with_powers[var].append((i/constant).args[1])
            twp_constants[var].append(constant)

        else:
            defaulters.append(i)
    if defaulters != []:
        raise Exception("Failed to comprehend these terms:" + str(defaulters))

    # start applying relations available

    used_powers = []
    for i in terms_with_powers[0]:
        if -i in terms_with_powers[1]:
            used_powers.append(abs(i))
            positive = twp_constants[0][terms_with_powers[0].index(i)]
            negative = twp_constants[1][terms_with_powers[1].index(-i)]
            if positive == negative:
                output += positive*sp.symbols('V_'+str(i))
            elif positive == -negative:
                output += positive*sp.symbols('U_'+str(i))
    if set(used_powers) != set(terms_with_powers[0]):
        message = "All terms could not be converted to U_n and V_n \n terms_with_powers: " +                   str(terms_with_powers)+"\n used_powers: "+str(used_powers)
        raise Exception(message)

    return output

# Enter your input here in the form of u(2)**3*v(2)**2
input_expr = ""

# This code gets the output and presents it.
# Output of the fucntion is stored in answer.
answer = function(eval(input_expr, {'u':u, 'v':v}))
print("input expression:", input_expr, "\n\nOutput:", answer)


# In[ ]:




