"""
Bedrock diagnostic — checks Gemma on AWS Bedrock.
Run: python diagnose_bedrock.py
"""

import os
import json
import sys
from dotenv import load_dotenv

load_dotenv()

print("=" * 55)
print("  Bedrock Diagnostics")
print("=" * 55)

region     = os.getenv("AWS_REGION")
access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
model_id   = os.getenv("BEDROCK_MODEL_ID")

# ── Step 1: Check env vars ─────────────────────────────────────
print("\n[1] Checking .env configuration...")
print(f"  AWS_REGION           : {region or '❌ NOT SET'}")
print(f"  AWS_ACCESS_KEY_ID    : {'✅ SET' if access_key else '❌ NOT SET'}")
print(f"  AWS_SECRET_ACCESS_KEY: {'✅ SET' if secret_key else '❌ NOT SET'}")
print(f"  BEDROCK_MODEL_ID     : {model_id or '❌ NOT SET'}")

if not all([region, access_key, secret_key, model_id]):
    print("\n❌ Missing env vars. Fix your .env file first.")
    sys.exit(1)

# ── Step 2: Check boto3 ────────────────────────────────────────
print("\n[2] Checking boto3 import...")
try:
    import boto3
    print("  ✅ boto3 is installed")
except ImportError:
    print("  ❌ boto3 not installed. Run: pip install boto3")
    sys.exit(1)

# ── Step 3: Check AWS credentials ─────────────────────────────
print("\n[3] Checking AWS credentials (STS)...")
try:
    sts = boto3.client(
        "sts",
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    identity = sts.get_caller_identity()
    print(f"  ✅ Credentials valid!")
    print(f"  Account : {identity['Account']}")
    print(f"  UserID  : {identity['UserId']}")
except Exception as e:
    print(f"  ❌ Credential error: {e}")
    sys.exit(1)

# ── Step 4: Check Bedrock model access ────────────────────────
print("\n[4] Checking Bedrock model access...")
try:
    bedrock_mgmt = boto3.client(
        "bedrock",
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    models = bedrock_mgmt.list_foundation_models()
    available = [m["modelId"] for m in models["modelSummaries"]]
    if model_id in available:
        print(f"  ✅ Model '{model_id}' is available in your region")
    else:
        print(f"  ⚠️  Model '{model_id}' not found in list (may still work).")
except Exception as e:
    print(f"  ⚠️  Could not list models: {e}")

# ── Step 5: Invoke Gemma ───────────────────────────────────────
print("\n[5] Trying Gemma invocation...")
try:
    bedrock_rt = boto3.client(
        service_name="bedrock-runtime",
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    body = json.dumps({
        "messages": [{"role": "user", "content": "Say hello in 5 words."}],
        "max_tokens": 50,
        "temperature": 0.1,
    })
    response = bedrock_rt.invoke_model(body=body, modelId=model_id)
    result = json.loads(response["body"].read())
    text = result["choices"][0]["message"]["content"]
    print(f"  ✅ Bedrock is working!")
    print(f"  Response: {text}")
except Exception as e:
    print(f"  ❌ Invocation failed: {e}")

print("\n" + "=" * 55)