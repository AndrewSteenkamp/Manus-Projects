def generate_keywords(hobby):
    """Generates relevant keywords and search terms from a user's hobby.

    Args:
        hobby (str): The user's hobby or interest.

    Returns:
        list: A list of generated keywords and search terms.
    """
    keywords = [
        hobby,
        f"{hobby} YouTube channel",
        f"{hobby} tutorial",
        f"{hobby} guide",
        f"best {hobby} channels",
        f"how to {hobby}",
        f"{hobby} tips and tricks",
        f"{hobby} for beginners",
        f"{hobby} community",
        f"learn {hobby}",
        f"{hobby} ideas",
        f"{hobby} review",
        f"{hobby} gear",
        f"{hobby} setup",
        f"{hobby} projects",
        f"{hobby} challenges",
        f"{hobby} inspiration",
        f"{hobby} vlog",
        f"{hobby} podcast",
        f"{hobby} automation",
        f"{hobby} monetization",
        f"profitable {hobby} niche",
        f"{hobby} audience",
        f"{hobby} competition",
        f"{hobby} trends",
        f"{hobby} market",
        f"{hobby} content ideas",
        f"{hobby} content creation",
        f"{hobby} channel growth",
        f"{hobby} tips",
        f"{hobby} tricks",
        f"{hobby} hacks",
        f"{hobby} secrets",
        f"{hobby} masterclass",
        f"{hobby} course",
        f"{hobby} online",
        f"{hobby} community",
        f"{hobby} forum",
        f"{hobby} blog",
        f"{hobby} website",
        f"{hobby} resources",
        f"{hobby} tools",
        f"{hobby} equipment",
        f"{hobby} supplies",
        f"{hobby} accessories",
        f"{hobby} products",
        f"{hobby} services",
        f"{hobby} business",
        f"{hobby} entrepreneur",
        f"{hobby} startup",
        f"{hobby} passive income",
        f"{hobby} online business",
        f"{hobby} digital product",
        f"{hobby} course",
        f"{hobby} ebook",
        f"{hobby} guide",
        f"{hobby} template",
        f"{hobby} checklist",
        f"{hobby} resource",
        f"{hobby} toolkit",
        f"{hobby} software",
        f"{hobby} app",
        f"{hobby} platform",
        f"{hobby} community",
        f"{hobby} forum",
        f"{hobby} blog",
        f"{hobby} website",
        f"{hobby} resources",
        f"{hobby} tools",
        f"{hobby} equipment",
        f"{hobby} supplies",
        f"{hobby} accessories",
        f"{hobby} products",
        f"{hobby} services",
        f"{hobby} business",
        f"{hobby} entrepreneur",
        f"{hobby} startup",
        f"{hobby} passive income",
        f"{hobby} online business",
        f"{hobby} digital product",
        f"{hobby} course",
        f"{hobby} ebook",
        f"{hobby} guide",
        f"{hobby} template",
        f"{hobby} checklist",
        f"{hobby} resource",
        f"{hobby} toolkit",
        f"{hobby} software",
        f"{hobby} app",
        f"{hobby} platform",
    ]
    return list(set(keywords)) # Remove duplicates

if __name__ == "__main__":
    hobby = "baking"
    generated_keywords = generate_keywords(hobby)
    print(f"Keywords for '{hobby}':")
    for keyword in generated_keywords:
        print(f"- {keyword}")

    hobby = "vintage video games"
    generated_keywords = generate_keywords(hobby)
    print(f"\nKeywords for '{hobby}':")
    for keyword in generated_keywords:
        print(f"- {keyword}")


