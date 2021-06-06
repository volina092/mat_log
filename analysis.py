from itertools import *

add_only = False
multi_only = False

def right_symbols(line):
    global add_only
    global multi_only
    line = line.replace('\n', '')
    line = line.replace('\t', '')
    line = line.replace(' ', '')
    for letter in line:
        if not letter in ['1', '0', 'x', '\'', '=', '*', '(', ')', '+']:
            return 'error'
        if 'xx' in line or '\'x' in line: return 'error'
    if not line.count('='):
        if line.count('+') and not line.count('*'):
            multi_only = True
            add_only = False
        elif line.count('*') and not line.count('+'):
            add_only = True
            multi_only = False
        else:
            add_only = False
            multi_only = False
            
    return line   

def simplier(line):
    find_streak = False
    parts = []
    for i in range(len(line)):
        if line[i] == 'x': find_streak = True
        elif line[i] == '\'' and not find_streak: return 'error'
        elif find_streak and line[i] != "\'":
            parts.append('x')
            find_streak = False
        elif i == len(line) - 1 and line[i] == '\'': parts.append('x')
        elif find_streak and line[i] == "\'": continue
        #if find_streak and i == (len(line) - 1) and line[i] == '\'': parts.append('x')
        if line[i] == '0' or line[i] == '1': parts.append('1')
        elif line[i] == '*' or line[i] == '+': parts.append('+')
        elif line[i] in ['(', ')', '=']: parts.append(line[i])
        #elif line[i] != '\'' and line[i] != 'x': parts.append(line[i])
    if line[-1] == 'x' and len(line) == 1: parts.append('x')
    elif line[-1] == 'x' and line[-2] != 'x': parts.append('x')
    new_line = ''.join(parts)
    if 'xx' in new_line:
        return 'error'
    if 'xx' in new_line or '1x' in new_line or 'x1' in new_line or '11' in new_line:
        return 'error'
    if '++' in new_line or '+=' in new_line or '=+' in new_line or '==' in new_line:
        return 'error'
    for i in range(len(new_line)-1):
        if new_line[i] == new_line[i+1] and new_line[i] not in ['(', ')']:
            return 'error'
        if new_line[i] == '1' and new_line[i+1] == 'x': return 'error'
        if new_line[i] == 'x' and new_line[i+1] == '1': return 'error' 
    return new_line

def plus_right(line):
    if line[0] == '+' or line[len(line) - 1] == '+': return 'error'
    for i in range(len(line)):
        if line[i] == '+' and (line[i-1] not in ['x', '1', ')'] or line[i+1] not in ['1', 'x', '(']):
                return 'error' 
    return line

def brackets(line):
    if not '(' in line and not ')' in line: return line
    if line.count('(') != line.count(')'): return 'error'
    for i in range(len(line)):
        if line[i] == '(': 
            if i == len(line) - 1: return 'error'
            elif i == 0:
                if line[i + 1] not in ['1', 'x', '(']: return 'error'
                else: continue
            elif line[i-1] not in ['=', '+', '('] or line[i+1] not in ['1', 'x', '(']:
                return 'error' 
        if line[i] == ')': 
            if i == 0: return 'error'
            elif i == len(line) - 1:
                if line[i-1] not in ['1', ')', 'x']: return 'error'
                else: continue
            elif (line[i-1] not in ['1', ')', 'x']) or (line[i+1] not in ['+', ')', '=']):
                return 'error' 
    return line

def brackets_right(line):
    only_brackets_and_equal = []
    only_brackets = ''
    for i in line:
        if i in ['(', ')']: only_brackets += i
        elif i == '=':
            only_brackets_and_equal.append(only_brackets)
            only_brackets = ''
    only_brackets_and_equal.append(only_brackets)
    for part in only_brackets_and_equal:
        if part.count('(') != part.count(')'): return 'error' 
        for i in range(len(part)//2):
            if part and part.count('()') == 0: return 'error'
            part = part.replace('()', '', 1)       
    return line
    
def equivalence(line):
    if line.count('=') == 0: return line
    if line[0] == '=' or line[-1] == '=': return 'error'
    for i in range(len(line)):
        if line[i] != '=': continue
        elif line[i-1] not in ['1', 'x', ')'] or line[i+1] not in ['1', 'x', '(']:
            return 'error'
        return line
    
def kind_of_phrase(line):
    global add_only
    global multi_only
    
    line = line.replace(')', '')
    line = line.replace('(', '')
    line = line.replace('\'', '')
    
    if line == 'error': return 'out of syntax'
    if line in ['0', '1']: return 'constant'
    if line in ['x']: return 'variable'
    if '=' in line: return 'formula'
    elif multi_only: return 'complex term (sum of simple terms)' 
    elif add_only: return 'complex term (multiplication of simple terms)' 
    return 'complex term'

def analysis(line):
    line = right_symbols(line)
    if line != 'error': line = simplier(line)
    if line != 'error': line = brackets(line)
    if line != 'error': line = equivalence(line)
    if line != 'error': line = brackets_right(line)
    if line != 'error': line = plus_right(line)
    if line != 'error': return True 
    else: return False
    
def synthesis():
    the_num = int(input('set the length of the expressions to synthesize: '))
    chars = ['1', '0', 'x', '\'', '=', '*', '(', ')', '+']
    for cur in product(chars, repeat = the_num):
        variant = ''.join(cur)
        if analysis(variant): print(variant)
    input()

line = input('enter the expression you want to check for syntactic correctness:\n') 
while line != 'end':
    if analysis(line):
        print(kind_of_phrase(line))
    else: print('out of syntax')
    line = input('enter the expression you want to check for syntactic correctness:\n')