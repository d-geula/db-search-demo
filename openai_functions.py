filter_table_meta = {
    "name": "filter_table",
    "description": "Use this function to generate valid SQLite queries to filter a given database table.",
    "parameters": {
        "type": "object",
        "properties": {
            "sql_query": {
                "type": "string",
                "description": "The SQL query to be executed on the given SQLite table.\n"
                "All queries should use 'SELECT *' to ensure all columns are included in the results.\n"
                "You can ignore this rule where necessary to properly answer the user's question."
                ""
            },
        },
        "required": ["sql_query"],
    }, 
}