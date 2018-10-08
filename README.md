# A2_AiDM

Approximating the number of distinct elements in a stream.\
Testing two distinct/element estimation techniques;
- Flajolet-Martin
- Durand-Flajolet (LogLog Counting)
 
Accuracy was evaluated by;
- Expected count of elements / buckets
- Number of distinct elements in the stream
- Required memory (number of bytes)
- Relative Approximation Error (RAE) metric 

Running multiple experiments, establish/verify the trade-offs;
- For various numbers of distinct elements
- number of buckets
- number of setups 

### Running experiment

Edit variables;
- Number of elements 
- Number of bits (used to determine number of buckets and memory)

RAE given as output
