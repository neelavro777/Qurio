import sys
from src.agent.loop import run_agent
from src.utils.logger import logger

def main():
    """
    Main entry point for the Qurio Agent.
    """
    print("Welcome to Qurio - Your Reasoning Assistant")
    print("-" * 40)
    
    # Check if a task was provided via command line arguments
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
    else:
        # Otherwise, ask the user for a task
        task = input("What can I help you with today? (e.g., 'What is 34 * 12?')\n> ")

    if not task.strip():
        logger.warning("No task provided. Exiting.")
        return

    try:
        # Run the agent
        # You can also customize max_steps here if needed
        result = run_agent(task)
        
        print("\n" + "=" * 40)
        print(f"RESULT: {result}")
        print("=" * 40)

    except KeyboardInterrupt:
        print("\nInterrupted by user. Goodbye!")
    except Exception as e:
        logger.critical(f"A fatal error occurred at the entry point: {e}")
        print(f"\nSorry, something went wrong. Check the logs for details.")

if __name__ == "__main__":
    main()