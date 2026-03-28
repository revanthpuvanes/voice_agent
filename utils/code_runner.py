import pandas as pd

def clean_code(code):
    code = code.replace("```python", "").replace("```", "")
    return code.strip()

def run_code(code, df):
    code = clean_code(code)

    exec_globals = {"pd": pd}
    exec_locals = {"df": df}

    try:
        exec(code, exec_globals, exec_locals)
        return exec_locals.get("result", "No result returned")
    except Exception as e:
        return f"Error: {str(e)}"