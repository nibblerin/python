import os

def default_output_path(fmt: str) -> str:
    env_var = "DEFAULT_OUTPUT_JSON" if fmt == "json" else "DEFAULT_OUTPUT_XML"
    fallback = f"result_{fmt}.{fmt}"
    return os.getenv(env_var, fallback)