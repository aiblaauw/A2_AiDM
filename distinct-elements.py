# -*- coding: utf-8 -*-

"""
Assignment 2: Distinct Elements,
Approximating the number of distinct elements in a stream.

Testing two distinct/element estimation techniques;
- Flajolet-Martin
- Durand-Flajolet (LogLog Counting)
 

Accuracy was evaluated by;
- Expected count of elements / buckets
- Number of distinct elements in the stream
- Required memory (number of bytes)
- Relative Approximation Error metric 

Running multiple experiments, establish/verify the trade-offs;
- For various numbers of distinct elements
- number of buckets
- number of setups 

"""

import numpy as np
import random


def trailing_zeroes(num):
  """Counts the number of trailing 0 bits in num."""
  if num == 0:
    return 32 # Assumes 32 bit integer inputs!
  p = 0
  while (num >> p) & 1 == 0:
    p += 1
  return p


## FM
## http://algo.inria.fr/flajolet/Publications/FlMa85.pdf
## https://www.cms.waikato.ac.nz/~abifet/book/chapter_4.html
## https://ravi-bhide.blogspot.com/2011/04/flajolet-martin-algorithm.html

## h = hash
## bit(y, k) = binary representation 
## p = position of the least significant 1-bit in the binary representation of v
## R = largest index with bitmap val 1
## f = correction factor 0.77351
## 2**R = estimate 

#for v in values:
#  bitmap[v] = 0
#for v in values:
#  index = p(h(v))
#  if bitmap[index] == 0:
#    bitmap[index] == 1

def estimate_cardinality_FM(values):
  """Estimates the number of unique elements in the input set values.

  Arguments:
    values: An iterator of hashable elements to estimate the cardinality of.
  """
  logvalues = np.log(values)
  for v in logvalues:
    h = hash(v)
    trailing = trailing_zeroes(h)
  return 2 ** trailing / 0.77351

result_FM = [100000/estimate_cardinality_FM([random.getrandbits(32) for i in range(100000)]) for j in range(10)]
print(result_FM)


## DF (LogLog)
## http://algo.inria.fr/flajolet/Publications/DuFl03-LNCS.pdf
## http://blog.notdot.net/2012/09/Dam-Cool-Algorithms-Cardinality-Estimation

def estimate_cardinality_DF(values, k):
  """Estimates the number of unique elements in the input set values.

  Arguments:
    values: An iterator of hashable elements to estimate the cardinality of.
    k: The number of bits of hash to use as a bucket number; there will be 2**k buckets.
  """
  num_buckets = 2 ** k
  max_zeroes = [0] * num_buckets
  for v in values:
    h = hash(v)
    bucket = h & (num_buckets - 1) # Mask out the k least significant bits as bucket ID
    bucket_hash = h >> k
    max_zeroes[bucket] = max(max_zeroes[bucket], trailing_zeroes(bucket_hash))
  return 2 ** (float(sum(max_zeroes)) / num_buckets) * num_buckets * 0.79402


result_DF = [100000/estimate_cardinality_DF([random.getrandbits(32) for i in range(100000)], 10) for j in range(10)]
print(result_DF)
