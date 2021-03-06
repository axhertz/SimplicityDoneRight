# SimplicityDoneRight

This is the code base of the evaluation shown in the work [Simplicity Done Right for Join Ordering](http://cidrdb.org/cidr2021/papers/cidr2021_paper01.pdf).

A short presentation is available at [CIDR DB](https://www.youtube.com/watch?v=PDph36kjPxI).

## Modules 

1. **Focused Sampling:** The code mimics an in-memory column store and exploits specific access patterns to boost sampling speed. 
2. **Conditional Sampling:** The code simulates an index over arbitrary filter predicates. The approach exploits index or index like structures to boost estimation accuracy. 
3. **JOB-Queries:** Queries of the [Join-Order-Benchmark](https://github.com/gregrahn/join-order-benchmark) by Leis et al. with implicit where clauses and queries transformed into  an explicit join order according to our enumeration scheme.
## Quick Start

Please run the following to compile code for the focused sampling approach and to download the necessary data sets. 

`./prepare.bash`

To run Focused Sampling:

`cd FocusedSampling/bin`
`./focusedSampling`

To run Conditional Sampling:

`cd ConditionalSampling`
`python3 evalCondSample.py`

To build new conditional samples: 

`cd buildCondSample`
`python3 buildCondSample.py`



To compare the implicit to the explicit JOB Queries you need to [install Postgres](https://www.postgresql.org/download/linux/ubuntu/) and [load the (frozen) IMDB data](https://github.com/gregrahn/join-order-benchmark).
 
For running the explicit queries on Postgres, please use the following SQL hints to **prevent join reordering** and to **restrict** the physical join operator selection **to hash joins** (merge joins for sorted attributes): 

`set join_collapse_limit = 1;`

`set enable_nestloop to false;`

