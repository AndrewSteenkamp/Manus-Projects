from default_api import omni_search

def search_youtube_content(keywords, num_results_per_keyword=5):
    """Performs targeted searches for YouTube channels and content.

    Args:
        keywords (list): A list of keywords to search for.
        num_results_per_keyword (int): The number of search results to retrieve per keyword.

    Returns:
        dict: A dictionary where keys are keywords and values are lists of search results.
    """
    all_results = {}
    for keyword in keywords:
        print(f"Searching for: {keyword}")
        try:
            # Use omni_search to find YouTube content. We'll assume 'info' search type is sufficient
            # for finding general web pages that might link to YouTube channels or videos.
            # In a real scenario, direct YouTube API integration would be ideal.
            search_query = f"YouTube channel {keyword}"
            results = omni_search(
                brief=f"Searching YouTube content for '{keyword}'",
                queries=[search_query],
                search_type="info"
            )
            # Process results to extract relevant information. This is a simplified example.
            web_results = results.get("webpage_results", [])
            # Limit the number of results per keyword
            all_results[keyword] = web_results[:num_results_per_keyword]
            print(f"Found {len(all_results[keyword])} results for '{keyword}'")
        except Exception as e:
            print(f"Error searching for '{keyword}': {e}")
            all_results[keyword] = []
    return all_results

if __name__ == "__main__":
    # Example usage with dummy keywords
    from keyword_generator import generate_keywords

    hobby = "baking"
    keywords = generate_keywords(hobby)[:5] # Get top 5 keywords for demonstration

    print(f"\nPerforming YouTube search for hobby: {hobby}")
    search_results = search_youtube_content(keywords)

    for keyword, results in search_results.items():
        print(f"\n--- Results for '{keyword}' ---")
        if results:
            for i, result in enumerate(results):
                print(f"  {i+1}. Title: {result.get('Title', 'N/A')}")
                print(f"     URL: {result.get('URL', 'N/A')}")
        else:
            print("  No results found.")

    hobby = "vintage video games"
    keywords = generate_keywords(hobby)[:5] # Get top 5 keywords for demonstration

    print(f"\nPerforming YouTube search for hobby: {hobby}")
    search_results = search_youtube_content(keywords)

    for keyword, results in search_results.items():
        print(f"\n--- Results for '{keyword}' ---")
        if results:
            for i, result in enumerate(results):
                print(f"  {i+1}. Title: {result.get('Title', 'N/A')}")
                print(f"     URL: {result.get('URL', 'N/A')}")
        else:
            print("  No results found.")


