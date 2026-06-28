from graph import build_graph

def main():
    print("=== 📈 FinVeda Stock Analysis — Phase 2 ===")
    print("Multi-agent analysis powered by LangGraph\n")

    graph = build_graph()

    while True:
        ticker = input("Enter stock ticker (e.g. TCS.NS, LTF.NS): ").strip()

        if not ticker:
            print("⚠️  Please enter a ticker symbol.\n")
            continue

        if ticker.lower() in ("quit", "exit", "q"):
            print("👋 Goodbye!")
            break

        print()

        # Invoke the graph with initial state
        # Java analogy: jobLauncher.run(job, jobParameters)
        # We only set ticker — nodes will fill the rest
        final_state = graph.invoke({
            "ticker": ticker,
            "stock_data": None,
            "news": None,
            "recommendation": None
        })

        print("\n" + "=" * 50)
        print(final_state["recommendation"])
        print("=" * 50 + "\n")

if __name__ == "__main__":
    main()