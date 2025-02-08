import ollama


def read_code_file(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def prompt_deepseek_14_bn(code_snippet):
    prompt = f"Here is the code to analyze:\n\n{code_snippet}\n\n Generate a Mermaid flowchart from this code."
    response = ollama.chat(
        model="deepseek-r1:14b",
        messages=[
            {
                "role": "system",
                "content": "You are a Mermaid flowchart generator. Please generate a Mermaid flowchart from the given code snippet. No description, just the flowchart. Write correct Mermaid syntax.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    print(response["message"]["content"])


if __name__ == "__main__":
    file_path = "codeSnippet.py"  # Replace with actual file path
    code = read_code_file(file_path)
    if code:
        prompt_deepseek_14_bn(code)
