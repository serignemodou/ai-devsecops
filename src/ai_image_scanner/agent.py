import json
import requests
import os
import subprocess

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def scan_image(image):
    result = subprocess.run(
        ["trivy", "image", "-f", "json", image],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def analyze_wit_ai(scan_result):
    prompt = f"""
    Analyse ces vulnérabilités et donne une décision:
    - BLOCK si critique exploitable
    - WARN si modéré
    - ALLOW si safe
    
    Data:
    {json.dumps(scan_result)[:4000]}
    """
    
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        },
        json={
            "model": "gpt-4.1-mini",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    
    return response.json()["choices"][0]["message"]["content"]

def decide(action):
    if "BLOCK" in action:
        return "BLOCK"
    elif "WARN" in action:
        return "WARN"
    return "ALLOW"

def main(image):
    scan = scan_image(image)
    ai_analysis = analyze_wit_ai(scan)
    decision = decide(ai_analysis)
    
    print(f"Decision: {decision}")
    print(ai_analysis)
    
    if decision == "BLOCK":
        exit(1)
    
if __name__ == "__main__":
    import sys
    main(sys.argv[1])