# Plotting sequences satisfying, x_{i+1} = p-1 - (p*i-1 mod x_i)
# with p prime and x_0 = 1, next to their autocorrelation.

import numpy as np
from matplotlib import pyplot  as plt

# The length of the sequences.
seq_length = 10000

upperbound_primes = 12 

# Computing a list of prime numbers up to n
def primes(n):
 sieve = [True] * n
 for i in xrange(3,int(n**0.5)+1,2):
   if sieve[i]:
       sieve[i*i::2*i]=[False]*((n-i*i-1)/(2*i)+1)
 return [2] + [i for i in xrange(3,n,2) if sieve[i]]

# The list of prime numbers up to upperbound_primes
p = primes(upperbound_primes)

# The amount of primes numbers
no_primes = len(p)

# Generate the sequence for the prime number p
def sequence(p):
  x = np.empty(seq_length)
  x[0] = 1
  for i in range(1,seq_length):
    x[i] = p - 1 - (p * (i-1) - 1) % x[i-1]
  return x

# List with the sequences.
seq = [sequence(i) for i in p]  

# Autocorrelation function.
def autocor(x):
  result = np.correlate(x,x,mode='full')
  return result[result.size/2:]

fig = plt.figure("The sequences next to their autocorrelation")
plt.suptitle("The sequences next to their autocorrelation")

# Proper spacing between subplots.
fig.subplots_adjust(hspace=1.2)

# Set up pyplot to use TeX.
plt.rc('text',usetex=True)
plt.rc('font',family='serif')

# Maximize plot window by command.
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

k = 0 
for s in  seq:
  k = k + 1
  fig.add_subplot(no_primes,2,2*(k-1)+1)
  plt.title("Sequence of the prime %d" % p[k-1])
  plt.plot(s)
  plt.xlabel(r"Index $i$")
  plt.ylabel(r"Sequence number $x_i$")
  plt.xlim(0,100)
  
  # Constrain the number of ticks on the y-axis, for clarity.
  plt.locator_params(axis='y',nbins=4)

  fig.add_subplot(no_primes,2,2*k)
  plt.title(r"Autocorrelation of the sequence $^{%d}x$" % p[k-1])
  plt.plot(autocor(s))
  plt.xlabel(r"Index $i$")
  plt.xticks
  plt.ylabel("Autocorrelation")
  
  # Proper scaling of the y-axis.
  ymin = autocor(s)[1]-int(autocor(s)[1]/10)
  ymax = autocor(s)[1]+int(autocor(s)[1]/10)
  plt.ylim(ymin,ymax)
  plt.xlim(0,500)
  
  plt.locator_params(axis='y',nbins=4)

  # Use scientific notation when 0< t < 1 or t > 10
  plt.ticklabel_format(style='sci',axis='y',scilimits=(0,1))

plt.show()