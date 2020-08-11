The folder "implicit" contains all JOB queries with implict where clauses

The folder "explict" contains the trainsformed JOB queries according to the scheme detailed in the paper. 

All queries use COUNT(*) as final aggregate to verify correctness of the explicit queries.

In case of Postgres please use the following hints for on the explicit queries:

	 "set join_collapse_limit = 1"
	 "set enable_nestloop to false"
