""" 
This script can be run from the shell by specifying the following
parameters as keyworded arguments:
    
p = probability of success
nt = number of trials
ns = number of success

If the arguments are not keyworded, they must be in the above order.

"""

import math

def combination(n, r):
    """ Calculate nCr """
    fact = math.factorial
    return fact(n) / fact(r) / fact(n-r)

def calc_prob(p_success, n_trials, n_success):
    """ Calculate P(X = x), x == n_success """
    # shortening
    p = p_success
    n = n_trials
    r = n_success
    
    return (combination(n, r) * p ** r * (1-p) ** (n-r))

def binom_probs(p_success, n_trials, n_success):
    # shortening
    p = p_success
    nt = n_trials
    ns = n_success
    
    if p < 0.0 or p > 1.0:
        raise ValueError('Probability of success must be between 0 and 1 (inclusive), input p_success = %s.' % p_success)
    elif nt < 0 or type(nt) != int:
        raise ValueError('Number of trials must be a positive integer, input n_trials = %s.' % n_trials)
    elif ns < 0 or type(ns) != int:
        raise ValueError('Number of success must be a positive integer, input n_success = %s.' % n_success)
    elif nt < ns:
        raise ValueError('Number of trials must be greater or equal to number of success, input n_trials = %s; n_success = %s.' % (n_trials, n_success))
    
    prob_list = [calc_prob(p, nt, k) for k in range(nt + 1)]
    
    X_eq_x = prob_list[ns] # P(X = x)
    
    X_less_x = sum(prob_list[:ns]) # P(X < x)
    X_leq_x = X_less_x + X_eq_x # P(X <= x)    
    
    X_great_x = sum(prob_list[ns+1:]) # P(X > x)
    X_geq_x = X_eq_x + X_great_x # P(X >= x)
    
    return (X_eq_x, X_less_x, X_leq_x, X_great_x, X_geq_x)

if __name__ == '__main__':
    import sys
    kw_detected = []
    parsed_key = []
    
    if len(sys.argv) != 4:
        raise RuntimeError('Expected 3 arguments (p, nt, ns), %d given' % (len(sys.argv)-1))
    
    for arg in sys.argv[1:]:
        key = arg.split('=')[0]
        if arg == key:
            kw_detected.append(False)
            continue
        else:
            kw_detected.append(True)
        
        if key in parsed_key:
            raise KeyError('Repeated keys detected.')
        if key not in ['p', 'nt', 'ns']:
            raise KeyError('Invalid argument key "%s".' % key)
            
        parsed_key.append(key)
    
    if not kw_detected[0] == kw_detected[1] == kw_detected[2]:
        raise RuntimeError('Arguments must be either all keyworded or all non-keyworded.')
        
    use_kw = kw_detected[0]
    
    if use_kw:
        for arg in sys.argv[1:]:
            k = arg.split('=')[0]
            v = arg.split('=')[1]
            
            if k == 'p':
                p = v
            elif k == 'nt':
                nt = v
            elif k == 'ns':
                ns = v
                
    else:
        p = sys.argv[1]
        nt = sys.argv[2]
        ns = sys.argv[3]
        
    X_eq_x, X_less_x, X_leq_x, X_great_x, X_geq_x = binom_probs(float(p), int(nt), int(ns))
    
    print('Calculating binomial probabilities with p=%s; nt=%s; ns=%s ...' % (p, nt, ns))
    print('P(X = %s) = %s' % (ns, X_eq_x))
    print('P(X < %s) = %s' % (ns, X_less_x))
    print('P(X <= %s) = %s' % (ns, X_leq_x))
    print('P(X > %s) = %s' % (ns, X_great_x))
    print('P(X >= %s) = %s' % (ns, X_geq_x))
