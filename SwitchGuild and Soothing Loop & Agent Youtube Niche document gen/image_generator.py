import os

def generate_video_image(prompt, output_path, aspect_ratio='landscape'):
    """Generates a static image for a video based on a prompt."""
    try:
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Direct call to the media_generate_image tool
        print(default_api.media_generate_image(
            brief=f"Generating image for video: {prompt}",
            images=[{'path': output_path, 'prompt': prompt, 'aspect_ratio': aspect_ratio}]
        ))

    except Exception as e:
        print(f"Error generating image: {e}")

if __name__ == "__main__":
    # Example usage:
    # Generate an image for a Lo-fi video
    generate_video_image(
        prompt="A cozy, dimly lit room with a window showing gentle rain, a warm cup of tea on a desk, and a subtle glow from a laptop. Lo-fi aesthetic, calm colors.",
        output_path="lofi_video_background.png",
        aspect_ratio="landscape"
    )

    # Generate an image for a baby sounds video
    generate_video_image(
        prompt="A peaceful nursery with soft pastel colors, a sleeping baby in a crib, and a gentle, warm light. Dreamy, calming atmosphere.",
        output_path="baby_sound_video_background.png",
        aspect_ratio="landscape"
    )

    # Generate an image for a white noise video
    generate_video_image(
        prompt="Abstract pattern of soft, swirling white and grey colors, minimalist, calming, suitable for background noise video.",
        output_path="white_noise_video_background.png",
        aspect_ratio="landscape"
    )


