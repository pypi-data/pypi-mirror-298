-- config
-- All paramerers are optional
-- @param name: The alias of the file. If not provided, the filename will be used.
-- @param description: The description of the file.
-- @param output_paths: The file paths where the execution results will be saved.
-- @param output_type: The type of the execution result. If no value is provided, it will be automatically estimated.
-- @param connection: The connection name created in the Morph app. If no value is provided, the query will be executed on the built-in database.
-- For more information: https://www.morphdb.io/docs
{{
	config(
		name="example_sql_cell",
		description="Example SQL cell",
		output_paths=["_private/{name}/{now()}{ext()}"],
        output_type="dataframe",
	)
}}

select 1 as test
