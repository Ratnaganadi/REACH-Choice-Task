# -*- coding: utf-8 -*-
import os, sys, csv, random, math
import operator as oprt
from itertools import combinations_with_replacement, product, chain, izip, izip_longest
from random import shuffle, choice

sorted_products = ['3 * 5','5 * 2','4 * 5','4 * 2','2 * 2','5 * 5','7 * 2','3 * 3','3 * 2',
    '3 * 4','6 * 2','9 * 9','2 * 8','5 * 6','4 * 4','5 * 7','5 * 9','5 * 8','3 * 7','9 * 2',
    '6 * 6','6 * 3','3 * 9','4 * 9','7 * 4','8 * 9','7 * 7','6 * 4','8 * 4','7 * 9','8 * 3',
    '6 * 8','8 * 8','7 * 8','9 * 6','6 * 7']

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def drange(start, stop, step):
    r = start
    while r < stop:
    	yield r
    	r += step

def precision_and_scale(x):
    max_digits = 14
    int_part = int(abs(x))
    magnitude = 1 if int_part == 0 else int(math.log10(int_part)) + 1
    if magnitude >= max_digits:
            return (magnitude, 0)
    frac_part = abs(x) - int_part
    multiplier = 10 ** (max_digits - magnitude)
    frac_digits = multiplier + int(multiplier * frac_part + 0.5)
    while frac_digits % 10 == 0:
            frac_digits /= 10
    scale = int(math.log10(frac_digits))
    return (magnitude + scale, scale)

def count_carries(exp):
    if '+' in exp:
        n1, n2 = exp.split()[0], exp.split()[-1]
        n1 = n1.replace('.','')
        n2 = n2.replace('.','')
        carry, answer = 0, 0
        for one,two in izip_longest(n1[::-1], n2[::-1], fillvalue='0'):
            carry = int(((int(one)+int(two)+carry)//10)>0)
            answer += ((int(one)+int(two)+carry)//10)>0
            carry += ((int(one)+int(two)+carry)//10)>0
        return answer

    elif '-' in exp:
        base=10
        lhs = exp.split()[0]; lhs = [int(lhs[i]) for i in range(len(lhs))]
        rhs = exp.split()[-1]; rhs = [int(rhs[i]) for i in range(len(rhs))]
        lhs = lhs.replace('.','')
        rhs = rhs.replace('.','')
        carries = 0
        length = max(len(lhs), len(rhs))
        lhs = [0 for i in range(len(lhs), length)] + lhs;
        rhs = [0 for i in range(len(rhs), length)] + rhs;
        for i in range(1, len(lhs) + 1):
            difference = lhs[-i] - rhs[-i]
            if difference < 0:
                carries += 1
                j = i + 1
                while j <= length:
                    lhs[-j] = (lhs[-j] + (base - 1)) % base
                    if lhs[-j] != base - 1:
                        break
                    else:
                        j = j + 1
        return carries


def get_pseudo_random_order(lst):
    order = range(len(lst))
    
    operator_list = [exp.split()[1] for exp in lst]
    operator_tuples = [(i, op) for i, op in enumerate(operator_list)]
    operators = list(set(operator_list))
    count = {}
    separated_ops = {}
    for o in operators: 
        count[o] = operator_list.count(o)
        separated_ops[o] = [tup for tup in operator_tuples if tup[1]==o]
        shuffle(separated_ops[o])
    
    long_op = max(count.iteritems(), key=oprt.itemgetter(1))[0]
    shuffle(separated_ops[long_op])
    separated_ops[long_op] = separated_ops[long_op][:min(count.values())]

    interleaved_tuples = []
    for i in range(len(separated_ops.values()[0])):
        for o in operators: interleaved_tuples.append(separated_ops[o][i])
    new_tuples = []
    for items in chunks(interleaved_tuples, 3):
        shuffle(items)
        new_tuples.extend(items)
    
    return [tup[0] for tup in new_tuples]

def longest_streak(expressions):
    longest = 0
    for i,exp in enumerate(expressions):
        if i==0: streak=1; continue
        if exp.split()[1] == expressions[i-1].split()[1]: streak+=1
        else: 
            if streak>longest: longest=streak
            streak=1
    return longest

def target_plus_minus(root, addends, invalid, secondary_addends=None):
    for addend in sorted(addends, key=lambda k: random.random()):
        res = root + addend
        if res>0 and res not in invalid: return res
    if secondary_addends:
        for addend in sorted(secondary_addends, key=lambda k: random.random()):
            res = root + addend
            if res>0 and res not in invalid: return res
    sys.exit("could not find a positive response not qual to the target for root %d, addends: %s, invalid: %s, and secondary addends: %s" %(root, repr(addends), repr(invalid), repr(secondary_addends)))

def create_expressions(num_range, operators):
    all_pairs = list(combinations_with_replacement(num_range, 2))
    for i in range(len(all_pairs)):
        all_pairs[i] = sorted(list(all_pairs[i]), key=lambda k: random.random())
    
    all_expressions = []
    for o in operators:
        if o=='-':
            all_expressions.extend(['{:.{}f} {} {:.{}f}'.format(max(p),precision_and_scale(max(p))[1],o,min(p),precision_and_scale(min(p))[1]) for p in all_pairs])
        else: all_expressions.extend(['{:.{}f} {} {:.{}f}'.format(p[0],precision_and_scale(p[0])[1], o, p[1],precision_and_scale(p[1])[1]) for p in all_pairs])
    return all_expressions

def create_product_expressions(num_set1, num_set2, operators):
    all_pairs = list(product(num_set1, num_set2))
    for i in range(len(all_pairs)):
        all_pairs[i] = sorted(list(all_pairs[i]), key=lambda k: random.random())
        
    all_expressions = []
    for o in operators:
        if o=='-':
            all_expressions.extend(['%d %s %d'%(max(p), o, min(p)) for p in all_pairs])
        else: all_expressions.extend(['%d %s %d'%(p[0], o, p[1]) for p in all_pairs])
    print 'created %d expressions' %len(all_expressions)
    return all_expressions

def convert_to_division_expressions(expressions):
    products = [eval(exp) for exp in expressions]
    new_expressions = []
    for exp,prd in zip(expressions,products):
        new_expressions.append('%d / %s' %(prd, exp.split()[0]))
        new_expressions.append('%d / %s' %(prd, exp.split()[-1]))
    return list(set(new_expressions))

def separate_carrying(expressions):
    non_carrying = list(expressions)
    carrying = []
    for exp in expressions:
        if count_carries(exp):
            non_carrying.remove(exp)
            carrying.append(exp)
    return carrying, non_carrying
    
def create_row(all_expressions, difficulty, max_stims, label):
    expressions = []
    targets = []
    foils1 = []
    foils2 = []
    foils3 = []
    max_target = max([eval(exp) for exp in all_expressions])
    if len(all_expressions)>500: all_expressions=sorted(all_expressions, key=lambda k: random.random())[:100]
    for exp in all_expressions:
        if eval(exp)<1: continue 
        target = eval(exp)
    
        if exp.split()[1] in ['+','-'] and '.' not in exp.split()[0]:
            if (float(exp.split()[0])>9 and float(exp.split()[-1])>9) and target>20:
                foil1 = target + choice([-10,10])
                foil2 = target_plus_minus(root=target, addends=[int(round(target*0.1)), int(round(target*-0.1))], invalid=[target, foil1])
                foil3 = target_plus_minus(root=foil2, addends=[-10,10], secondary_addends=[-20,20], invalid=[target, foil1, foil2])
            else:
                foil1 = target_plus_minus(root=target, addends=[-2,-1,1,2], invalid=[target])
                foil2 = target_plus_minus(root=target, addends=[-4,-3,3,4], invalid=[target, foil1])
                foil3 = target_plus_minus(root=target, addends=[-6,-5,5,6], invalid=[target, foil1, foil2])
        elif exp.split()[1] in ['+','-'] and '.' in exp.split()[0]:
            first = exp.split()[0]
            if len(first.split('.')[-1])==1:
                foil1 = target_plus_minus(root=target, addends=[-1,1], invalid = [target])
                foil2 = target_plus_minus(root=target, addends=list(drange(-0.9,-0.1,0.1))+list(drange(0.1,0.9,0.1)), invalid=[target, foil1])
                foil3 = target_plus_minus(root=foil2, addends=[-1,1], invalid=[target, foil1, foil2])
            elif len(first.split('.')[-1])==2:
                foil1 = target_plus_minus(root=target, addends=[-0.1,0.1], invalid = [target])
                foil2 = target_plus_minus(root=target, addends=list(drange(-0.09,-0.01,0.01))+list(drange(0.01,0.09,0.01)), invalid=[target, foil1])
                foil3 = target_plus_minus(root=foil2, addends=[-0.1,0.1], invalid=[target, foil1, foil2])
        elif exp.split()[1]=='*':
            if "10" in [exp.split()[0], exp.split()[-1]]:
                foil1 = target_plus_minus(root=target, addends=[-10,10], invalid=[target])
                foil2 = target_plus_minus(root=target, addends=[-20,20], invalid=[target, foil1])
                foil3 = target_plus_minus(root=target, addends=[-30,30], invalid=[target, foil1, foil2])
            elif int(exp.split()[0])>15 or int(exp.split()[-1])>15:
                foil1 = target_plus_minus(root=target, addends=[-10,10], invalid=[target])
                factors = [int(exp.split()[0]), int(exp.split()[-1])]
                foil2 = target_plus_minus(root=target, addends=[-1*min(factors), min(factors)], invalid=[target, foil1])
                foil3 = target_plus_minus(root=foil2, addends=[-10,10], secondary_addends=[-20,20], invalid=[target, foil1, foil2])
            elif target>10:
                factors = [int(exp.split()[0]), int(exp.split()[-1])]
                foil1 = target_plus_minus(root=target, addends=[-1*min(factors), min(factors)], invalid=[target])
                foil2 = target_plus_minus(root=target, addends=[-2*min(factors), 2*min(factors)], invalid=[target, foil1])
                foil3 = target_plus_minus(root=target, addends=[-1*max(factors), max(factors)], invalid=[target, foil1, foil2])
            else:
                foil1 = target_plus_minus(root=target, addends=[-2,-1,1,2], invalid=[target])
                foil2 = target_plus_minus(root=target, addends=[-4,-3,3,4], invalid=[target, foil1])
                foil3 = target_plus_minus(root=target, addends=[-6,-5,5,6], invalid=[target, foil1, foil2])
            exp = exp.replace('*','x')
        elif exp.split()[1]=='/':
            if exp.split()[0]==exp.split()[-1]:
                foil1 = int(exp.split()[0])
                foil2 = target_plus_minus(root=target, addends=[-2,-1,1,2], invalid=[target, foil1]+range(max_target+1,max_target+4))
                foil3 = target_plus_minus(root=foil1, addends=[-2,-1,1,2], invalid=[target, foil1, foil2]+range(max_target+1,max_target+4))
            else:
                foil1 = target_plus_minus(root=target, addends=[-1,1], invalid=[target]+range(max_target+1,max_target+4))
                foil2 = target_plus_minus(root=target, addends=[-2,2], invalid=[target, foil1]+range(max_target+1,max_target+4))
                foil3 = target_plus_minus(root=target, addends=[-3,3], invalid=[target, foil1, foil2]+range(max_target+1,max_target+4))
            exp = exp.replace('/',u'*div')
    
        expressions.append(exp)
        targets.append('{:.{}f}'.format(target, precision_and_scale(target)[1]))
        foils1.append('{:.{}f}'.format(foil1, precision_and_scale(foil1)[1]))
        foils2.append('{:.{}f}'.format(foil2, precision_and_scale(foil2)[1]))
        foils3.append('{:.{}f}'.format(foil3, precision_and_scale(foil3)[1]))
    
    if len(list(set([exp.split()[1] for exp in all_expressions])))==1:
        pseudo_order = range(len(expressions)); shuffle(pseudo_order)
    else: pseudo_order = get_pseudo_random_order(expressions)
    expressions = [expressions[i] for i in pseudo_order]
    targets = [targets[i] for i in pseudo_order]
    foils1 = [foils1[i] for i in pseudo_order]
    foils2 = [foils2[i] for i in pseudo_order]
    foils3 = [foils3[i] for i in pseudo_order]
    
    if len(expressions)>max_stims:
        expressions = expressions[:max_stims]
        targets = targets[:max_stims]
        foils1 = foils1[:max_stims]
        foils2 = foils2[:max_stims]
        foils3 = foils3[:max_stims]
    
    outrow = {'Difficulty': difficulty, 'Stimulus': expressions, 'Correct': targets,
        'Foil1': foils1, 'Foil2': foils2, 'Foil3': foils3, 'Label': label}
    writer.writerow(outrow)

difficulty=1

# create file to write
out_file= open('../math_stims_multiplication.csv', 'w')
fieldnames=['Difficulty','Stimulus','Correct','Foil1','Foil2','Foil3','Label']
headers = dict((n,n) for n in fieldnames)
writer = csv.DictWriter(out_file,fieldnames=fieldnames, lineterminator= '\n')
writer.writerow(headers)


# Generate Math Stimuli


# Multiplication by 1s
all_expressions = create_product_expressions(num_set1=[1], num_set2=range(1,10), operators=['*'])
create_row(all_expressions=all_expressions, difficulty=difficulty, max_stims=16, label='Multiplication by 1s up to 9')
difficulty+=1

# Multiplication by 10s
all_expressions = create_product_expressions(num_set1=[10], num_set2=range(1,11), operators=['*'])
create_row(all_expressions=all_expressions, difficulty=difficulty, max_stims=16, label='Multiplication by 10s up to 10')
difficulty+=1

product_sets = list(chunks(sorted_products, len(sorted_products)/3))
# Mixed Multiplication Level 1
create_row(product_sets[0], difficulty=difficulty, max_stims=16, label='Mixed Multiplication Level 1')
difficulty+=1

# Multiplication by 1s
all_expressions = create_product_expressions(num_set1=[1], num_set2=range(10,31), operators=['*'])
create_row(all_expressions=all_expressions, difficulty=difficulty, max_stims=16, label='Multiplication by 1s up to 30')
difficulty+=1

# Multiplication by 10s
all_expressions = create_product_expressions(num_set1=[10], num_set2=range(10,31), operators=['*'])
create_row(all_expressions=all_expressions, difficulty=difficulty, max_stims=16, label='Multiplication by 10s up to 30')
difficulty+=1

# Mixed Multiplication Level 2
create_row(product_sets[1], difficulty=difficulty, max_stims=16, label='Mixed Multiplication Level 2')
difficulty+=1

# Mixed Multiplication Level 3
create_row(product_sets[2], difficulty=difficulty, max_stims=16, label='Mixed Multiplication Level 3')
difficulty+=1

# Multiplication of 2s with 13-30
all_expressions = create_product_expressions(num_set1=[2], num_set2=range(13,20)+range(21,30), operators=['*'])
create_row(all_expressions=all_expressions, difficulty=difficulty, max_stims=16, label='Multiplication by 2s up to 30')
difficulty+=1

# Mixed 2-digit by 1-digit multiplication
num_set2 = range(13,100)
for num in drange(15,100,5): num_set2.remove(num)
all_expressions = create_product_expressions(num_set1=range(3,10), num_set2=num_set2, operators=['*'])
create_row(all_expressions=all_expressions, difficulty=difficulty, max_stims=16, label='Mixed 2-digit by 1-digit multiplication')
difficulty+=1