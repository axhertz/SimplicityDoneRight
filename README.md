# SimplicityDoneRight

This is the code base of the evaluation shown in the work "Simplicity Done Right for Join Ordering".

## Modules 

1. **Focused Sampling:** The code mimics an in-memory column store and exploits specific access patterns to boost sampling speed. 
2. **Conditional Sampling:** The code simulates an index over arbitrary filter predicates. The approach exploits index or index like structures to boost estimation accuracy. 
3. **JOB-Queries:** Queries of the Join-Order-Benchmark with implicit where clauses and transformed into explicit join orders according to our enumeration scheme. For more details consider reading the README.md in die JOB-Queries directory.

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



To compare the implicit to the explicit JOB Queries you may need to [install Postgres](https://www.postgresql.org/)  first and [load the IMDB data](https://github.com/gregrahn/join-order-benchmark).

Please use the following sql hints if running the explicit queries on Postgres:

`set collapse_join limit = 1;`

`set enable_nestloop to false;`
