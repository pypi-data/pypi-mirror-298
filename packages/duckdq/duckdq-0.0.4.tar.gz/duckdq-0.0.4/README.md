# Requirements
```pip install -r requirements.txt```

# Env
.env File
```
API_KEY=xyz
API_URL=xyz
```
Or
Export variables 
```
export API_KEY=xyz
export API_URL=xyz
```

# Database User
```
GRANT USAGE on schema "validation" to anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA "validation" TO anon;
GRANT ALL ON SEQUENCE validation.rule_output_rule_output_id_seq TO anon;
GRANT ALL ON SEQUENCE validation. connections_connection_id_seq TO anon;
GRANT ALL ON SEQUENCE validation.owlcheck_q_job_id_seq TO anon;
GRANT ALL ON SEQUENCE validation.job_log_log_id_seq TO anon;
GRANT ALL ON SEQUENCE validation.assignment_q_id_seq TO anon;
```

# Examples
```
"""
# Invididual Usage Examples 

#Client instantiation
api = APIClient(api_client)

engine = duckdb.connect(':memory:')
engine.sql(" select * from read_csv_auto('./data/fake_customers.csv') limit 10").show()
engine.close()

# owl_check_history, Delete, Insert, Read
api.delete_owl_check_history("test")
api.insert_owl_check_history("test", "2024-09-16")
rs = api.get_owl_check_history("test")
print(rs)

# owl_catalog, Delete, Insert, Read
api.delete_owl_catalog("test")
api.insert_owl_catalog("test")
rs = api.get_owl_catalog("test")
print(rs)

# dataset_schema, Delete, Insert, Read
api.delete_dataset_schema("test")
api.insert_dataset_schema("test")
rs = api.get_dataset_schema("test")
print(rs)

# dataset_field, Delete, Insert, Read
api.delete_dataset_field("test", "2024-09-16")
api.insert_dataset_field("test", "2024-09-16")
rs = api.get_dataset_field("test", "2024-09-16")
print(rs)

# Print the result
df = pd.DataFrame(rs.data)
print(df[['dataset','run_id','rc']])

# run rules 
api.delete_rule_output("test", "2024-09-16")
api.run_rules("test", "2024-09-16")

# scoring
rule_output = api.get_rule_output("test", "2024-09-16")
rule_score = 0
for r in rule_output.data:
    rule_score += r['score']
print(rule_score)

# dataset_scan, Delete, Insert, Read
delete_record = api.delete_dataset_scan("test", "2024-09-16")
add_record = api.insert_dataset_scan("test", "2024-09-16", 100, 100 - rule_score)
```




# Register
```
dataset = 'test' 

# opt_spark
api.delete_opt_spark(dataset)
api.insert_opt_spark(dataset)
rs = api.get_opt_spark(dataset)
print(rs)
df = pd.DataFrame(rs.data)
display(df)

# opt_pushdown
api.delete_opt_pushdown(dataset)
api.insert_opt_pushdown(dataset)
rs = api.get_opt_pushdown(dataset)
print(rs)
df = pd.DataFrame(rs.data)
display(df)

# opt_profile
api.delete_opt_profile(dataset)
api.insert_opt_profile(dataset)
rs = api.get_opt_profile(dataset)
print(rs)
df = pd.DataFrame(rs.data)
display(df)

# opt_load
api.delete_opt_load(dataset)
api.insert_opt_load(dataset)
rs = api.get_opt_load(dataset)
print(rs)
df = pd.DataFrame(rs.data)
display(df)

# opt_profile
api.delete_opt_profile(dataset)
api.insert_opt_profile(dataset)
rs = api.get_opt_profile(dataset)
print(rs)
df = pd.DataFrame(rs.data)
display(df)

# opt_env
api.delete_opt_env(dataset)
api.insert_opt_env(dataset)
rs = api.get_opt_env(dataset)
print(rs)
df = pd.DataFrame(rs.data)
display(df)

# opt_owl
api.delete_opt_owl(dataset)
api.insert_opt_owl(dataset)
rs = api.get_opt_owl(dataset)
print(rs)
df = pd.DataFrame(rs.data)
display(df)
```


# Job 
```
dataset = 'test' 
run_id = '2024-09-20'
conn.sql(f"create table if not exists {dataset} as select * from read_csv_auto('./data/fake_customers.csv') ")

# owl_check_history, 
# Delete, Insert, Read
api.delete_owl_check_history(dataset)
api.insert_owl_check_history(dataset, run_id)
rs = api.get_owl_check_history(dataset)
print(rs)

# owl_catalog, 
# Delete, Insert, Read
api.delete_owl_catalog(dataset)
api.insert_owl_catalog(dataset)
rs = api.get_owl_catalog(dataset)
print(rs)

# dataset_schema, 
# Delete, Insert, Read
api.delete_dataset_schema(dataset)
api.insert_dataset_schema(dataset)
rs = api.get_dataset_schema(dataset)
print(rs)

# dataset_field, 
# Delete, Insert, Read
api.delete_dataset_field(dataset, run_id)
api.insert_dataset_field(dataset, run_id)
rs = api.get_dataset_field(dataset, run_id)
print(rs)

# run rules 
api.delete_rule_output(dataset, run_id)
api.run_rules(dataset, run_id)

# scoring
rule_output = api.get_rule_output(dataset, run_id)
print(rule_output.data)

rule_score = 0
for r in rule_output.data:
    rule_score += r['score']
print(str(rule_score))

# dataset_scan, 
# Delete, Insert, Read
delete_record = api.delete_dataset_scan(dataset, run_id)
add_record = api.insert_dataset_scan(dataset, run_id, 100, 100 - rule_score)
rs = api.get_dataset_scan(dataset, run_id)
print(rs.data)

```