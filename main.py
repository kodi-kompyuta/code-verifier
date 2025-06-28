from fastapi import FastAPI, Request
from pydantic import BaseModel
import subprocess

app = FastAPI()

# ✅ Add this root route
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI 🎉"}

# ✅ Your code model
class CodeRequest(BaseModel):
    code: str
    expectedOutput: str = None
    testIncludes: str = None

@app.post("/verify")
async def verify_code(payload: CodeRequest):
    try:
        result = subprocess.run(
            ['python3', '-c', payload.code],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout.strip()

        if payload.expectedOutput:
            is_match = payload.expectedOutput in output
        elif payload.testIncludes:
            is_match = payload.testIncludes in output
        else:
            is_match = False

        return {"success": is_match, "output": output}
    except Exception as e:
        return {"success": False, "error": str(e)}
