def generate_lofi_metadata(title_prefix, duration_minutes, keywords=None):
    """Generates metadata for a Lo-fi music video.

    Args:
        title_prefix (str): Main part of the video title (e.g., "Cozy Rain Lo-fi").
        duration_minutes (int): Duration of the video in minutes.
        keywords (list): Additional keywords for tags.

    Returns:
        dict: A dictionary containing title, description, and tags.
    """
    title = f"{title_prefix} | {duration_minutes} Minute Lo-fi Study/Relax Music"
    description = (
        f"Immerse yourself in {duration_minutes} minutes of calming Lo-fi music, perfect for studying, relaxing, or sleeping. "
        "Let the gentle beats and soothing melodies create the perfect ambiance for your focus and tranquility."
    )
    tags = ["lofi", "lofi hip hop", "study music", "relaxing music", "chill beats", "sleep music", "ambient", "focus music", "instrumental"]
    if keywords:
        tags.extend(keywords)
    return {"title": title, "description": description, "tags": ", ".join(tags)}

def generate_baby_sound_metadata(sound_type, duration_minutes, keywords=None):
    """Generates metadata for a baby sound/white noise video.

    Args:
        sound_type (str): Type of sound (e.g., "White Noise", "Rain Sound", "Lullaby").
        duration_minutes (int): Duration of the video in minutes.
        keywords (list): Additional keywords for tags.

    Returns:
        dict: A dictionary containing title, description, and tags.
    """
    title = f"{sound_type} for Baby Sleep | {duration_minutes} Minute Soothing Sound"
    description = (
        f"Help your baby sleep soundly with {duration_minutes} minutes of {sound_type}. "
        "This continuous, calming sound is designed to mask distractions and create a peaceful environment for your little one to rest."
    )
    tags = ["baby sleep", "white noise", "baby sounds", "soothing sounds", "sleep aid", "newborn sleep", "lullaby", "calming sounds"]
    if keywords:
        tags.extend(keywords)
    return {"title": title, "description": description, "tags": ", ".join(tags)}

if __name__ == "__main__":
    # Example Lo-fi metadata
    lofi_meta = generate_lofi_metadata("Rainy Day Chill", 180, ["rain", "cozy", "fireplace"])
    print("\n--- Lo-fi Video Metadata ---")
    print(f"Title: {lofi_meta['title']}")
    print(f"Description: {lofi_meta['description']}")
    print(f"Tags: {lofi_meta['tags']}")

    # Example Baby Sound metadata
    baby_meta = generate_baby_sound_metadata("Pink Noise", 360, ["infant sleep", "pink noise machine"])
    print("\n--- Baby Sound Video Metadata ---")
    print(f"Title: {baby_meta['title']}")
    print(f"Description: {baby_meta['description']}")
    print(f"Tags: {baby_meta['tags']}")


