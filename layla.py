import ollama
import time

def get_ollama_response(prompt, history):
    """
    Get a response from the Ollama chatbot using the provided prompt and chat history.
    """
    try:
        response = ollama.chat(model="llama2", messages=history + [{"role": "user", "content": prompt}])
        return response.message.content
    except Exception as e:
        return f"Error: {e}"

def save_conversation_to_file(chat_history):
    """
    Save the conversation history to a text file.
    """
    with open("chat_history.txt", "a") as file:
        for message in chat_history:
            role = message["role"].capitalize()
            content = message["content"]
            file.write(f"{role}: {content}\n")
        file.write("\n--- End of Conversation ---\n\n")

def print_welcome_message():
    """
    Print a welcome message and basic instructions.
    """
    print("Hi! How can I help?")
    print("Type 'help' for commands, 'clear' to reset, or 'exit' to quit.")

def chat_with_ollama():
    """
    Start a chat with Ollama chatbot.
    """
    print_welcome_message()
    chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("")
            save_conversation_to_file(chat_history)
            break
        elif user_input.lower() == "help":
            print("Commands: 'help', 'clear', 'exit'.")
            print("")
            continue
        elif user_input.lower() == "clear":
            print("Chat reset.")
            print("")
            chat_history = [{"role": "system", "content": "Layla is determined, analytical, and driven by a deep sense of responsibility. Though reserved, she is empathetic and strives to use technology for the greater good."}]
            continue
        
        # Get response from Ollama
        start_time = time.time()
        response = get_ollama_response(user_input, chat_history)
        
        # Timeout check
        if time.time() - start_time > 10:
            response = "Timeout. Please try again."
        
        # Update chat history
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": response})
        
        print("Bot: " + response)
        print("")

if __name__ == "__main__":
    chat_with_ollama()
