
import extension

def main():
    """
    The main loop for the AI agent.
    """
    print("AI Agent: Hello! I'm ready to manage the LanceDB/RAG system.")
    print("Available commands: init, init_conversations, add <text>, search <query>, help, exit")

    while True:
        try:
            user_input = input("> ").strip()
            if not user_input:
                continue

            parts = user_input.split(" ", 1)
            command = parts[0].lower()

            if command == "exit":
                print("AI Agent: Goodbye!")
                break
            elif command == "help":
                print("Available commands: init, init_conversations, add <text>, search <query>, help, exit")
            elif command == "init":
                extension.rag_init_db()
            elif command == "init_conversations":
                extension.rag_init_conversations_db()
            elif command == "add":
                if len(parts) > 1:
                    extension.rag_add(parts[1])
                else:
                    print("AI Agent: Please provide the text to add.")
            elif command == "search":
                if len(parts) > 1:
                    extension.rag_search(parts[1])
                else:
                    print("AI Agent: Please provide a search query.")
            else:
                print("AI Agent: Unknown command. Type 'help' for a list of commands.")
        except (EOFError, KeyboardInterrupt):
            print("\nAI Agent: Goodbye!")
            break

if __name__ == "__main__":
    main()
