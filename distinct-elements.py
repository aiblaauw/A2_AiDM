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


## FM
## h = hash
## bit(y, k) = binary representation 
## R = largest index with bitmap val 1
## 2**R = estimate 

#for i in items:
#  bitmap[i] = 0
#for b in buckets:
#  index = p(h(x))
#  if bitmap[index] == 0:
#    bitmap[index] == 1


## DF
## http://algo.inria.fr/flajolet/Publications/DuFl03-LNCS.pdf

#import numpy as np
import random


def trailing_zeroes(num):
  """Counts the number of trailing 0 bits in num."""
  if num == 0:
    return 32 # Assumes 32 bit integer inputs!
  p = 0
  while (num >> p) & 1 == 0:
    p += 1
  return p

def estimate_cardinality(values, k):
  """Estimates the number of unique elements in the input set values.

  Arguments:
    values: An iterator of hashable elements to estimate the cardinality of.
    k: The number of bits of hash to use as a bucket number; there will be 2**k buckets.
  """
  num_buckets = 2 ** k
  max_zeroes = [0] * num_buckets
  for value in values:
    h = hash(value)
    bucket = h & (num_buckets - 1) # Mask out the k least significant bits as bucket ID
    bucket_hash = h >> k
    max_zeroes[bucket] = max(max_zeroes[bucket], trailing_zeroes(bucket_hash))
  return 2 ** (float(sum(max_zeroes)) / num_buckets) * num_buckets * 0.79402


result = [100000/estimate_cardinality([random.random() for i in range(100000)], 10) for j in range(10)]
print(result)
