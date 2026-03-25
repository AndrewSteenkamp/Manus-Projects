#!/usr/bin/env python3
"""
TDI VISUAL ASSET GENERATOR
Automated system for creating professional visual assets for geopolitical videos
"""

import os
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import numpy as np

class TDIVisualGenerator:
    def __init__(self):
        self.base_dir = "/home/ubuntu/tdi_visual_assets"
        self.templates_dir = os.path.join(self.base_dir, "templates")
        self.generated_dir = os.path.join(self.base_dir, "generated")
        self.maps_dir = os.path.join(self.base_dir, "maps")
        self.charts_dir = os.path.join(self.base_dir, "charts")
        self.overlays_dir = os.path.join(self.base_dir, "overlays")
        
        # Ensure directories exist
        for directory in [self.generated_dir, self.maps_dir, self.charts_dir, self.overlays_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # TDI Brand Colors
        self.brand_colors = {
            'primary_blue': '#1E3A8A',
            'secondary_blue': '#3B82F6',
            'accent_blue': '#60A5FA',
            'white': '#FFFFFF',
            'light_gray': '#F3F4F6',
            'dark_gray': '#374151',
            'text_dark': '#1F2937'
        }
        
        print(f"🎨 TDI Visual Generator initialized")
        print(f"📁 Assets directory: {self.base_dir}")
    
    def create_world_map_highlight(self, regions_to_highlight, title, output_filename):
        """Create a world map with specific regions highlighted"""
        
        # Create figure
        fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
        fig.patch.set_facecolor(self.brand_colors['primary_blue'])
        
        # World map coordinates (simplified)
        world_regions = {
            'North America': {'coords': [(-140, 20), (-50, 70)], 'countries': ['USA', 'Canada', 'Mexico']},
            'Europe': {'coords': [(-10, 35), (40, 70)], 'countries': ['Germany', 'France', 'UK', 'Russia']},
            'Asia': {'coords': [(40, 10), (180, 70)], 'countries': ['China', 'India', 'Japan', 'Russia']},
            'Middle East': {'coords': [(25, 15), (65, 45)], 'countries': ['Saudi Arabia', 'Iran', 'Turkey', 'Israel']},
            'Africa': {'coords': [(-20, -35), (55, 35)], 'countries': ['Nigeria', 'South Africa', 'Egypt']},
            'South America': {'coords': [(-85, -55), (-35, 15)], 'countries': ['Brazil', 'Argentina', 'Colombia']},
            'Ukraine': {'coords': [(22, 44), (40, 52)], 'countries': ['Ukraine']},
            'China': {'coords': [(73, 18), (135, 53)], 'countries': ['China']},
            'Indo-Pacific': {'coords': [(90, -50), (180, 50)], 'countries': ['Australia', 'Indonesia', 'Philippines']}
        }
        
        # Draw base world map
        ax.set_xlim(-180, 180)
        ax.set_ylim(-90, 90)
        ax.set_facecolor(self.brand_colors['secondary_blue'])
        
        # Draw continents as rectangles (simplified representation)
        for region, data in world_regions.items():
            coords = data['coords']
            width = coords[1][0] - coords[0][0]
            height = coords[1][1] - coords[0][1]
            
            if region in regions_to_highlight:
                color = self.brand_colors['accent_blue']
                alpha = 0.8
                linewidth = 3
            else:
                color = self.brand_colors['light_gray']
                alpha = 0.4
                linewidth = 1
            
            rect = patches.Rectangle(
                coords[0], width, height,
                linewidth=linewidth, 
                edgecolor=self.brand_colors['white'],
                facecolor=color,
                alpha=alpha
            )
            ax.add_patch(rect)
        
        # Add title
        ax.text(0, 85, title, fontsize=24, fontweight='bold', 
                color=self.brand_colors['white'], ha='center')
        
        # Add TDI branding
        ax.text(-170, -80, 'TDI - TRENDING DAILY INSIGHTS', 
                fontsize=16, fontweight='bold', 
                color=self.brand_colors['white'])
        
        # Remove axes
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        # Save
        output_path = os.path.join(self.maps_dir, output_filename)
        plt.tight_layout()
        plt.savefig(output_path, dpi=100, bbox_inches='tight', 
                   facecolor=self.brand_colors['primary_blue'])
        plt.close()
        
        print(f"✅ World map created: {output_filename}")
        return output_path
    
    def create_data_chart(self, data, chart_type, title, output_filename):
        """Create professional data charts for geopolitical analysis"""
        
        fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
        fig.patch.set_facecolor(self.brand_colors['primary_blue'])
        ax.set_facecolor(self.brand_colors['light_gray'])
        
        if chart_type == 'bar':
            bars = ax.bar(data['labels'], data['values'], 
                         color=self.brand_colors['secondary_blue'],
                         edgecolor=self.brand_colors['white'],
                         linewidth=2)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                       f'{height:.1f}', ha='center', va='bottom',
                       fontsize=14, fontweight='bold',
                       color=self.brand_colors['text_dark'])
        
        elif chart_type == 'line':
            ax.plot(data['x'], data['y'], 
                   color=self.brand_colors['secondary_blue'],
                   linewidth=4, marker='o', markersize=8,
                   markerfacecolor=self.brand_colors['accent_blue'],
                   markeredgecolor=self.brand_colors['white'],
                   markeredgewidth=2)
            
            # Fill area under curve
            ax.fill_between(data['x'], data['y'], alpha=0.3,
                           color=self.brand_colors['secondary_blue'])
        
        elif chart_type == 'pie':
            colors = [self.brand_colors['secondary_blue'], 
                     self.brand_colors['accent_blue'],
                     self.brand_colors['light_gray']]
            wedges, texts, autotexts = ax.pie(data['values'], 
                                            labels=data['labels'],
                                            colors=colors,
                                            autopct='%1.1f%%',
                                            startangle=90,
                                            textprops={'fontsize': 14, 'fontweight': 'bold'})
        
        # Styling
        ax.set_title(title, fontsize=24, fontweight='bold', 
                    color=self.brand_colors['white'], pad=20)
        
        if chart_type != 'pie':
            ax.tick_params(colors=self.brand_colors['text_dark'], labelsize=12)
            ax.grid(True, alpha=0.3, color=self.brand_colors['dark_gray'])
        
        # Add TDI branding
        fig.text(0.02, 0.02, 'TDI - TRENDING DAILY INSIGHTS', 
                fontsize=14, fontweight='bold', 
                color=self.brand_colors['white'])
        
        # Save
        output_path = os.path.join(self.charts_dir, output_filename)
        plt.tight_layout()
        plt.savefig(output_path, dpi=100, bbox_inches='tight',
                   facecolor=self.brand_colors['primary_blue'])
        plt.close()
        
        print(f"✅ Chart created: {output_filename}")
        return output_path
    
    def create_text_overlay(self, text, overlay_type, output_filename):
        """Create text overlays for video scenes"""
        
        # Create image
        img = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Load fonts (using default if custom not available)
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
            body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
        
        if overlay_type == 'title':
            # Main title overlay
            bbox = draw.textbbox((0, 0), text, font=title_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (1920 - text_width) // 2
            y = (1080 - text_height) // 2
            
            # Background rectangle
            padding = 40
            draw.rectangle([x-padding, y-padding, x+text_width+padding, y+text_height+padding],
                          fill=(30, 58, 138, 200))  # Semi-transparent blue
            
            # Text
            draw.text((x, y), text, font=title_font, fill=(255, 255, 255, 255))
        
        elif overlay_type == 'lower_third':
            # Lower third overlay
            # Background bar
            draw.rectangle([0, 850, 1920, 1080], fill=(30, 58, 138, 220))
            
            # TDI logo area
            draw.rectangle([50, 870, 300, 1060], fill=(59, 130, 246, 255))
            draw.text((60, 900), "TDI", font=title_font, fill=(255, 255, 255, 255))
            draw.text((60, 980), "TRENDING DAILY", font=body_font, fill=(255, 255, 255, 255))
            draw.text((60, 1020), "INSIGHTS", font=body_font, fill=(255, 255, 255, 255))
            
            # Main text
            draw.text((350, 900), text, font=subtitle_font, fill=(255, 255, 255, 255))
        
        elif overlay_type == 'statistic':
            # Large statistic display
            lines = text.split('\n')
            if len(lines) >= 2:
                number = lines[0]
                description = lines[1]
                
                # Number
                bbox = draw.textbbox((0, 0), number, font=title_font)
                text_width = bbox[2] - bbox[0]
                x = (1920 - text_width) // 2
                draw.text((x, 400), number, font=title_font, fill=(59, 130, 246, 255))
                
                # Description
                bbox = draw.textbbox((0, 0), description, font=subtitle_font)
                text_width = bbox[2] - bbox[0]
                x = (1920 - text_width) // 2
                draw.text((x, 500), description, font=subtitle_font, fill=(255, 255, 255, 255))
        
        # Save
        output_path = os.path.join(self.overlays_dir, output_filename)
        img.save(output_path, 'PNG')
        
        print(f"✅ Text overlay created: {output_filename}")
        return output_path
    
    def generate_video_assets(self, topic_data):
        """Generate all visual assets for a video topic"""
        
        topic_title = topic_data['title']
        safe_title = topic_title.replace(' ', '_').replace(':', '').replace('?', '')[:30]
        date_str = datetime.now().strftime("%Y%m%d")
        
        assets = {
            'topic': topic_title,
            'date': date_str,
            'files': {}
        }
        
        print(f"\n🎬 Generating assets for: {topic_title}")
        
        # 1. Create world map with highlighted regions
        if 'regions' in topic_data:
            map_file = f"{safe_title}_map_{date_str}.png"
            map_path = self.create_world_map_highlight(
                topic_data['regions'], 
                topic_title,
                map_file
            )
            assets['files']['world_map'] = map_path
        
        # 2. Create data charts
        if 'chart_data' in topic_data:
            for i, chart in enumerate(topic_data['chart_data']):
                chart_file = f"{safe_title}_chart_{i+1}_{date_str}.png"
                chart_path = self.create_data_chart(
                    chart['data'],
                    chart['type'],
                    chart['title'],
                    chart_file
                )
                assets['files'][f'chart_{i+1}'] = chart_path
        
        # 3. Create text overlays
        overlays = [
            {'text': topic_title, 'type': 'title', 'name': 'title'},
            {'text': topic_data.get('subtitle', 'Geopolitical Analysis'), 'type': 'lower_third', 'name': 'lower_third'}
        ]
        
        if 'statistics' in topic_data:
            for i, stat in enumerate(topic_data['statistics']):
                overlays.append({
                    'text': f"{stat['value']}\n{stat['description']}", 
                    'type': 'statistic', 
                    'name': f'statistic_{i+1}'
                })
        
        for overlay in overlays:
            overlay_file = f"{safe_title}_{overlay['name']}_{date_str}.png"
            overlay_path = self.create_text_overlay(
                overlay['text'],
                overlay['type'],
                overlay_file
            )
            assets['files'][overlay['name']] = overlay_path
        
        # Save asset manifest
        manifest_file = os.path.join(self.generated_dir, f"{safe_title}_assets_{date_str}.json")
        with open(manifest_file, 'w') as f:
            json.dump(assets, f, indent=2)
        
        print(f"✅ Asset generation complete!")
        print(f"📄 Manifest saved: {manifest_file}")
        
        return assets

def generate_sample_assets():
    """Generate sample assets for testing"""
    
    generator = TDIVisualGenerator()
    
    # Sample topic data
    sample_topics = [
        {
            'title': 'Ukraine War Economic Impact: Global Analysis',
            'subtitle': 'Economic Consequences of Ongoing Conflict',
            'regions': ['Europe', 'Ukraine', 'North America'],
            'chart_data': [
                {
                    'type': 'bar',
                    'title': 'GDP Impact by Region (%)',
                    'data': {
                        'labels': ['EU', 'USA', 'China', 'Russia'],
                        'values': [-2.1, -0.8, -1.2, -8.5]
                    }
                },
                {
                    'type': 'line',
                    'title': 'Energy Prices Over Time',
                    'data': {
                        'x': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                        'y': [85, 95, 120, 110, 105, 98]
                    }
                }
            ],
            'statistics': [
                {'value': '€2.1T', 'description': 'Total Economic Impact'},
                {'value': '40%', 'description': 'Energy Price Increase'}
            ]
        },
        {
            'title': "China's Belt and Road Initiative: Latest Developments",
            'subtitle': 'Infrastructure Investment Analysis',
            'regions': ['Asia', 'China', 'Europe', 'Africa'],
            'chart_data': [
                {
                    'type': 'pie',
                    'title': 'BRI Investment by Region',
                    'data': {
                        'labels': ['Asia', 'Europe', 'Africa'],
                        'values': [60, 25, 15]
                    }
                }
            ],
            'statistics': [
                {'value': '$1.3T', 'description': 'Total Investment Committed'},
                {'value': '147', 'description': 'Countries Participating'}
            ]
        }
    ]
    
    # Generate assets for each topic
    all_assets = []
    for topic in sample_topics:
        assets = generator.generate_video_assets(topic)
        all_assets.append(assets)
    
    print(f"\n🎉 Sample asset generation complete!")
    print(f"📁 Check the following directories:")
    print(f"   Maps: {generator.maps_dir}")
    print(f"   Charts: {generator.charts_dir}")
    print(f"   Overlays: {generator.overlays_dir}")
    print(f"   Generated: {generator.generated_dir}")
    
    return all_assets

if __name__ == "__main__":
    # Generate sample assets
    assets = generate_sample_assets()
    
    print("\n" + "="*60)
    print("🎨 TDI VISUAL ASSET GENERATOR - READY FOR PRODUCTION!")
    print("="*60)
