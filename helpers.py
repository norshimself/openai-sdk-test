import os

def load_system_prompt(prompt_path="system_prompt.md"):
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"System prompt file not found at: {prompt_path}")
        
    with open(prompt_path, "r") as f:
        content = f.read()
        if "# Analytics Assistant System Prompt" in content:
            return content.replace("# Analytics Assistant System Prompt", "").strip()
        return content.strip()

def strip_markdown_code_blocks(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text

