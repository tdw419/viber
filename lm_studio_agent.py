import subprocess
import json

LM_STUDIO_API_URL = "http://localhost:1234/v1" # Default LM Studio API URL

def run_command(command):
    """Runs a command and returns the output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(e.stderr)
        return None

def check_lm_studio_status():
    """
    Checks if LM Studio API is reachable.
    """
    print(f"Checking LM Studio API status at {LM_STUDIO_API_URL}...")
    try:
        # Use curl to check if the API is reachable
        # This assumes curl is available in the environment
        response = run_command(f"curl -s -o /dev/null -w '%{{http_code}}' {LM_STUDIO_API_URL}/models")
        if response == "200":
            print("LM Studio API is running and reachable.")
            # Optionally, fetch models list
            models_response = run_command(f"curl -s {LM_STUDIO_API_URL}/models")
            if models_response:
                try:
                    models_data = json.loads(models_response)
                    print("Available models:")
                    for model in models_data.get("data", []):
                        print(f"- {model.get('id')}")
                except json.JSONDecodeError:
                    print("Could not parse models list from LM Studio API.")
            return True
        else:
            print(f"LM Studio API is not responding. HTTP Code: {response}")
            return False
    except Exception as e:
        print(f"An error occurred while checking LM Studio status: {e}")
        return False

def get_embedding_from_lm_studio(text: str) -> list[float]:
    """
    Gets a vector embedding for a given text from the LM Studio API.
    """
    try:
        # Use curl to call the embeddings API
        # This assumes curl is available in the environment
        with open("payload.json", "w") as f:
            json.dump({"input": text, "model": "nomic-ai/nomic-embed-text-v1.5-GGUF"}, f)
        command = f"""
        curl -s -X POST {LM_STUDIO_API_URL}/embeddings \
        -H "Content-Type: application/json" \
        -d @payload.json
        """
        response = run_command(command)
        if response:
            try:
                data = json.loads(response)
                return data['data'][0]['embedding']
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Could not parse embedding from LM Studio API response: {e}")
                print(f"Response: {response}")
                return []
    except Exception as e:
        print(f"An error occurred while getting embedding from LM Studio: {e}")
        return []

def get_completion_from_lm_studio(prompt: str, model: str = "local-model") -> str:
    """
    Gets a chat completion for a given prompt from the LM Studio API.
    """
    try:
        # Use curl to call the chat completions API
        # This assumes curl is available in the environment
        with open("payload.json", "w") as f:
            json.dump({
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
            }, f)
        command = f"""
        curl -s -X POST {LM_STUDIO_API_URL}/chat/completions \
        -H "Content-Type: application/json" \
        -d @payload.json
        """
        response = run_command(command)
        if response:
            try:
                data = json.loads(response)
                return data['choices'][0]['message']['content']
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Could not parse completion from LM Studio API response: {e}")
                print(f"Response: {response}")
                return ""
    except Exception as e:
        print(f"An error occurred while getting completion from LM Studio: {e}")
        return ""

def main():
    """
    The main loop for the LM Studio AI agent.
    """
    print("LM Studio Agent: Hello! I'm ready to help manage LM Studio.")
    print("Available commands: status, help, exit")

    while True:
        try:
            user_input = input("> ").strip()
            if not user_input:
                continue

            command = user_input.lower()

            if command == "exit":
                print("LM Studio Agent: Goodbye!")
                break
            elif command == "help":
                print("Available commands: status, help, exit")
            elif command == "status":
                check_lm_studio_status()
            else:
                print("LM Studio Agent: Unknown command. Type 'help' for a list of commands.")
        except (EOFError, KeyboardInterrupt):
            print("\nLM Studio Agent: Goodbye!")
            break

if __name__ == "__main__":
    main()
