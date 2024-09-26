from app.prompts.main import Prompt

prompt = Prompt.read_prompt_full('query_template', schema='tableName', question='column1, column2')

print(prompt)