#!/usr/bin/env python3
"""
TDI VIDEO ASSEMBLER & SYNCHRONIZATION SYSTEM
Complete video production system that combines audio, visuals, and text overlays
"""

import os
import json
from datetime import datetime
import subprocess
from moviepy.editor import *
from moviepy.video.fx import resize, fadein, fadeout
from moviepy.audio.fx import audio_fadein, audio_fadeout
import numpy as np

class TDIVideoAssembler:
    def __init__(self):
        self.base_dir = "/home/ubuntu/tdi_video_production"
        self.assets_dir = "/home/ubuntu/tdi_visual_assets"
        self.output_dir = os.path.join(self.base_dir, "final_videos")
        self.temp_dir = os.path.join(self.base_dir, "temp")
        
        # Create directories
        for directory in [self.base_dir, self.output_dir, self.temp_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Video specifications
        self.video_specs = {
            'width': 1920,
            'height': 1080,
            'fps': 30,
            'duration': 480,  # 8 minutes default
            'codec': 'libx264',
            'audio_codec': 'aac'
        }
        
        print(f"🎬 TDI Video Assembler initialized")
        print(f"📁 Output directory: {self.output_dir}")
    
    def create_background_video(self, duration):
        """Create a professional background video clip"""
        
        # Use the professional newsroom background
        bg_image_path = os.path.join(self.assets_dir, "backgrounds", "professional_newsroom.png")
        
        if os.path.exists(bg_image_path):
            # Create video clip from background image
            bg_clip = ImageClip(bg_image_path, duration=duration)
            bg_clip = bg_clip.resize((self.video_specs['width'], self.video_specs['height']))
            
            # Add subtle zoom effect for dynamic feel
            def zoom_effect(get_frame, t):
                frame = get_frame(t)
                zoom_factor = 1 + 0.02 * np.sin(t * 0.1)  # Subtle breathing effect
                return resize(frame, zoom_factor)
            
            bg_clip = bg_clip.fl(zoom_effect)
        else:
            # Fallback: create solid color background
            bg_clip = ColorClip(
                size=(self.video_specs['width'], self.video_specs['height']),
                color=(30, 58, 138),  # TDI blue
                duration=duration
            )
        
        return bg_clip
    
    def create_title_sequence(self, title, duration=5):
        """Create opening title sequence"""
        
        # Background
        bg = ColorClip(
            size=(self.video_specs['width'], self.video_specs['height']),
            color=(30, 58, 138),
            duration=duration
        )
        
        # Title text
        title_clip = TextClip(
            title,
            fontsize=72,
            color='white',
            font='Arial-Bold',
            size=(1600, None)
        ).set_position('center').set_duration(duration)
        
        # TDI branding
        branding_clip = TextClip(
            "TDI - TRENDING DAILY INSIGHTS",
            fontsize=36,
            color='white',
            font='Arial',
        ).set_position(('center', 'bottom')).set_duration(duration)
        
        # Combine with fade effects
        title_sequence = CompositeVideoClip([
            bg,
            title_clip.crossfadein(1).crossfadeout(1),
            branding_clip.crossfadein(1).crossfadeout(1)
        ])
        
        return title_sequence
    
    def create_scene_with_visuals(self, background, visual_asset, text_overlay, audio_segment, start_time, duration):
        """Create a scene combining background, visuals, text, and audio"""
        
        scene_clips = []
        
        # Background video
        bg_clip = background.subclip(start_time, start_time + duration)
        scene_clips.append(bg_clip)
        
        # Visual asset (map, chart, etc.)
        if visual_asset and os.path.exists(visual_asset):
            visual_clip = ImageClip(visual_asset, duration=duration)
            visual_clip = visual_clip.resize(height=600).set_position(('right', 'center'))
            visual_clip = visual_clip.crossfadein(0.5).crossfadeout(0.5)
            scene_clips.append(visual_clip)
        
        # Text overlay
        if text_overlay and os.path.exists(text_overlay):
            overlay_clip = ImageClip(text_overlay, duration=duration)
            overlay_clip = overlay_clip.set_position('center')
            overlay_clip = overlay_clip.crossfadein(0.5).crossfadeout(0.5)
            scene_clips.append(overlay_clip)
        
        # Combine all visual elements
        scene = CompositeVideoClip(scene_clips)
        
        # Add audio if provided
        if audio_segment:
            scene = scene.set_audio(audio_segment)
        
        return scene
    
    def create_lower_third_scene(self, background, text, start_time, duration):
        """Create a scene with lower third graphics"""
        
        # Background
        bg_clip = background.subclip(start_time, start_time + duration)
        
        # Lower third background
        lower_third_bg = ColorClip(
            size=(1920, 200),
            color=(30, 58, 138, 200),  # Semi-transparent blue
            duration=duration
        ).set_position(('center', 'bottom'))
        
        # TDI logo area
        logo_bg = ColorClip(
            size=(250, 180),
            color=(59, 130, 246),
            duration=duration
        ).set_position((50, 900))
        
        # TDI text
        tdi_text = TextClip(
            "TDI",
            fontsize=48,
            color='white',
            font='Arial-Bold'
        ).set_position((60, 920)).set_duration(duration)
        
        # Subtitle
        subtitle_text = TextClip(
            "TRENDING DAILY\nINSIGHTS",
            fontsize=24,
            color='white',
            font='Arial'
        ).set_position((60, 980)).set_duration(duration)
        
        # Main text
        main_text = TextClip(
            text,
            fontsize=36,
            color='white',
            font='Arial',
            size=(1400, None)
        ).set_position((350, 940)).set_duration(duration)
        
        # Combine all elements
        scene = CompositeVideoClip([
            bg_clip,
            lower_third_bg.crossfadein(0.5).crossfadeout(0.5),
            logo_bg.crossfadein(0.5).crossfadeout(0.5),
            tdi_text.crossfadein(0.5).crossfadeout(0.5),
            subtitle_text.crossfadein(0.5).crossfadeout(0.5),
            main_text.crossfadein(0.5).crossfadeout(0.5)
        ])
        
        return scene
    
    def create_subscribe_outro(self, duration=10):
        """Create subscribe call-to-action outro"""
        
        # Background
        bg = ColorClip(
            size=(self.video_specs['width'], self.video_specs['height']),
            color=(30, 58, 138),
            duration=duration
        )
        
        # Main message
        main_text = TextClip(
            "SUBSCRIBE FOR DAILY\nGEOPOLITICAL INSIGHTS",
            fontsize=64,
            color='white',
            font='Arial-Bold',
            method='caption',
            size=(1600, None)
        ).set_position('center').set_duration(duration)
        
        # Channel name
        channel_text = TextClip(
            "TRENDING DAILY INSIGHTS",
            fontsize=48,
            color='white',
            font='Arial'
        ).set_position(('center', 'bottom')).set_duration(duration)
        
        # Subscribe button simulation
        button_bg = ColorClip(
            size=(300, 80),
            color=(255, 0, 0),  # YouTube red
            duration=duration
        ).set_position(('center', 700))
        
        button_text = TextClip(
            "SUBSCRIBE",
            fontsize=32,
            color='white',
            font='Arial-Bold'
        ).set_position(('center', 720)).set_duration(duration)
        
        # Combine elements
        outro = CompositeVideoClip([
            bg,
            main_text.crossfadein(1),
            channel_text.crossfadein(1),
            button_bg.crossfadein(1),
            button_text.crossfadein(1)
        ])
        
        return outro
    
    def assemble_complete_video(self, video_data):
        """Assemble complete video from all components"""
        
        title = video_data['title']
        script_segments = video_data['script_segments']
        visual_assets = video_data['visual_assets']
        audio_file = video_data.get('audio_file')
        
        print(f"\n🎬 Assembling video: {title}")
        
        # Calculate total duration
        total_duration = sum(segment['duration'] for segment in script_segments)
        
        # Create background video
        background = self.create_background_video(total_duration + 15)  # Extra for intro/outro
        
        # Create video segments
        video_segments = []
        current_time = 0
        
        # 1. Title sequence (5 seconds)
        title_seq = self.create_title_sequence(title, 5)
        video_segments.append(title_seq)
        current_time += 5
        
        # 2. Main content segments
        for i, segment in enumerate(script_segments):
            segment_duration = segment['duration']
            
            if segment['type'] == 'analysis':
                # Analysis scene with visuals
                visual_asset = visual_assets.get(f'chart_{i+1}') or visual_assets.get('world_map')
                text_overlay = visual_assets.get('lower_third')
                
                scene = self.create_scene_with_visuals(
                    background, visual_asset, text_overlay, None, current_time, segment_duration
                )
            
            elif segment['type'] == 'introduction':
                # Introduction with lower third
                scene = self.create_lower_third_scene(
                    background, segment['text'][:100], current_time, segment_duration
                )
            
            elif segment['type'] == 'statistics':
                # Statistics display
                stat_overlay = visual_assets.get('statistic_1')
                scene = self.create_scene_with_visuals(
                    background, None, stat_overlay, None, current_time, segment_duration
                )
            
            else:
                # Default scene
                scene = background.subclip(current_time, current_time + segment_duration)
            
            video_segments.append(scene)
            current_time += segment_duration
        
        # 3. Subscribe outro (10 seconds)
        outro = self.create_subscribe_outro(10)
        video_segments.append(outro)
        
        # Combine all segments
        final_video = concatenate_videoclips(video_segments, method="compose")
        
        # Add audio if provided
        if audio_file and os.path.exists(audio_file):
            audio = AudioFileClip(audio_file)
            # Adjust audio duration to match video
            if audio.duration > final_video.duration:
                audio = audio.subclip(0, final_video.duration)
            elif audio.duration < final_video.duration:
                # Loop audio if too short
                audio = audio.loop(duration=final_video.duration)
            
            final_video = final_video.set_audio(audio)
        
        # Export final video
        safe_title = title.replace(' ', '_').replace(':', '').replace('?', '')[:30]
        date_str = datetime.now().strftime("%Y%m%d")
        output_filename = f"TDI_{safe_title}_{date_str}.mp4"
        output_path = os.path.join(self.output_dir, output_filename)
        
        print(f"🎥 Rendering video: {output_filename}")
        print("⏳ This may take several minutes...")
        
        final_video.write_videofile(
            output_path,
            fps=self.video_specs['fps'],
            codec=self.video_specs['codec'],
            audio_codec=self.video_specs['audio_codec'],
            temp_audiofile=os.path.join(self.temp_dir, 'temp_audio.m4a'),
            remove_temp=True,
            verbose=False,
            logger=None
        )
        
        print(f"✅ Video completed: {output_path}")
        
        # Create video metadata
        metadata = {
            'title': title,
            'filename': output_filename,
            'path': output_path,
            'duration': final_video.duration,
            'resolution': f"{self.video_specs['width']}x{self.video_specs['height']}",
            'fps': self.video_specs['fps'],
            'created': datetime.now().isoformat(),
            'segments': len(script_segments),
            'visual_assets_used': list(visual_assets.keys())
        }
        
        metadata_path = os.path.join(self.output_dir, f"{safe_title}_metadata_{date_str}.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return {
            'video_path': output_path,
            'metadata_path': metadata_path,
            'metadata': metadata
        }

def create_sample_video():
    """Create a sample video for testing"""
    
    assembler = TDIVideoAssembler()
    
    # Sample video data
    sample_video = {
        'title': 'Ukraine War Economic Impact: Global Market Analysis',
        'script_segments': [
            {
                'type': 'introduction',
                'text': 'Welcome to Trending Daily Insights. Today we analyze the economic impact of the Ukraine war.',
                'duration': 30
            },
            {
                'type': 'analysis',
                'text': 'The conflict has disrupted global supply chains and energy markets.',
                'duration': 60
            },
            {
                'type': 'statistics',
                'text': 'Economic losses exceed 2.1 trillion euros across affected regions.',
                'duration': 30
            },
            {
                'type': 'analysis',
                'text': 'Energy prices have increased by 40% since the conflict began.',
                'duration': 60
            },
            {
                'type': 'analysis',
                'text': 'Looking ahead, we expect continued volatility in global markets.',
                'duration': 40
            }
        ],
        'visual_assets': {
            'world_map': '/home/ubuntu/tdi_visual_assets/maps/Ukraine_War_Economic_Impact_Gl_map_20250923.png',
            'chart_1': '/home/ubuntu/tdi_visual_assets/charts/Ukraine_War_Economic_Impact_Gl_chart_1_20250923.png',
            'chart_2': '/home/ubuntu/tdi_visual_assets/charts/Ukraine_War_Economic_Impact_Gl_chart_2_20250923.png',
            'lower_third': '/home/ubuntu/tdi_visual_assets/overlays/Ukraine_War_Economic_Impact_Gl_lower_third_20250923.png',
            'statistic_1': '/home/ubuntu/tdi_visual_assets/overlays/Ukraine_War_Economic_Impact_Gl_statistic_1_20250923.png'
        }
    }
    
    # Assemble the video
    result = assembler.assemble_complete_video(sample_video)
    
    print(f"\n🎉 Sample video creation complete!")
    print(f"📹 Video file: {result['video_path']}")
    print(f"📄 Metadata: {result['metadata_path']}")
    
    return result

if __name__ == "__main__":
    # Install required packages if not available
    try:
        import moviepy
    except ImportError:
        print("📦 Installing moviepy...")
        subprocess.run(["pip3", "install", "moviepy"], check=True)
        import moviepy
    
    # Create sample video
    result = create_sample_video()
    
    print("\n" + "="*60)
    print("🎬 TDI VIDEO ASSEMBLER - READY FOR PRODUCTION!")
    print("="*60)
