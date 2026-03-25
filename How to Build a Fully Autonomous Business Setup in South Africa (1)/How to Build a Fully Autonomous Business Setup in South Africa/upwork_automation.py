"""
Upwork Automation Service
Implements Nick's Phase 1: Front-loading client acquisition
Automatically finds and applies to relevant projects
"""

import requests
from datetime import datetime
import json
from openai import OpenAI

class UpworkAutomation:
    """
    Automates Upwork job discovery and proposal generation
    Target: 20-25 proposals per day (Nick's strategy)
    """
    
    def __init__(self):
        self.client = OpenAI()
        self.proposals_sent_today = 0
        self.target_proposals_per_day = 25
        self.niches = []
        
    def set_niches(self, niches):
        """
        Set multiple niches to target (Nick's multi-niche strategy)
        Example: ["AI automation", "web scraping", "data analysis"]
        """
        self.niches = niches
        
    def generate_search_queries(self, niche):
        """
        AI-generated search queries for Upwork
        """
        prompt = f"""Generate 5 effective Upwork search queries for finding {niche} projects.

These should be specific enough to find quality projects but broad enough to get results.

Respond in JSON format:
{{
    "queries": ["query1", "query2", "query3", "query4", "query5"]
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are an Upwork expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            result = json.loads(response.choices[0].message.content)
            return result["queries"]
        except Exception as e:
            return [niche]  # Fallback to basic search
    
    def analyze_job_posting(self, job_description, job_title, budget):
        """
        AI analyzes if a job is worth applying to
        Returns: score (0-100) and reasoning
        """
        prompt = f"""Analyze this Upwork job posting:

Title: {job_title}
Budget: {budget}
Description: {job_description}

Evaluate based on:
1. Budget adequacy (is it worth the time?)
2. Scope clarity (is it well-defined?)
3. Client quality indicators
4. Likelihood of success
5. Red flags

Respond in JSON:
{{
    "score": 0-100,
    "worth_applying": true/false,
    "reasoning": "explanation",
    "red_flags": ["flag1", "flag2"],
    "key_requirements": ["req1", "req2"]
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are an expert at evaluating Upwork jobs."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {
                "score": 50,
                "worth_applying": False,
                "reasoning": f"Error analyzing: {str(e)}",
                "red_flags": [],
                "key_requirements": []
            }
    
    def generate_upwork_proposal(self, job_title, job_description, client_info):
        """
        Generate a winning Upwork proposal
        Nick's strategy: Personalized, value-focused, clear CTA
        """
        prompt = f"""Create a winning Upwork proposal for:

Job Title: {job_title}
Job Description: {job_description}
Client: {client_info.get('name', 'Potential Client')}
Client History: {client_info.get('jobs_posted', 'Unknown')} jobs posted

The proposal should:
1. Hook them immediately (first sentence)
2. Show you understand their specific problem
3. Demonstrate relevant experience
4. Provide a clear solution approach
5. Include a soft CTA
6. Be 150-200 words (Upwork sweet spot)
7. End with a question to encourage response

Respond in JSON:
{{
    "proposal_text": "the full proposal",
    "estimated_time": "X hours/days",
    "key_selling_points": ["point1", "point2"]
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a top-rated Upwork freelancer who wins 40% of proposals."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8
            )
            
            proposal = json.loads(response.choices[0].message.content)
            proposal["generated_at"] = datetime.now().isoformat()
            proposal["proposal_id"] = f"UP-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            
            self.proposals_sent_today += 1
            
            return proposal
        except Exception as e:
            return {
                "error": str(e),
                "proposal_text": "Error generating proposal"
            }
    
    def create_loom_script_for_upwork(self, job_title, client_name, key_pain_points):
        """
        Generate Loom video script for Upwork proposal
        Nick's secret weapon: Stand out with video
        """
        prompt = f"""Create a 60-90 second Loom video script for an Upwork proposal:

Job: {job_title}
Client: {client_name}
Pain Points: {', '.join(key_pain_points)}

Script structure:
1. Hook (5 seconds): Grab attention with their name/problem
2. Empathy (15 seconds): Show you understand their situation
3. Solution (30 seconds): Briefly explain your approach
4. Proof (20 seconds): Quick credibility builder
5. CTA (10 seconds): Soft next step

Respond in JSON:
{{
    "hook": "text",
    "empathy": "text",
    "solution": "text",
    "proof": "text",
    "cta": "text",
    "full_script": "complete script with timing"
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a video marketing expert creating compelling Loom scripts."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}
    
    def simulate_job_search(self, niche):
        """
        Simulates finding jobs on Upwork
        In production, this would use Upwork's RSS feed or API
        """
        # Generate realistic job data
        job_types = [
            "Build AI automation system",
            "Web scraping project",
            "Data analysis dashboard",
            "API integration",
            "Process automation"
        ]
        
        budgets = ["$500-$1000", "$1000-$5000", "$5000+", "Hourly: $50-100"]
        
        # Simulate 10 jobs found
        jobs = []
        for i in range(10):
            job = {
                "id": f"job_{i}",
                "title": f"{job_types[i % len(job_types)]} for {niche}",
                "budget": budgets[i % len(budgets)],
                "description": f"Looking for expert in {niche} to help with project...",
                "client": {
                    "name": f"Client_{i}",
                    "jobs_posted": i + 1,
                    "rating": 4.5 + (i * 0.05)
                },
                "posted": "2 hours ago"
            }
            jobs.append(job)
        
        return jobs
    
    def auto_apply_workflow(self, niche, max_applications=5):
        """
        Complete automated workflow:
        1. Search for jobs
        2. Analyze each job
        3. Generate proposal for good ones
        4. Track results
        """
        results = {
            "niche": niche,
            "jobs_found": 0,
            "jobs_analyzed": 0,
            "proposals_generated": 0,
            "applications": []
        }
        
        # Find jobs
        jobs = self.simulate_job_search(niche)
        results["jobs_found"] = len(jobs)
        
        # Analyze and apply
        for job in jobs[:max_applications]:
            # Analyze job
            analysis = self.analyze_job_posting(
                job["description"],
                job["title"],
                job["budget"]
            )
            results["jobs_analyzed"] += 1
            
            # If worth applying, generate proposal
            if analysis["worth_applying"] and analysis["score"] >= 70:
                proposal = self.generate_upwork_proposal(
                    job["title"],
                    job["description"],
                    job["client"]
                )
                
                # Generate Loom script
                loom_script = self.create_loom_script_for_upwork(
                    job["title"],
                    job["client"]["name"],
                    analysis.get("key_requirements", [])
                )
                
                results["proposals_generated"] += 1
                results["applications"].append({
                    "job": job,
                    "analysis": analysis,
                    "proposal": proposal,
                    "loom_script": loom_script
                })
        
        return results
    
    def get_daily_stats(self):
        """
        Get today's performance stats
        """
        return {
            "proposals_sent_today": self.proposals_sent_today,
            "target": self.target_proposals_per_day,
            "progress": f"{(self.proposals_sent_today / self.target_proposals_per_day * 100):.1f}%",
            "remaining": self.target_proposals_per_day - self.proposals_sent_today
        }
