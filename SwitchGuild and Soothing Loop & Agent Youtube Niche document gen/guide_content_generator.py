def generate_youtube_guide_content(niche_suggestion=None):
    """Generates the core content for the step-by-step YouTube channel guide.

    Args:
        niche_suggestion (dict, optional): A dictionary containing niche details
                                           to personalize the guide. Defaults to None.

    Returns:
        str: Markdown formatted content for the guide.
    """
    guide_content = "# Step-by-Step Guide to Starting Your YouTube Channel\n\n"
    guide_content += "This comprehensive guide will walk you through every essential step to launch and grow your YouTube channel. Whether you're a complete beginner or looking to refine your strategy, this guide provides actionable insights and best practices.\n\n"

    if niche_suggestion:
        guide_content += f"## Your Niche: {niche_suggestion.get('name', 'Undefined Niche')}\n\n"
        guide_content += f"Based on your interests, we've identified **{niche_suggestion.get('name', 'a promising niche')}** for your YouTube channel. This niche offers {niche_suggestion.get('potential', 'great potential')} due to {niche_suggestion.get('reason', 'its unique characteristics')}. Below, we'll integrate specific examples relevant to this niche to help you get started.\n\n"

    guide_content += "## 1. Define Your Channel's Foundation\n\n"
    guide_content += "Before you even think about recording, it's crucial to lay a strong foundation for your channel. This involves understanding your purpose, target audience, and unique value proposition.\n\n"
    guide_content += "### 1.1. Clarify Your 'Why'\n\n"
    guide_content += "Why do you want to start a YouTube channel? Is it to share knowledge, entertain, build a community, or generate income? Your 'why' will be your guiding star through the challenges of content creation.\n\n"
    guide_content += "### 1.2. Identify Your Target Audience\n\n"
    guide_content += "Who are you trying to reach? Understanding your ideal viewer – their demographics, interests, pain points, and what they seek on YouTube – is paramount. This will inform your content, tone, and promotion strategies.\n\n"
    guide_content += "### 1.3. Craft Your Unique Value Proposition (UVP)\n\n"
    guide_content += "What makes your channel different? In a crowded YouTube landscape, your UVP is what sets you apart. It could be your unique perspective, a specific content format, or a niche within a niche.\n\n"

    guide_content += "## 2. Channel Setup and Branding\n\n"
    guide_content += "Once your foundation is solid, it's time to set up your YouTube channel and establish a strong brand identity.\n\n"
    guide_content += "### 2.1. Create Your YouTube Channel\n\n"
    guide_content += "If you don't have one, create a Google account. Then, go to YouTube and create a new channel. Choose a 'Brand Account' for more flexibility and collaboration options.\n\n"
    guide_content += "### 2.2. Choose a Memorable Channel Name\n\n"
    guide_content += "Your channel name should be relevant to your niche, easy to remember, and unique. Check for availability on YouTube and other social media platforms.\n\n"
    guide_content += "### 2.3. Design Your Channel Art\n\n"
    guide_content += "This includes your channel banner, profile picture, and video watermarks. These visual elements are crucial for brand recognition and conveying your channel's theme. Use tools like Canva or Photoshop.\n\n"
    guide_content += "### 2.4. Write a Compelling Channel Description\n\n"
    guide_content += "In your 'About' section, clearly explain what your channel is about, who it's for, and what viewers can expect. Include relevant keywords to help with discoverability.\n\n"

    guide_content += "## 3. Content Planning and Ideation\n\n"
    guide_content += "Content is king on YouTube. A well-thought-out content strategy is vital for consistent growth.\n\n"
    guide_content += "### 3.1. Brainstorm Video Ideas\n\n"
    guide_content += "Think about topics within your niche that your target audience would find valuable or entertaining. Look at trending topics, common questions, and what your competitors are doing (and not doing).\n\n"
    guide_content += "### 3.2. Create a Content Calendar\n\n"
    guide_content += "Plan your video releases in advance. A content calendar helps you stay organized, consistent, and ensures a steady flow of content. Include topics, target release dates, and key milestones.\n\n"
    guide_content += "### 3.3. Outline Your Videos\n\n"
    guide_content += "Before recording, create a detailed outline or script for each video. This ensures you cover all key points, maintain a logical flow, and stay on message.\n\n"

    guide_content += "## 4. Basic Video Production\n\n"
    guide_content += "You don't need expensive equipment to start, but understanding the basics of recording and editing is essential.\n\n"
    guide_content += "### 4.1. Equipment Essentials\n\n"
    guide_content += "Start with what you have: a smartphone, a basic webcam, or a DSLR camera. Invest in a good microphone as audio quality is often more important than video quality. Ensure good lighting.\n\n"
    guide_content += "### 4.2. Recording Your Content\n\n"
    guide_content += "Choose a quiet, well-lit space. Speak clearly and confidently. Practice your delivery. For screen recordings, use software like OBS Studio.\n\n"
    guide_content += "### 4.3. Video Editing Basics\n\n"
    guide_content += "Learn a basic video editing software (e.g., DaVinci Resolve, Shotcut, iMovie). Focus on trimming, adding text overlays, background music, and basic color correction. Keep your edits clean and engaging.\n\n"

    guide_content += "## 5. YouTube Optimization (SEO)\n\n"
    guide_content += "To get discovered, your videos need to be optimized for YouTube's search algorithm.\n\n"
    guide_content += "### 5.1. Keyword Research for Videos\n\n"
    guide_content += "Use tools like TubeBuddy, vidIQ, or Google Keyword Planner to find relevant keywords for each video. Integrate these naturally into your title, description, and tags.\n\n"
    guide_content += "### 5.2. Craft Compelling Titles\n\n"
    guide_content += "Your title should be catchy, include your main keyword, and accurately reflect your video's content. Aim for clarity and curiosity.\n\n"
    guide_content += "### 5.3. Write Detailed Descriptions\n\n"
    guide_content += "Provide a comprehensive description of your video, including keywords, timestamps, links to resources, and a call to action. This helps YouTube understand your content and improves discoverability.\n\n"
    guide_content += "### 5.4. Use Relevant Tags\n\n"
    guide_content += "Tags help YouTube categorize your video. Use a mix of broad and specific tags relevant to your content and niche.\n\n"
    guide_content += "### 5.5. Design Engaging Thumbnails\n\n"
    guide_content += "Your thumbnail is often the first thing viewers see. Make it visually appealing, clear, and intriguing. Use bright colors, clear text, and expressive faces.\n\n"

    guide_content += "## 6. Audience Engagement and Community Building\n\n"
    guide_content += "Building a loyal community is key to long-term success on YouTube.\n\n"
    guide_content += "### 6.1. Respond to Comments\n\n"
    guide_content += "Engage with your viewers by responding to comments. This shows you value their input and helps build a relationship.\n\n"
    guide_content += "### 6.2. Ask for Engagement\n\n"
    guide_content += "Encourage viewers to like, comment, share, and subscribe in your videos. Ask questions to spark discussion.\n\n"
    guide_content += "### 6.3. Use Community Tab and Social Media\n\n"
    guide_content += "Extend your reach beyond videos. Use YouTube's Community tab for polls and updates, and promote your content on other social media platforms.\n\n"

    guide_content += "## 7. Monetization Strategies\n\n"
    guide_content += "Once you meet YouTube's eligibility requirements, you can start monetizing your channel.\n\n"
    guide_content += "### 7.1. YouTube Partner Program (YPP)\n\n"
    guide_content += "Earn revenue from ads displayed on your videos. Requires meeting subscriber and watch time thresholds.\n\n"
    guide_content += "### 7.2. Affiliate Marketing\n\n"
    guide_content += "Promote products or services you use and trust, earning a commission on sales made through your unique links.\n\n"
    guide_content += "### 7.3. Selling Your Own Products/Services\n\n"
    guide_content += "Create and sell digital products (e.g., e-books, courses, templates) or physical merchandise related to your niche.\n\n"
    guide_content += "### 7.4. Sponsorships and Brand Deals\n\n"
    guide_content += "Collaborate with brands for sponsored content. This typically requires a dedicated and engaged audience.\n\n"

    guide_content += "## Conclusion\n\n"
    guide_content += "Starting a YouTube channel is a journey that requires dedication, consistency, and continuous learning. By following this step-by-step guide, you'll be well-equipped to build a successful channel that resonates with your audience and achieves your goals. Good luck!\n"

    return guide_content

if __name__ == "__main__":
    # Example with a generic guide
    generic_guide = generate_youtube_guide_content()
    with open("youtube_guide_generic.md", "w") as f:
        f.write(generic_guide)
    print("Generic YouTube guide generated: youtube_guide_generic.md")

    # Example with a personalized guide for 'baking' niche
    baking_niche = {
        "name": "Artisan Bread Baking for Beginners",
        "potential": "high demand for home baking tutorials",
        "reason": "many aspiring bakers seek clear, step-by-step instructions and troubleshooting tips"
    }
    personalized_guide = generate_youtube_guide_content(baking_niche)
    with open("youtube_guide_baking.md", "w") as f:
        f.write(personalized_guide)
    print("Personalized YouTube guide for baking generated: youtube_guide_baking.md")


