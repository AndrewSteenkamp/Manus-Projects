"""
Service Provider Collection System
Collects and compares services from various platforms
"""

import requests
import time
import random
from typing import List, Dict, Any
from bs4 import BeautifulSoup

class ServiceProviderCollector:
    def __init__(self):
        self.service_platforms = {
            'Fiverr': {
                'base_url': 'https://www.fiverr.com',
                'search_url': 'https://www.fiverr.com/search/gigs',
                'affiliate_param': 'source',
                'categories': ['web-development', 'graphic-design', 'digital-marketing', 'writing', 'video-animation']
            },
            'Upwork': {
                'base_url': 'https://www.upwork.com',
                'search_url': 'https://www.upwork.com/freelance-jobs/search',
                'affiliate_param': 'ref',
                'categories': ['web-mobile-software-dev', 'design-creative', 'sales-marketing', 'writing', 'admin-support']
            },
            'Freelancer': {
                'base_url': 'https://www.freelancer.com',
                'search_url': 'https://www.freelancer.com/search/projects',
                'affiliate_param': 'ref_id',
                'categories': ['websites', 'mobile-apps', 'design', 'marketing', 'writing']
            },
            'TaskRabbit': {
                'base_url': 'https://www.taskrabbit.com',
                'search_url': 'https://www.taskrabbit.com/services',
                'affiliate_param': 'ref',
                'categories': ['handyman', 'cleaning', 'moving', 'furniture-assembly', 'mounting']
            },
            'Thumbtack': {
                'base_url': 'https://www.thumbtack.com',
                'search_url': 'https://www.thumbtack.com/k',
                'affiliate_param': 'utm_source',
                'categories': ['home-improvement', 'wellness', 'events', 'business', 'lessons']
            },
            'Angie': {
                'base_url': 'https://www.angi.com',
                'search_url': 'https://www.angi.com/companylist',
                'affiliate_param': 'source',
                'categories': ['home-improvement', 'lawn-care', 'cleaning', 'pest-control', 'hvac']
            }
        }
        
        self.service_categories = {
            'Digital Services': {
                'subcategories': ['Web Development', 'Graphic Design', 'Digital Marketing', 'Content Writing', 'SEO', 'Social Media Management'],
                'platforms': ['Fiverr', 'Upwork', 'Freelancer']
            },
            'Home Services': {
                'subcategories': ['Cleaning', 'Handyman', 'Plumbing', 'Electrical', 'HVAC', 'Landscaping'],
                'platforms': ['TaskRabbit', 'Thumbtack', 'Angie']
            },
            'Professional Services': {
                'subcategories': ['Legal', 'Accounting', 'Consulting', 'Real Estate', 'Insurance', 'Financial Planning'],
                'platforms': ['Thumbtack', 'Upwork']
            },
            'Personal Services': {
                'subcategories': ['Tutoring', 'Fitness Training', 'Pet Care', 'Event Planning', 'Photography', 'Music Lessons'],
                'platforms': ['Thumbtack', 'TaskRabbit', 'Fiverr']
            },
            'Business Services': {
                'subcategories': ['Virtual Assistant', 'Data Entry', 'Customer Service', 'Translation', 'Bookkeeping', 'Market Research'],
                'platforms': ['Upwork', 'Freelancer', 'Fiverr']
            }
        }

    def search_services(self, query: str, category: str = None, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for services across multiple platforms"""
        all_services = []
        
        # Determine relevant platforms based on category
        relevant_platforms = self._get_relevant_platforms(category)
        
        for platform in relevant_platforms:
            try:
                services = self._search_platform_services(platform, query, max_results // len(relevant_platforms))
                all_services.extend(services)
                time.sleep(random.uniform(1, 2))  # Rate limiting
            except Exception as e:
                print(f"Error searching {platform}: {e}")
                continue
        
        return all_services[:max_results]

    def _get_relevant_platforms(self, category: str) -> List[str]:
        """Get platforms relevant to the service category"""
        if not category:
            return list(self.service_platforms.keys())
        
        for cat_name, cat_info in self.service_categories.items():
            if category.lower() in cat_name.lower() or any(sub.lower() in category.lower() for sub in cat_info['subcategories']):
                return cat_info['platforms']
        
        return list(self.service_platforms.keys())

    def _search_platform_services(self, platform: str, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search for services on a specific platform"""
        if platform == 'Fiverr':
            return self._search_fiverr(query, max_results)
        elif platform == 'Upwork':
            return self._search_upwork(query, max_results)
        elif platform == 'Freelancer':
            return self._search_freelancer(query, max_results)
        elif platform == 'TaskRabbit':
            return self._search_taskrabbit(query, max_results)
        elif platform == 'Thumbtack':
            return self._search_thumbtack(query, max_results)
        elif platform == 'Angie':
            return self._search_angie(query, max_results)
        else:
            return []

    def _search_fiverr(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search Fiverr for services (mock data for demo)"""
        services = []
        base_prices = [5, 10, 15, 25, 50, 75, 100, 150, 200, 300]
        
        for i in range(min(max_results, 5)):
            base_price = random.choice(base_prices)
            service = {
                'platform': 'Fiverr',
                'title': f'{query} Service - Professional Gig #{i+1}',
                'provider_name': f'Expert{random.randint(100, 999)}',
                'provider_rating': round(random.uniform(4.0, 5.0), 1),
                'provider_reviews': random.randint(10, 500),
                'starting_price': base_price,
                'currency': 'USD',
                'delivery_time': f'{random.choice([1, 2, 3, 5, 7])} days',
                'description': f'Professional {query} service with high quality delivery',
                'service_url': f'https://www.fiverr.com/gigs/{query.replace(" ", "-")}-{i+1}',
                'provider_level': random.choice(['New Seller', 'Level 1', 'Level 2', 'Top Rated']),
                'service_type': 'Digital Service',
                'location': random.choice(['United States', 'United Kingdom', 'Canada', 'Australia', 'Germany']),
                'response_time': f'{random.choice([1, 2, 4, 8, 24])} hours',
                'completion_rate': f'{random.randint(95, 100)}%',
                'packages': {
                    'basic': {'price': base_price, 'delivery': '3 days', 'features': ['Basic service', 'Standard quality']},
                    'standard': {'price': base_price * 2, 'delivery': '5 days', 'features': ['Enhanced service', 'Premium quality', 'Revisions']},
                    'premium': {'price': base_price * 3, 'delivery': '7 days', 'features': ['Complete service', 'Premium quality', 'Unlimited revisions', 'Fast delivery']}
                }
            }
            services.append(service)
        
        return services

    def _search_upwork(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search Upwork for freelancers (mock data for demo)"""
        services = []
        hourly_rates = [15, 25, 35, 50, 75, 100, 150, 200]
        
        for i in range(min(max_results, 4)):
            hourly_rate = random.choice(hourly_rates)
            service = {
                'platform': 'Upwork',
                'title': f'{query} Specialist - Freelancer #{i+1}',
                'provider_name': f'Professional{random.randint(100, 999)}',
                'provider_rating': round(random.uniform(4.2, 5.0), 1),
                'provider_reviews': random.randint(5, 200),
                'hourly_rate': hourly_rate,
                'currency': 'USD',
                'availability': random.choice(['Available now', 'Available in 1 week', 'Available in 2 weeks']),
                'description': f'Experienced {query} professional with proven track record',
                'service_url': f'https://www.upwork.com/freelancers/{query.replace(" ", "-")}-{i+1}',
                'provider_level': random.choice(['Rising Talent', 'Top Rated', 'Top Rated Plus']),
                'service_type': 'Professional Service',
                'location': random.choice(['United States', 'United Kingdom', 'Canada', 'India', 'Philippines']),
                'success_rate': f'{random.randint(90, 100)}%',
                'total_earned': f'${random.randint(10, 500)}K+',
                'skills': [f'{query}', 'Project Management', 'Communication', 'Quality Assurance'],
                'project_types': ['Fixed Price', 'Hourly'],
                'min_project_size': f'${random.choice([500, 1000, 2500, 5000])}'
            }
            services.append(service)
        
        return services

    def _search_freelancer(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search Freelancer.com for services (mock data for demo)"""
        services = []
        bid_amounts = [50, 100, 250, 500, 750, 1000, 1500, 2000]
        
        for i in range(min(max_results, 3)):
            bid_amount = random.choice(bid_amounts)
            service = {
                'platform': 'Freelancer',
                'title': f'{query} Expert - Bid #{i+1}',
                'provider_name': f'Freelancer{random.randint(100, 999)}',
                'provider_rating': round(random.uniform(4.0, 5.0), 1),
                'provider_reviews': random.randint(8, 150),
                'bid_amount': bid_amount,
                'currency': 'USD',
                'delivery_time': f'{random.choice([3, 5, 7, 10, 14])} days',
                'description': f'Professional {query} service with competitive pricing',
                'service_url': f'https://www.freelancer.com/projects/{query.replace(" ", "-")}-{i+1}',
                'provider_level': random.choice(['New', 'Experienced', 'Expert']),
                'service_type': 'Freelance Service',
                'location': random.choice(['India', 'Pakistan', 'Bangladesh', 'Philippines', 'Ukraine']),
                'completion_rate': f'{random.randint(85, 98)}%',
                'on_time_delivery': f'{random.randint(90, 100)}%',
                'skills_tests': random.randint(2, 8),
                'portfolio_items': random.randint(5, 25)
            }
            services.append(service)
        
        return services

    def _search_taskrabbit(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search TaskRabbit for local services (mock data for demo)"""
        services = []
        hourly_rates = [25, 35, 45, 55, 65, 75, 85, 95]
        
        for i in range(min(max_results, 4)):
            hourly_rate = random.choice(hourly_rates)
            service = {
                'platform': 'TaskRabbit',
                'title': f'{query} Tasker - Local Expert #{i+1}',
                'provider_name': f'Tasker{random.randint(100, 999)}',
                'provider_rating': round(random.uniform(4.3, 5.0), 1),
                'provider_reviews': random.randint(15, 300),
                'hourly_rate': hourly_rate,
                'currency': 'USD',
                'availability': random.choice(['Today', 'Tomorrow', 'This week', 'Next week']),
                'description': f'Reliable {query} service in your local area',
                'service_url': f'https://www.taskrabbit.com/profile/{query.replace(" ", "-")}-{i+1}',
                'provider_level': 'Elite Tasker' if random.random() > 0.7 else 'Tasker',
                'service_type': 'Local Service',
                'location': random.choice(['New York, NY', 'Los Angeles, CA', 'Chicago, IL', 'Houston, TX', 'Phoenix, AZ']),
                'response_time': f'{random.choice([15, 30, 60])} minutes',
                'same_day_availability': random.choice([True, False]),
                'background_checked': True,
                'insurance_covered': True,
                'tools_provided': random.choice([True, False])
            }
            services.append(service)
        
        return services

    def _search_thumbtack(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search Thumbtack for professional services (mock data for demo)"""
        services = []
        quote_ranges = [(50, 150), (100, 300), (200, 500), (300, 800), (500, 1200)]
        
        for i in range(min(max_results, 4)):
            quote_range = random.choice(quote_ranges)
            service = {
                'platform': 'Thumbtack',
                'title': f'{query} Professional - Pro #{i+1}',
                'provider_name': f'Pro{random.randint(100, 999)}',
                'provider_rating': round(random.uniform(4.1, 5.0), 1),
                'provider_reviews': random.randint(12, 250),
                'quote_range': f'${quote_range[0]} - ${quote_range[1]}',
                'currency': 'USD',
                'response_time': f'{random.choice([1, 2, 4, 8])} hours',
                'description': f'Professional {query} service with competitive quotes',
                'service_url': f'https://www.thumbtack.com/pro/{query.replace(" ", "-")}-{i+1}',
                'provider_level': 'Top Pro' if random.random() > 0.6 else 'Pro',
                'service_type': 'Professional Service',
                'location': random.choice(['San Francisco, CA', 'Seattle, WA', 'Austin, TX', 'Denver, CO', 'Atlanta, GA']),
                'years_experience': random.randint(2, 15),
                'background_checked': True,
                'license_verified': random.choice([True, False]),
                'free_consultation': random.choice([True, False]),
                'satisfaction_guarantee': random.choice([True, False])
            }
            services.append(service)
        
        return services

    def _search_angie(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search Angie (formerly Angie's List) for home services (mock data for demo)"""
        services = []
        price_ranges = [('$', 50, 200), ('$$', 200, 500), ('$$$', 500, 1000), ('$$$$', 1000, 2500)]
        
        for i in range(min(max_results, 3)):
            price_tier, min_price, max_price = random.choice(price_ranges)
            service = {
                'platform': 'Angie',
                'title': f'{query} Company - Contractor #{i+1}',
                'provider_name': f'Company{random.randint(100, 999)}',
                'provider_rating': round(random.uniform(4.0, 5.0), 1),
                'provider_reviews': random.randint(20, 400),
                'price_tier': price_tier,
                'price_range': f'${min_price} - ${max_price}',
                'currency': 'USD',
                'response_time': f'{random.choice([2, 4, 8, 24])} hours',
                'description': f'Licensed and insured {query} contractor',
                'service_url': f'https://www.angi.com/companylist/{query.replace(" ", "-")}-{i+1}',
                'provider_level': 'Super Service Award' if random.random() > 0.7 else 'Certified',
                'service_type': 'Home Service',
                'location': random.choice(['Dallas, TX', 'Miami, FL', 'Boston, MA', 'Portland, OR', 'Nashville, TN']),
                'years_in_business': random.randint(5, 25),
                'licensed': True,
                'insured': True,
                'bonded': random.choice([True, False]),
                'warranty_offered': random.choice([True, False]),
                'free_estimates': True
            }
            services.append(service)
        
        return services

    def get_service_categories(self) -> Dict[str, Any]:
        """Get available service categories"""
        return self.service_categories

    def get_platform_info(self) -> Dict[str, Any]:
        """Get information about supported platforms"""
        return self.service_platforms

# Example usage
if __name__ == "__main__":
    collector = ServiceProviderCollector()
    
    # Test service search
    print("Testing service search...")
    services = collector.search_services("web development", "Digital Services", 10)
    
    print(f"\nFound {len(services)} services:")
    for service in services:
        print(f"- {service['platform']}: {service['title']} - ${service.get('starting_price', service.get('hourly_rate', service.get('bid_amount', 'Quote')))}")
