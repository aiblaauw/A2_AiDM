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

def estimate_cardinality_FM(values):
  """Estimates the number of unique elements in the input set values.
  Arguments:
    values: An iterator of hashable elements to estimate the cardinality of.
  """
  
  correction_factor_FM = 0.77351
  bitvector = np.zeros(32)
  
  for v in values:
      trailing = trailing_zeroes(v)
      bitvector[trailing] = 1
  #print(bitvector)
  for index, bit in enumerate(bitvector):
      if bit == 0:
          return 2 ** index / correction_factor_FM
  return 2 ** trailing / correction_factor_FM

predictions_FM = [estimate_cardinality_FM([random.getrandbits(32) for i in range(100000)]) for j in range(10)]
predictions_FM = np.array(predictions_FM)
# True unique element value very close to number of random values 
RAE_FM = np.abs(100000 - predictions_FM)/100000

print("RAE_FM:", RAE_FM)

# Partition your hash functions into several groups
# Calculate the average of each group
# Then take the median of the averages


###


## DF (LogLog)
## http://algo.inria.fr/flajolet/Publications/DuFl03-LNCS.pdf
## http://blog.notdot.net/2012/09/Dam-Cool-Algorithms-Cardinality-Estimation

def estimate_cardinality_DF(values, k):
  """Estimates the number of unique elements in the input set values.
  Arguments:
    values: An iterator of hashable elements to estimate the cardinality of.
    k: The number of bits of hash to use as a bucket number; there will be 2**k buckets.
  """
  
  correction_factor_DF = 0.79402
  num_buckets = 2 ** k
  max_zeroes = [0] * num_buckets # Initialize, all zeroes
  
  for v in values:
    bucket = v & (num_buckets - 1) # Mask out the k least significant bits as bucket ID
    bucket_hash = v >> k # Returns h with the bits shifted to the right by k places,
    # 
    max_zeroes[bucket] = max(max_zeroes[bucket], trailing_zeroes(bucket_hash))
    # If trailing zeroes from bucket hash > max zeroes; update
  
  cardinality = correction_factor_DF * num_buckets * ( 2 ** np.mean(max_zeroes) )  
  return cardinality


predictions_DF = [estimate_cardinality_DF([random.getrandbits(32) for i in range(100000)], 10) for j in range(10)]
predictions_DF = np.array(predictions_DF)
# True unique element value very close to number of random values 
RAE_DF = np.abs(100000 - predictions_DF)/100000

print("\nRAE_DF:", RAE_DF)


#test = np.zeros(60)
#for index, item in enumerate(test):
#    print(index)
