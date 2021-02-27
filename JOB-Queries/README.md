### Quick Start

The folder "implicit" contains all JOB queries with implict where clauses.

The folder "explict" contains the trainsformed JOB queries according to the scheme detailed in the [paper](http://cidrdb.org/cidr2021/papers/cidr2021_paper01.pdf). 

All queries use COUNT(*) as final aggregate to verify correctness of the explicit queries.

In case of Postgres please use the following hints for on the explicit queries:

	 "set join_collapse_limit = 1"
	 "set enable_nestloop to false"
	 	 
### Reproduce Query Transformation
	 
In order to request statistics you may need to create the following SQL Function: 
```sql
CREATE FUNCTION count_estimate(query text) RETURNS integer AS
$func$
DECLARE
    rec   record;
    rows  integer;
BEGIN
    FOR rec IN EXECUTE 'EXPLAIN ' || query LOOP
        rows := substring(rec."QUERY PLAN" FROM ' rows=([[:digit:]]+)');
        EXIT WHEN rows IS NOT NULL;
    END LOOP;

    RETURN rows;
END
$func$ LANGUAGE plpgsql;
```

Then run:

	python3 transform.py
The script is highly experimental and transforms the implicit queries of the Join-Order-Benchmark into the explicit join order described in the paper. Note that the script is meant for reproducibilty purposes and the necessary parsing code might obfuscate the core enumeration procedure. To gain insights on the enumeration procedure we recommend reading the paper.  
