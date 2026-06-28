from agent.stock_agent import analyse_stock

def main():
    print("=== 📈 Stock Analysis Agent — Phase 1 ===")
    print("Type a stock ticker to analyse, or 'quit' to exit.\n")

    while True:
        ticker = input("Enter stock ticker (e.g. TCS.NS, LTF.NS): ").strip()

        # ignore empty input
        if not ticker:
            print("⚠️  Please enter a ticker symbol.\n")
            continue

        # exit condition
        if ticker.lower() in ("quit", "exit", "q"):
            print("👋 Goodbye!")
            break

        print()
        result = analyse_stock(ticker)

        print("\n" + "=" * 50)
        print(result)
        print("=" * 50 + "\n")

if __name__ == "__main__":
    main()