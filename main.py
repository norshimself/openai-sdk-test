import sys
import json
from client import get_client, ProviderConfigurationError
from helpers import load_system_prompt, strip_markdown_code_blocks


def main():
    try:
        with open("test/analytics_data.json", "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON file: {e}", file=sys.stderr)
        sys.exit(1)

    system_prompt = load_system_prompt("system_prompt.md")

    try:
        client = get_client()
    except ProviderConfigurationError as e:
        print(f"Initialization Error: {e}", file=sys.stderr)
        sys.exit(1)

    print("Sending data from test/analytics_data.json to openai/gpt-4o-mini...")
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(data)}
            ],
        )

        result = response.choices[0].message.content
        if result:
            clean_result = strip_markdown_code_blocks(result)
            try:
                parsed_json = json.loads(clean_result)
                with open("result.json", "w") as f:
                    json.dump(parsed_json, f, indent=2)
                print("Result successfully saved to result.json")
            except json.JSONDecodeError:
                with open("result.json", "w") as f:
                    f.write(clean_result)
                print("Saved raw content to result.json (could not parse as JSON)")
        else:
            refusal = response.choices[0].message.refusal
            print(f"Model refused to respond: {refusal}", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error calling LLM provider: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
