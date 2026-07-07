from agent import build_agent

def main():
    print("=== 📈 FinVeda Stock Analysis — Phase 3 ===")
    print("True Agentic AI — LLM drives the flow\n")

    agent = build_agent()

    while True:
        ticker = input("Enter stock ticker (e.g. TCS.NS, LTF.NS): ").strip()

        if not ticker:
            print("⚠️  Please enter a ticker symbol.\n")
            continue

        if ticker.lower() in ("quit", "exit", "q"):
            print("👋 Goodbye!")
            break

        print()

        # Invoke the agent with just the ticker
        # LLM decides which tools to call and when
        # Java analogy: jobLauncher.run(job, jobParameters)
        response = agent.invoke({
            "messages": [
                {"role": "user", "content": f"Analyse this stock: {ticker}"}
            ]
        })

        # Final message is always the LLM's last response
        final_message = response["messages"][-1].content

        print("\n" + "=" * 50)
        print(final_message)
        print("=" * 50 + "\n")

if __name__ == "__main__":
    main()