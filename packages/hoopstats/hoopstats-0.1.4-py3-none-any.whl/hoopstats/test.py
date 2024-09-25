from hoopstats import PlayerScraper


def main():
    print("NBA Player Stats Fetcher")

    while True:
        try:
            # Continuously ask for input
            name = (
                input("Enter player name or type 'exit' to quit): ").strip().split(" ")
            )
            if name[0].lower() == "exit":
                print("Exiting program.")
                break

            playerScraper = PlayerScraper(name[0], name[1])

            stat_type = input(
                "Enter stat type (e.g., 'per_game', 'totals', 'advanced'): "
            ).strip()

            # Fetch and display player stats
            if stat_type:
                print(playerScraper.get_stats_by_year(stat_type=stat_type))
            else:
                print(playerScraper.get_stats_by_year())

            print(playerScraper.get_game_log_by_year(2024))
        except KeyboardInterrupt:
            print("\nKeyboard exit. Exiting program.")
            break


if __name__ == "__main__":
    main()
