            else:
                return "supplements"  # Default fallback
                
        except Exception as e:
            print(f"Error detecting category: {str(e)}")
            return "supplements"  # Default fallback
    
    def research_pain_points(self, product_name: str, product_description: str = "", category: str = None) -> Dict[str, Any]:
        """
        Use Perplexity AI to research pain points that the product solves
        Customized research based on product category
        """
        try:
            # Auto-detect category if not provided
            if not category:
                category = self.detect_product_category(product_name, product_description)
            
            config = self.category_configs.get(category, self.category_configs["supplements"])
            
            prompt = f"""
            Research the pain points that {product_name} solves in the {category} category.
            Product description: {product_description}
            
            Focus your research on: {config['research_focus']}
            
            Please provide:
            1. A list of main pain points this product addresses (specific to {category})
            2. Customer quotes or testimonials that mention these pain points
            3. Common language customers use when describing these problems
            4. Specific benefits this product category typically provides
            
            Format the response as JSON with keys: pain_points, customer_quotes, common_language, category_benefits
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are a market research expert specializing in {category} products. Provide realistic, detailed research based on common customer experiences in this category."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Try to extract JSON, fallback to category-specific structure
            try:
                research_data = json.loads(content)
            except:
                # Category-specific fallback data
                research_data = self._get_fallback_research_data(category, product_name)
            
            research_data["detected_category"] = category
            return research_data
            
        except Exception as e:
            print(f"Error in pain point research: {str(e)}")
            return self._get_fallback_research_data(category or "supplements", product_name)
    
    def _get_fallback_research_data(self, category: str, product_name: str) -> Dict[str, Any]:
        """
        Provide fallback research data based on category
        """
        fallback_data = {
            "supplements": {
                "pain_points": ["Low energy levels", "Poor health", "Nutritional gaps", "Wellness goals"],
                "customer_quotes": ["Finally have energy again", "Feel so much healthier", "This actually works"],
                "common_language": ["energy", "healthy", "effective", "natural", "results"]
            },
            "electronics": {
                "pain_points": ["Slow performance", "Poor battery life", "Compatibility issues", "High prices"],
                "customer_quotes": ["Works perfectly", "Great value for money", "So much faster now"],
                "common_language": ["fast", "reliable", "compatible", "affordable", "quality"]
            },
            "beauty": {
                "pain_points": ["Skin issues", "Aging concerns", "Product reactions", "Lack of results"],
                "customer_quotes": ["My skin looks amazing", "Finally found something that works", "No irritation"],
                "common_language": ["glowing", "smooth", "gentle", "effective", "beautiful"]
            },
            "outdoor": {
                "pain_points": ["Gear failure", "Weather issues", "Comfort problems", "Durability concerns"],
                "customer_quotes": ["Survived the storm", "So comfortable", "Built to last"],
                "common_language": ["durable", "waterproof", "comfortable", "reliable", "adventure-ready"]
            },
            "fashion": {
                "pain_points": ["Poor fit", "Style issues", "Quality problems", "Limited options"],
                "customer_quotes": ["Perfect fit", "Love the style", "Great quality"],
                "common_language": ["stylish", "comfortable", "flattering", "versatile", "trendy"]
            },
            "home": {
                "pain_points": ["Space issues", "Organization problems", "Poor quality", "Difficult setup"],
                "customer_quotes": ["Transformed my space", "So much more organized", "Easy to assemble"],
                "common_language": ["organized", "spacious", "functional", "stylish", "practical"]
            },
            "fitness": {
                "pain_points": ["Lack of results", "Equipment failure", "Motivation issues", "Comfort problems"],
                "customer_quotes": ["Amazing results", "So motivating", "Perfect for my workouts"],
                "common_language": ["results", "effective", "motivating", "comfortable", "strong"]
            }
        }