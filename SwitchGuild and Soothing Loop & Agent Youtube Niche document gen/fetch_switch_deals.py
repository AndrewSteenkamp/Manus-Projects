from nintendeals.noa.listing import list_switch_games

def fetch_and_generate_deals_news():
    try:
        all_switch_games = list_switch_games()

        games_on_sale = []
        for game in all_switch_games:
            try:
                # Use the price() method to get price information for the US region
                price_info = game.price(country=\'US\')

                if price_info and price_info.sale_price and price_info.sale_price < price_info.normal_price:
                    game.sale_price = price_info.sale_price
                    game.normal_price = price_info.normal_price
                    games_on_sale.append(game)
            except Exception as e:
                # Some games might not have price info or throw errors, skip them
                # print(f"Could not get price for {game.title}: {e}")
                pass

        if not games_on_sale:
            return "No Nintendo Switch deals found at this time."

        # Sort games by discount percentage (descending)
        games_on_sale.sort(key=lambda x: (1 - (x.sale_price / x.normal_price)) if x.normal_price else 0, reverse=True)

        news_content = "# Nintendo Switch Deals of the Day!\n\n"
        news_content += "Here are some of the hottest deals on the Nintendo eShop:\n\n"

        for game in games_on_sale[:5]:  # Limit to top 5 deals for brevity
            title = game.title
            sale_price = game.sale_price
            normal_price = game.normal_price
            discount = f"{(1 - (sale_price / normal_price)) * 100:.0f}% off" if normal_price and normal_price > 0 else "N/A"
            # The \'url\' attribute is not directly available on the Game object from list_switch_games.
            # For now, we\'ll use a placeholder or try to construct a URL if possible.
            # A more robust solution might involve another API call or web scraping Deku Deals for the URL.
            game_url = f"https://www.nintendo.com/games/detail/{{game.nsuid}}/" if game.nsuid else "N/A"

            news_content += f"## {title}\n"
            news_content += f"*   **Sale Price:** ${sale_price:.2f}\n"
            news_content += f"*   **Original Price:** ${normal_price:.2f}\n"
            news_content += f"*   **Discount:** {discount}\n"
            news_content += f"*   **Link:** {game_url}\n\n"

        news_content += "Stay tuned for more amazing deals!\n"
        return news_content

    except Exception as e:
        return f"Error fetching Nintendo Switch deals: {e}"

if __name__ == "__main__":
    print("Fetching Nintendo Switch deals...")
    news = fetch_and_generate_deals_news()
    with open("switch_deals_news.md", "w") as f:
        f.write(news)
    print("News content generated in switch_deals_news.md")


