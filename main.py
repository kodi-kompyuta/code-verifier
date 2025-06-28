from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI()

class CodeRequest(BaseModel):
    code: str
    testIncludes: str | None = None  # optional
    expectedOutput: str | None = None  # also optional

@app.post("/verify")
async def verify_code(payload: CodeRequest):
    print("✅ Received request to /verify")
    print("📦 Code:", payload.code)
    print("🔍 testIncludes:", payload.testIncludes)
    print("🔍 expectedOutput:", payload.expectedOutput)

    try:
        result = subprocess.run(
            ['python3', '-c', payload.code],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout.strip()
        print("🖨️ Code Output:", output)

        # Priority: check exact match if expectedOutput exists
        if payload.expectedOutput and output == payload.expectedOutput:
            return {"success": True, "output": output}
        # Otherwise fallback to substring check
        elif payload.testIncludes and payload.testIncludes in output:
            return {"success": True, "output": output}
        else:
            return {"success": False, "output": output}

    except Exception as e:
        print("🔥 Error running code:", str(e))
        return {"success": False, "error": str(e)}
