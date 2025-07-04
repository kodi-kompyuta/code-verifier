from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import io
import sys
from contextlib import redirect_stdout

app = FastAPI()

# ✅ Allow CORS so your React Native app can call it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with your domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Model to parse the incoming request
class CodeRequest(BaseModel):
    code: str

@app.post("/verify")
async def verify_code(request: CodeRequest):
    code = request.code

    # ✅ Define a minimal, safe execution environment
    safe_globals = {
        "__builtins__": {
            "print": print,
            "range": range,
            "len": len,
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            # Add more safe functions as needed
        }
    }

    try:
        f = io.StringIO()
        with redirect_stdout(f):
            exec(code, safe_globals, {})
        output = f.getvalue()
        return {"output": output}
    except Exception as e:
        return {"output": f"❌ Error: {str(e)}"}
