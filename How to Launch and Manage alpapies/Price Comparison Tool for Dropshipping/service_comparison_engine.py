"""
Service Comparison Engine
Advanced algorithms for comparing services and service providers
"""

import re
from typing import List, Dict, Any, Tuple
from difflib import SequenceMatcher
import statistics

class ServiceComparisonEngine:
    def __init__(self):
        self.service_weights = {
            'price_score': 0.25,
            'rating_score': 0.20,
            'experience_score': 0.15,
            'response_time_score': 0.15,
            'platform_trust_score': 0.10,
            'location_score': 0.10,
            'verification_score': 0.05
        }
        
        self.platform_trust_scores = {
            'Fiverr': 0.85,
            'Upwork': 0.90,
            'Freelancer': 0.80,
            'TaskRabbit': 0.88,
            'Thumbtack': 0.87,
            'Angie': 0.89
        }

    def compare_services(self, services: List[Dict[str, Any]], user_preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """Compare services and provide intelligent recommendations"""
        if not services:
            return {'services': [], 'recommendations': [], 'insights': {}}
        
        # Group similar services
        service_groups = self._group_similar_services(services)
        
        # Score and rank services
        scored_services = self._score_services(services, user_preferences)
        
        # Generate recommendations
        recommendations = self._generate_service_recommendations(scored_services, user_preferences)
        
        # Create insights
        insights = self._generate_service_insights(scored_services)
        
        return {
            'services': scored_services,
            'service_groups': service_groups,
            'recommendations': recommendations,
            'insights': insights,
            'total_services': len(services),
            'platforms_searched': len(set(s['platform'] for s in services))
        }

    def _group_similar_services(self, services: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Group similar services together"""
        groups = []
        used_indices = set()
        
        for i, service in enumerate(services):
            if i in used_indices:
                continue
                
            group = {
                'group_id': len(groups) + 1,
                'primary_service': service,
                'similar_services': [],
                'service_type': service.get('service_type', 'Unknown'),
                'avg_price': 0,
                'price_range': {'min': float('inf'), 'max': 0}
            }
            
            used_indices.add(i)
            group_services = [service]
            
            # Find similar services
            for j, other_service in enumerate(services):
                if j in used_indices or i == j:
                    continue
                    
                similarity = self._calculate_service_similarity(service, other_service)
                if similarity > 0.7:  # 70% similarity threshold
                    group['similar_services'].append(other_service)
                    group_services.append(other_service)
                    used_indices.add(j)
            
            # Calculate group statistics
            prices = []
            for svc in group_services:
                price = self._extract_price(svc)
                if price:
                    prices.append(price)
                    group['price_range']['min'] = min(group['price_range']['min'], price)
                    group['price_range']['max'] = max(group['price_range']['max'], price)
            
            if prices:
                group['avg_price'] = statistics.mean(prices)
                if group['price_range']['min'] == float('inf'):
                    group['price_range']['min'] = min(prices)
            
            groups.append(group)
        
        return groups

    def _calculate_service_similarity(self, service1: Dict[str, Any], service2: Dict[str, Any]) -> float:
        """Calculate similarity between two services"""
        # Title similarity
        title_sim = SequenceMatcher(None, 
                                  service1.get('title', '').lower(), 
                                  service2.get('title', '').lower()).ratio()
        
        # Service type similarity
        type_sim = 1.0 if service1.get('service_type') == service2.get('service_type') else 0.0
        
        # Platform similarity (services on same platform are less similar for comparison)
        platform_sim = 0.3 if service1.get('platform') == service2.get('platform') else 0.7
        
        # Description similarity
        desc_sim = SequenceMatcher(None,
                                 service1.get('description', '').lower(),
                                 service2.get('description', '').lower()).ratio()
        
        # Weighted similarity score
        similarity = (title_sim * 0.4 + type_sim * 0.3 + platform_sim * 0.1 + desc_sim * 0.2)
        
        return similarity

    def _score_services(self, services: List[Dict[str, Any]], user_preferences: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Score services based on various factors"""
        if not user_preferences:
            user_preferences = {}
        
        scored_services = []
        
        for service in services:
            scores = {}
            
            # Price score (lower price = higher score)
            scores['price_score'] = self._calculate_price_score(service, services)
            
            # Rating score
            scores['rating_score'] = self._calculate_rating_score(service)
            
            # Experience score
            scores['experience_score'] = self._calculate_experience_score(service)
            
            # Response time score
            scores['response_time_score'] = self._calculate_response_time_score(service)
            
            # Platform trust score
            scores['platform_trust_score'] = self.platform_trust_scores.get(service.get('platform'), 0.75)
            
            # Location score
            scores['location_score'] = self._calculate_location_score(service, user_preferences)
            
            # Verification score
            scores['verification_score'] = self._calculate_verification_score(service)
            
            # Calculate overall score
            overall_score = sum(scores[key] * self.service_weights[key] for key in scores)
            
            # Add scores to service
            service_copy = service.copy()
            service_copy['scores'] = scores
            service_copy['overall_score'] = overall_score
            service_copy['recommendation_level'] = self._get_recommendation_level(overall_score)
            
            scored_services.append(service_copy)
        
        # Sort by overall score
        scored_services.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return scored_services

    def _calculate_price_score(self, service: Dict[str, Any], all_services: List[Dict[str, Any]]) -> float:
        """Calculate price competitiveness score"""
        price = self._extract_price(service)
        if not price:
            return 0.5  # Neutral score for services without clear pricing
        
        # Get all prices for comparison
        all_prices = [self._extract_price(s) for s in all_services if self._extract_price(s)]
        if not all_prices:
            return 0.5
        
        min_price = min(all_prices)
        max_price = max(all_prices)
        
        if max_price == min_price:
            return 0.8  # All prices are the same
        
        # Normalize price (lower price = higher score)
        normalized_score = 1 - (price - min_price) / (max_price - min_price)
        return max(0.1, min(1.0, normalized_score))

    def _extract_price(self, service: Dict[str, Any]) -> float:
        """Extract numeric price from service"""
        # Try different price fields
        for field in ['starting_price', 'hourly_rate', 'bid_amount']:
            if field in service and service[field]:
                return float(service[field])
        
        # Try to extract from price_range or quote_range
        for field in ['price_range', 'quote_range']:
            if field in service and service[field]:
                price_str = service[field]
                # Extract first number from range like "$100 - $300"
                numbers = re.findall(r'\d+', str(price_str))
                if numbers:
                    return float(numbers[0])
        
        return None

    def _calculate_rating_score(self, service: Dict[str, Any]) -> float:
        """Calculate rating-based score"""
        rating = service.get('provider_rating', 0)
        if not rating:
            return 0.5
        
        # Normalize rating (assuming 5-star scale)
        return min(1.0, rating / 5.0)

    def _calculate_experience_score(self, service: Dict[str, Any]) -> float:
        """Calculate experience-based score"""
        # Check various experience indicators
        score = 0.5  # Base score
        
        # Years of experience
        if 'years_experience' in service:
            years = service['years_experience']
            score += min(0.3, years / 20)  # Max 0.3 for 20+ years
        
        if 'years_in_business' in service:
            years = service['years_in_business']
            score += min(0.3, years / 20)
        
        # Number of reviews (indicates experience)
        reviews = service.get('provider_reviews', 0)
        if reviews:
            score += min(0.2, reviews / 500)  # Max 0.2 for 500+ reviews
        
        # Provider level
        level = service.get('provider_level', '').lower()
        if 'top' in level or 'elite' in level or 'expert' in level:
            score += 0.2
        elif 'level 2' in level or 'experienced' in level:
            score += 0.1
        
        return min(1.0, score)

    def _calculate_response_time_score(self, service: Dict[str, Any]) -> float:
        """Calculate response time score"""
        response_time = service.get('response_time', '')
        if not response_time:
            return 0.5
        
        # Extract hours from response time
        if 'minute' in response_time.lower():
            return 1.0  # Excellent response time
        elif '1 hour' in response_time.lower():
            return 0.9
        elif '2 hour' in response_time.lower():
            return 0.8
        elif '4 hour' in response_time.lower():
            return 0.7
        elif '8 hour' in response_time.lower():
            return 0.6
        elif '24 hour' in response_time.lower() or '1 day' in response_time.lower():
            return 0.5
        else:
            return 0.4

    def _calculate_location_score(self, service: Dict[str, Any], user_preferences: Dict[str, Any]) -> float:
        """Calculate location relevance score"""
        user_location = user_preferences.get('location', '')
        service_location = service.get('location', '')
        
        if not user_location or not service_location:
            return 0.5  # Neutral score
        
        # Simple location matching (can be enhanced with geolocation)
        if user_location.lower() in service_location.lower():
            return 1.0
        elif any(word in service_location.lower() for word in user_location.lower().split()):
            return 0.8
        else:
            return 0.3  # Remote service penalty

    def _calculate_verification_score(self, service: Dict[str, Any]) -> float:
        """Calculate verification and trust score"""
        score = 0.0
        
        # Check various verification indicators
        verifications = [
            'background_checked', 'licensed', 'insured', 'bonded',
            'license_verified', 'insurance_covered'
        ]
        
        for verification in verifications:
            if service.get(verification):
                score += 0.2
        
        # Completion rate
        completion_rate = service.get('completion_rate', '')
        if completion_rate:
            rate = float(re.findall(r'\d+', completion_rate)[0]) if re.findall(r'\d+', completion_rate) else 0
            score += (rate / 100) * 0.3
        
        return min(1.0, score)

    def _get_recommendation_level(self, score: float) -> str:
        """Get recommendation level based on score"""
        if score >= 0.8:
            return 'Highly Recommended'
        elif score >= 0.7:
            return 'Recommended'
        elif score >= 0.6:
            return 'Good Option'
        else:
            return 'Consider Carefully'

    def _generate_service_recommendations(self, scored_services: List[Dict[str, Any]], user_preferences: Dict[str, Any] = None) -> List[str]:
        """Generate intelligent service recommendations"""
        if not scored_services:
            return []
        
        recommendations = []
        
        # Best overall service
        best_service = scored_services[0]
        recommendations.append(f"Best overall: {best_service['title']} from {best_service['platform']} - {best_service['recommendation_level']}")
        
        # Best value service
        value_services = [s for s in scored_services if self._extract_price(s)]
        if value_services:
            best_value = min(value_services, key=lambda x: self._extract_price(x) / max(x['overall_score'], 0.1))
            price = self._extract_price(best_value)
            recommendations.append(f"Best value: {best_value['title']} from {best_value['platform']} at ${price}")
        
        # Fastest response
        response_services = [s for s in scored_services if s.get('response_time')]
        if response_services:
            fastest = max(response_services, key=lambda x: x['scores']['response_time_score'])
            recommendations.append(f"Fastest response: {fastest['title']} from {fastest['platform']} - {fastest.get('response_time', 'Quick response')}")
        
        # Most experienced
        exp_services = [s for s in scored_services if s['scores']['experience_score'] > 0.7]
        if exp_services:
            most_exp = max(exp_services, key=lambda x: x['scores']['experience_score'])
            recommendations.append(f"Most experienced: {most_exp['title']} from {most_exp['platform']} - {most_exp.get('provider_level', 'Experienced')}")
        
        # Local service (if applicable)
        if user_preferences and user_preferences.get('location'):
            local_services = [s for s in scored_services if s['scores']['location_score'] > 0.8]
            if local_services:
                best_local = local_services[0]
                recommendations.append(f"Best local option: {best_local['title']} from {best_local['platform']} in {best_local.get('location', 'your area')}")
        
        return recommendations

    def _generate_service_insights(self, scored_services: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate insights about the service comparison"""
        if not scored_services:
            return {}
        
        prices = [self._extract_price(s) for s in scored_services if self._extract_price(s)]
        ratings = [s.get('provider_rating', 0) for s in scored_services if s.get('provider_rating')]
        
        insights = {
            'price_analysis': {},
            'quality_analysis': {},
            'platform_analysis': {},
            'service_types': {}
        }
        
        # Price analysis
        if prices:
            insights['price_analysis'] = {
                'min_price': min(prices),
                'max_price': max(prices),
                'avg_price': statistics.mean(prices),
                'price_spread': max(prices) - min(prices),
                'budget_options': len([p for p in prices if p <= statistics.mean(prices) * 0.8])
            }
        
        # Quality analysis
        if ratings:
            insights['quality_analysis'] = {
                'avg_rating': statistics.mean(ratings),
                'high_rated_services': len([r for r in ratings if r >= 4.5]),
                'rating_consistency': 1 - (statistics.stdev(ratings) if len(ratings) > 1 else 0) / 5
            }
        
        # Platform analysis
        platform_counts = {}
        for service in scored_services:
            platform = service.get('platform', 'Unknown')
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        insights['platform_analysis'] = {
            'platforms_found': list(platform_counts.keys()),
            'platform_distribution': platform_counts,
            'most_results_platform': max(platform_counts.items(), key=lambda x: x[1])[0] if platform_counts else None
        }
        
        # Service types
        type_counts = {}
        for service in scored_services:
            service_type = service.get('service_type', 'Unknown')
            type_counts[service_type] = type_counts.get(service_type, 0) + 1
        
        insights['service_types'] = type_counts
        
        return insights

# Example usage
if __name__ == "__main__":
    # Mock services for testing
    mock_services = [
        {
            'platform': 'Fiverr',
            'title': 'Web Development Service',
            'provider_rating': 4.8,
            'starting_price': 50,
            'response_time': '2 hours',
            'service_type': 'Digital Service'
        },
        {
            'platform': 'Upwork',
            'title': 'Web Development Specialist',
            'provider_rating': 4.9,
            'hourly_rate': 75,
            'response_time': '1 hour',
            'service_type': 'Professional Service'
        }
    ]
    
    engine = ServiceComparisonEngine()
    result = engine.compare_services(mock_services)
    
    print("Service comparison result:")
    print(f"Total services: {result['total_services']}")
    print(f"Recommendations: {result['recommendations']}")
