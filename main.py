from fastapi import FastAPI, Request
from pydantic import BaseModel
import subprocess

app = FastAPI()

class CodeRequest(BaseModel):
    code: str
    testIncludes: str

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
        if payload.testIncludes in output:
            return {"success": True, "output": output}
        else:
            return {"success": False, "output": output}
    except Exception as e:
        return {"success": False, "error": str(e)}