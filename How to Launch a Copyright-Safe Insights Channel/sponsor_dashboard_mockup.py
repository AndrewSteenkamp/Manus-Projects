#!/usr/bin/env python3
"""
Sponsor Dashboard Mockup
Trending Daily Insights - Real-time Performance Tracking
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import seaborn as sns

# Set style for professional appearance
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def create_sponsor_dashboard():
    """Create a comprehensive sponsor performance dashboard"""
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(20, 16))
    fig.suptitle('Trending Daily Insights - Sponsor Performance Dashboard\nReal-time Analytics & ROI Tracking', 
                 fontsize=20, fontweight='bold', y=0.98)
    
    # Generate sample data for the last 30 days
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), 
                         end=datetime.now(), freq='D')
    
    # Sample performance data
    np.random.seed(42)  # For reproducible results
    views = np.random.normal(2500, 300, len(dates))
    engagement_rate = np.random.normal(8.2, 0.8, len(dates))
    ctr = np.random.normal(5.7, 0.6, len(dates))
    conversion_rate = np.random.normal(3.2, 0.4, len(dates))
    
    # Ensure realistic bounds
    engagement_rate = np.clip(engagement_rate, 5.0, 12.0)
    ctr = np.clip(ctr, 3.0, 8.0)
    conversion_rate = np.clip(conversion_rate, 1.5, 5.0)
    
    # 1. Daily Performance Trends (Top Left)
    ax1 = plt.subplot(3, 4, (1, 2))
    ax1.plot(dates, views, linewidth=2, label='Daily Views', color='#3B82F6')
    ax1.set_title('Daily Video Performance', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Views', fontsize=12)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Add trend line
    z = np.polyfit(range(len(dates)), views, 1)
    p = np.poly1d(z)
    ax1.plot(dates, p(range(len(dates))), "--", alpha=0.8, color='red', 
             label=f'Trend: {"↗" if z[0] > 0 else "↘"}')
    ax1.legend()
    
    # 2. Key Metrics Gauges (Top Right)
    ax2 = plt.subplot(3, 4, (3, 4))
    
    # Create gauge-like visualization for key metrics
    metrics = ['Engagement\nRate', 'Click-Through\nRate', 'Conversion\nRate']
    values = [8.2, 5.7, 3.2]
    targets = [8.0, 5.5, 3.0]
    colors = ['#10B981', '#3B82F6', '#F59E0B']
    
    x_pos = np.arange(len(metrics))
    bars = ax2.bar(x_pos, values, color=colors, alpha=0.7, label='Current')
    ax2.bar(x_pos, targets, color=colors, alpha=0.3, label='Target', width=0.5)
    
    ax2.set_title('Key Performance Indicators', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Percentage (%)', fontsize=12)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(metrics)
    ax2.legend()
    
    # Add value labels on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 3. ROI Calculation (Middle Left)
    ax3 = plt.subplot(3, 4, 5)
    
    # Sample ROI data for different sponsors
    sponsors = ['SecureVPN', 'TradingPro', 'InvestCorp']
    roi_values = [2.4, 2.1, 2.8]
    investment = [3500, 1500, 7000]
    
    colors_roi = ['#EF4444', '#3B82F6', '#10B981']
    bars_roi = ax3.barh(sponsors, roi_values, color=colors_roi, alpha=0.7)
    ax3.set_title('Sponsor ROI Performance', fontsize=14, fontweight='bold')
    ax3.set_xlabel('ROI Multiplier', fontsize=12)
    ax3.axvline(x=2.0, color='red', linestyle='--', alpha=0.7, label='Target ROI: 2.0x')
    
    # Add ROI labels
    for i, (bar, roi, inv) in enumerate(zip(bars_roi, roi_values, investment)):
        width = bar.get_width()
        ax3.text(width + 0.05, bar.get_y() + bar.get_height()/2,
                f'{roi:.1f}x\n(${inv:,})', ha='left', va='center', fontweight='bold')
    
    ax3.legend()
    ax3.set_xlim(0, 3.5)
    
    # 4. Audience Demographics (Middle Center)
    ax4 = plt.subplot(3, 4, 6)
    
    # Income distribution
    income_brackets = ['<$50K', '$50-100K', '$100-150K', '$150K+']
    income_percentages = [15, 27, 32, 26]
    
    wedges, texts, autotexts = ax4.pie(income_percentages, labels=income_brackets, 
                                      autopct='%1.1f%%', startangle=90,
                                      colors=['#EF4444', '#F59E0B', '#3B82F6', '#10B981'])
    ax4.set_title('Audience Income Distribution', fontsize=14, fontweight='bold')
    
    # 5. Engagement Trends (Middle Right)
    ax5 = plt.subplot(3, 4, (7, 8))
    
    ax5.plot(dates, engagement_rate, linewidth=2, label='Engagement Rate', color='#10B981')
    ax5.plot(dates, ctr, linewidth=2, label='Click-Through Rate', color='#3B82F6')
    ax5.plot(dates, conversion_rate, linewidth=2, label='Conversion Rate', color='#F59E0B')
    
    ax5.set_title('Performance Trends (30 Days)', fontsize=14, fontweight='bold')
    ax5.set_ylabel('Percentage (%)', fontsize=12)
    ax5.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    ax5.tick_params(axis='x', rotation=45)
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # 6. Competitive Benchmarking (Bottom Left)
    ax6 = plt.subplot(3, 4, 9)
    
    metrics_comp = ['Engagement', 'CTR', 'Conversion']
    our_performance = [8.2, 5.7, 3.2]
    industry_avg = [4.1, 2.8, 1.5]
    
    x = np.arange(len(metrics_comp))
    width = 0.35
    
    bars1 = ax6.bar(x - width/2, our_performance, width, label='Trending Daily Insights', 
                   color='#3B82F6', alpha=0.8)
    bars2 = ax6.bar(x + width/2, industry_avg, width, label='Industry Average', 
                   color='#9CA3AF', alpha=0.8)
    
    ax6.set_title('Competitive Benchmarking', fontsize=14, fontweight='bold')
    ax6.set_ylabel('Percentage (%)', fontsize=12)
    ax6.set_xticks(x)
    ax6.set_xticklabels(metrics_comp)
    ax6.legend()
    
    # Add performance improvement labels
    for i, (our, ind) in enumerate(zip(our_performance, industry_avg)):
        improvement = ((our - ind) / ind) * 100
        ax6.text(i, max(our, ind) + 0.3, f'+{improvement:.0f}%', 
                ha='center', va='bottom', fontweight='bold', color='green')
    
    # 7. Geographic Distribution (Bottom Center)
    ax7 = plt.subplot(3, 4, 10)
    
    regions = ['North America', 'Europe', 'Asia-Pacific', 'Other']
    percentages = [45, 28, 20, 7]
    colors_geo = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444']
    
    bars_geo = ax7.bar(regions, percentages, color=colors_geo, alpha=0.7)
    ax7.set_title('Geographic Distribution', fontsize=14, fontweight='bold')
    ax7.set_ylabel('Percentage (%)', fontsize=12)
    ax7.tick_params(axis='x', rotation=45)
    
    # Add percentage labels
    for bar, pct in zip(bars_geo, percentages):
        height = bar.get_height()
        ax7.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{pct}%', ha='center', va='bottom', fontweight='bold')
    
    # 8. Performance Summary Table (Bottom Right)
    ax8 = plt.subplot(3, 4, (11, 12))
    ax8.axis('off')
    
    # Create summary table
    summary_data = [
        ['Metric', 'Current', 'Target', 'Status'],
        ['Monthly Views', '75,250', '70,000', '✓ Exceeded'],
        ['Avg Engagement', '8.2%', '8.0%', '✓ Met'],
        ['Avg CTR', '5.7%', '5.5%', '✓ Exceeded'],
        ['Avg Conversion', '3.2%', '3.0%', '✓ Exceeded'],
        ['Total Conversions', '2,408', '2,100', '✓ Exceeded'],
        ['Cost Per Acquisition', '$42', '$50', '✓ Under Budget'],
        ['Average ROI', '2.4x', '2.0x', '✓ Exceeded']
    ]
    
    table = ax8.table(cellText=summary_data[1:], colLabels=summary_data[0],
                     cellLoc='center', loc='center', bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Style the table
    for i in range(len(summary_data[0])):
        table[(0, i)].set_facecolor('#1E3A8A')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Color code the status column
    for i in range(1, len(summary_data)):
        if '✓' in summary_data[i][3]:
            table[(i, 3)].set_facecolor('#D1FAE5')  # Light green
    
    ax8.set_title('Performance Summary - Current Month', fontsize=14, fontweight='bold', pad=20)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.subplots_adjust(top=0.93, hspace=0.3, wspace=0.3)
    
    # Save the dashboard
    plt.savefig('/home/ubuntu/sponsor_dashboard_mockup.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    
    print("Sponsor dashboard mockup created successfully!")
    print("File saved as: /home/ubuntu/sponsor_dashboard_mockup.png")

def create_roi_breakdown_chart():
    """Create detailed ROI breakdown visualization"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Sponsor ROI Breakdown Analysis', fontsize=16, fontweight='bold')
    
    # 1. Revenue Attribution (Top Left)
    revenue_sources = ['Direct Sales', 'Lead Generation', 'Brand Awareness', 'Long-term Value']
    revenue_values = [4200, 2100, 1200, 550]
    colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444']
    
    wedges, texts, autotexts = ax1.pie(revenue_values, labels=revenue_sources, 
                                      autopct=lambda pct: f'${pct*sum(revenue_values)/100:.0f}',
                                      startangle=90, colors=colors)
    ax1.set_title('Revenue Attribution ($8,050 Total)', fontweight='bold')
    
    # 2. Cost Efficiency Comparison (Top Right)
    channels = ['TDI Sponsorship', 'Google Ads', 'LinkedIn Ads', 'Trade Shows']
    cpa_values = [42, 67, 89, 156]
    
    bars = ax2.bar(channels, cpa_values, color=['#10B981', '#9CA3AF', '#9CA3AF', '#9CA3AF'])
    ax2.set_title('Cost Per Acquisition Comparison', fontweight='bold')
    ax2.set_ylabel('Cost Per Acquisition ($)')
    ax2.tick_params(axis='x', rotation=45)
    
    # Highlight our performance
    bars[0].set_color('#3B82F6')
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'${height}', ha='center', va='bottom', fontweight='bold')
    
    # 3. ROI Timeline (Bottom Left)
    months = ['Month 1', 'Month 2', 'Month 3', 'Projected M4']
    cumulative_roi = [0.8, 1.4, 2.4, 3.1]
    
    ax3.plot(months, cumulative_roi, marker='o', linewidth=3, markersize=8, color='#3B82F6')
    ax3.axhline(y=2.0, color='red', linestyle='--', alpha=0.7, label='Target ROI: 2.0x')
    ax3.set_title('ROI Growth Timeline', fontweight='bold')
    ax3.set_ylabel('ROI Multiplier')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # Add ROI labels
    for i, roi in enumerate(cumulative_roi):
        ax3.text(i, roi + 0.1, f'{roi:.1f}x', ha='center', va='bottom', fontweight='bold')
    
    # 4. Performance vs Investment (Bottom Right)
    investment_tiers = ['Bronze\n$1,500', 'Silver\n$3,500', 'Gold\n$7,000']
    roi_performance = [1.8, 2.4, 2.7]
    investment_amounts = [1500, 3500, 7000]
    
    # Create scatter plot
    scatter = ax4.scatter(investment_amounts, roi_performance, 
                         s=[200, 300, 400], alpha=0.7, c=['#D97706', '#9CA3AF', '#F59E0B'])
    
    ax4.set_title('Investment vs ROI Performance', fontweight='bold')
    ax4.set_xlabel('Monthly Investment ($)')
    ax4.set_ylabel('ROI Multiplier')
    ax4.grid(True, alpha=0.3)
    
    # Add labels for each point
    for i, (inv, roi, tier) in enumerate(zip(investment_amounts, roi_performance, investment_tiers)):
        ax4.annotate(f'{tier}\nROI: {roi}x', (inv, roi), 
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8),
                    fontweight='bold', ha='left')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/roi_breakdown_analysis.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    
    print("ROI breakdown analysis created successfully!")
    print("File saved as: /home/ubuntu/roi_breakdown_analysis.png")

if __name__ == "__main__":
    create_sponsor_dashboard()
    create_roi_breakdown_chart()
    print("\nBoth sponsor analytics visualizations have been created!")
    print("These mockups demonstrate the comprehensive tracking and reporting capabilities")
    print("that will be provided to sponsors for transparent ROI measurement.")

