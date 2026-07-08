import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def main():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY environment variable not set.")
        return
        
    client = Groq(api_key=api_key)
    
    with open("prompt_template.txt", "r") as f:
        prompt = f.read()
        
    print("Generating post with random dynamic topic...")
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            response_content = completion.choices[0].message.content
            break # Success, exit retry loop
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                print("Max retries reached. Exiting.")
                return
            print("Retrying...")
            
    # Try to extract json from the response
    json_str = response_content
    match = re.search(r"```json\s*(.*?)\s*```", response_content, re.DOTALL)
    if match:
        json_str = match.group(1)
        
    try:
        post_data = json.loads(json_str)
        with open("post.json", "w") as f:
            json.dump(post_data, f, indent=2)
        print("Successfully generated post.json")
                
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response from Groq. Error: {e}")
        print(response_content)

if __name__ == "__main__":
    main()
