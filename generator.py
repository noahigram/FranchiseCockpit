import random
import anthropic
import streamlit as st
from scenarios import SCENARIO_DATABASE
import requests
import json

# Lists of scenario components for random generation
BUSINESS_ASPECTS = [
    "finance",
    "marketing",
    "operations",
    "customer service",
    "staff management",
    "supply chain",
    "technology",
    "location",
    "regulations",
    "competition"
]

BEST_CASE_INVESTMENTS = [
    "Hire a specialized consultant",
    "Implement a cutting-edge solution",
    "Invest in premium resources",
    "Develop a comprehensive strategy",
    "Engage industry experts",
    "Launch an innovative approach",
    "Acquire top-tier assets",
    "Deploy high-end technology",
    "Orchestrate a strategic overhaul",
    "Establish a best-in-class system"
]

WORST_CASE_APPROACHES = [
    "Handle it internally",
    "Use a minimal approach",
    "Implement a basic solution",
    "Delegate to existing staff",
    "Apply a low-cost alternative",
    "Take a conservative approach",
    "Wait and see before acting",
    "Make incremental changes",
    "Use existing resources",
    "Find a temporary workaround"
]

BUSINESS_IMPACT_DESCRIPTIONS = [
    "This will have significant implications for your franchise's future.",
    "Your decision could substantially affect your franchise's performance.",
    "This choice will shape your business trajectory for years to come.",
    "The path you choose will determine your competitive positioning.",
    "Your approach to this challenge will define your market presence.",
    "The way you handle this situation will impact customer perception.",
    "Your strategy here will influence operational efficiency long-term.",
    "This decision point represents a pivotal moment for your franchise.",
    "How you address this issue will affect your brand reputation.",
    "The direction you take now will influence your financial stability."
]

def generate_scenario_topics(business_profile, uploaded_files=None, custom_topic=None):
    """Generate a list of relevant scenario topics based on the business profile"""
    
    # Create a prompt for topic generation
    prompt = f"""You are a business scenario generator for a franchise management simulator. Based on the following business profile, generate 5-7 relevant scenario topics that would be most impactful for this business.

Business Profile:
{business_profile}

{f'Custom Topic (if relevant): {custom_topic}' if custom_topic else ''}

Generate a list of scenario topics that:
1. Are specific to the business's industry and situation
2. Cover different aspects of business management (operations, finance, marketing, etc.)
3. Include both immediate challenges and long-term opportunities
4. Are realistic and actionable
5. Would have significant impact on business metrics

Format your response as a simple list of topics, one per line, with no numbers or bullet points. Keep each topic concise (2-4 words). Example:
Staff Training Program
Marketing Campaign
Supply Chain Optimization
..."""

    try:
        # Prepare the API request
        url = "https://api.protobots.ai/proto_bots/generate_v2"
        
        # Headers
        headers = {
            "Authorization": f"Bearer {st.secrets['PROTOBOTS_API_KEY']}"
        }
        
        # Form data
        data = {
            "_id": "64f9ec54981dcfe5b966e5a3",  # Replace with your actual bot ID
            "stream": "false",
            "message.assistant.0": "I am a business scenario generator. I will create relevant scenario topics based on the business profile.",
            "message.user.1": prompt
        }
        
        # Make the API request
        response = requests.post(url, headers=headers, data=data)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse the response
            response_data = response.json()
            
            # Extract the topics from the response
            # The response structure is: {"object": "```text\nTopic 1\nTopic 2\n...\n```"}
            topics_text = response_data.get('object', '')
            
            if topics_text:
                try:
                    # Clean the response text
                    # Remove any markdown code block markers if present
                    topics_text = topics_text.replace('```text', '').replace('```', '').strip()
                    
                    # Split the text into lines and clean each line
                    # Remove any numbers or bullet points from the start of each line
                    topics = []
                    for topic in topics_text.split('\n'):
                        topic = topic.strip()
                        # Remove any numbers or bullet points from the start
                        topic = topic.lstrip('0123456789. -•*')
                        if topic:
                            topics.append(topic)
                    
                    # Validate that we got a list of strings
                    if topics:
                        print("Successfully generated topics:", topics)  # Debug print
                        return topics
                    else:
                        print("No valid topics found in response")
                        print("Response:", topics_text)
                        raise Exception("No valid topics found in response")
                except Exception as e:
                    print(f"Error parsing topics: {str(e)}")
                    print("Raw response:", topics_text)
                    raise Exception("Failed to parse topics from response")
            else:
                print("No topics found in response")
                print("Response:", response_data)
                raise Exception("No topics found in response")
        else:
            print(f"API request failed with status code {response.status_code}")
            print("Response:", response.text)
            raise Exception(f"API request failed with status code {response.status_code}")
            
    except Exception as e:
        print(f"Error in API call: {str(e)}")
        # Fallback to some generic topics
        return [
            "Staff Management",
            "Marketing Strategy",
            "Financial Planning",
            "Customer Service",
            "Technology Implementation"
        ]

def generate_scenario(topic, business_profile):
    """Generate a scenario based on the topic and business profile"""
    
    # Create a prompt for scenario generation
    prompt = f"""You are a business scenario generator for a franchise management simulator. Create a concise scenario based on the following topic and business profile.

Topic: {topic}
Business Profile: {business_profile}

The scenario should follow this exact JSON structure:
{{
    "description": "A brief description of the situation (1-2 sentences)",
    "best_case": {{
        "title": "A short title for the best case option (3-5 words)",
        "description": "Brief description of the best case approach (1-2 sentences)",
        "consequences": {{
            "cash_flow": <integer between -100000 and 50000>,
            "customer_satisfaction": <integer between -25 and 25>,
            "growth_potential": <integer between -25 and 25>,
            "risk_level": <integer between -25 and 25>
        }},
        "next_scenarios": ["<scenario1>", "<scenario2>"]
    }},
    "worst_case": {{
        "title": "A short title for the worst case option (3-5 words)",
        "description": "Brief description of the worst case approach (1-2 sentences)",
        "consequences": {{
            "cash_flow": <integer between -100000 and 50000>,
            "customer_satisfaction": <integer between -25 and 25>,
            "growth_potential": <integer between -25 and 25>,
            "risk_level": <integer between -25 and 25>
        }},
        "next_scenarios": ["<scenario1>", "<scenario2>"]
    }}
}}

Guidelines:
1. Keep all descriptions extremely concise - no more than 1-2 sentences
2. Make the scenario realistic and business-focused
3. Best case should be ambitious but achievable
4. Worst case should be conservative but not disastrous
5. Consequences should be balanced and make sense for the situation
6. Next scenarios should be relevant to the current scenario
7. Ensure all numeric values are integers
8. Make the scenario specific to the business profile provided

Generate a scenario that follows this structure exactly."""

    try:
        # Prepare the API request
        url = "https://api.protobots.ai/proto_bots/generate_v2"
        
        # Headers
        headers = {
            "Authorization": f"Bearer {st.secrets['PROTOBOTS_API_KEY']}"
        }
        
        # Form data
        data = {
            "_id": "64f9ec54981dcfe5b966e5a3",  # Replace with your actual bot ID
            "stream": "false",
            "message.assistant.0": "I am a business scenario generator. I will create realistic franchise management scenarios following the specified JSON structure.",
            "message.user.1": prompt
        }
        
        # Make the API request
        response = requests.post(url, headers=headers, data=data)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse the response
            response_data = response.json()
            
            # Extract the generated scenario from the response
            # The response structure is: {"object": "```json\n{...}\n```"}
            scenario_text = response_data.get('object', '')
            
            if scenario_text:
                try:
                    # Clean the response text to ensure it's valid JSON
                    # Remove any markdown code block markers if present
                    scenario_text = scenario_text.replace('```json', '').replace('```', '').strip()
                    
                    # Parse the JSON response
                    scenario = json.loads(scenario_text)
                    
                    # Validate the structure and values
                    if not all(key in scenario for key in ["description", "best_case", "worst_case"]):
                        raise ValueError("Missing required keys in scenario structure")
                        
                    if not all(key in scenario["best_case"] for key in ["title", "description", "consequences", "next_scenarios"]):
                        raise ValueError("Missing required keys in best_case structure")
                        
                    if not all(key in scenario["worst_case"] for key in ["title", "description", "consequences", "next_scenarios"]):
                        raise ValueError("Missing required keys in worst_case structure")
            
                    if not all(key in scenario["best_case"]["consequences"] for key in ["cash_flow", "customer_satisfaction", "growth_potential", "risk_level"]):
                        raise ValueError("Missing required keys in best_case consequences")
            
                    if not all(key in scenario["worst_case"]["consequences"] for key in ["cash_flow", "customer_satisfaction", "growth_potential", "risk_level"]):
                        raise ValueError("Missing required keys in worst_case consequences")
            
                    return scenario
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error: {str(e)}")
                    print("Raw response:", scenario_text)
                    raise Exception("Failed to parse scenario as JSON")
            else:
                print("No scenario found in response")
                print("Response:", response_data)
                raise Exception("No scenario found in response")
        else:
            print(f"API request failed with status code {response.status_code}")
            print("Response:", response.text)
            raise Exception(f"API request failed with status code {response.status_code}")
        
    except Exception as e:
        print(f"Error in API call: {str(e)}")
        # Fallback to random generation if API fails
        return generate_random_scenario(topic)

def generate_random_scenario(topic):
    """Fallback function to generate a random scenario if API fails"""
    # Generate scenario description
    aspect = random.choice([
        "finance",
        "marketing",
        "operations",
        "customer service",
        "staff management",
        "supply chain",
        "technology",
        "location",
        "regulations",
        "competition"
    ])
    
    scenario_description = f"Your franchise is facing a decision regarding {topic.lower()} that affects your {aspect}."
    
    # Generate best case option
    best_action = random.choice([
        "Hire a specialized consultant",
        "Implement a cutting-edge solution",
        "Invest in premium resources",
        "Develop a comprehensive strategy",
        "Engage industry experts",
        "Launch an innovative approach",
        "Acquire top-tier assets",
        "Deploy high-end technology",
        "Orchestrate a strategic overhaul",
        "Establish a best-in-class system"
    ])
    best_desc = f"{best_action} to address the {topic.lower()} situation."
    
    # Generate consequences for best case (generally positive with some cash flow impact)
    best_consequences = {
        "cash_flow": random.randint(-40000, -10000),
        "customer_satisfaction": random.randint(10, 25),
        "growth_potential": random.randint(10, 25),
        "risk_level": random.randint(-20, 5)
    }
    
    # Generate worst case option
    worst_action = random.choice([
        "Handle it internally",
        "Use a minimal approach",
        "Implement a basic solution",
        "Delegate to existing staff",
        "Apply a low-cost alternative",
        "Take a conservative approach",
        "Wait and see before acting",
        "Make incremental changes",
        "Use existing resources",
        "Find a temporary workaround"
    ])
    worst_desc = f"{worst_action} for the {topic.lower()} situation."
    
    # Generate consequences for worst case (mixed, generally lower cost but fewer benefits)
    worst_consequences = {
        "cash_flow": random.randint(-15000, 5000),  # May sometimes save money
        "customer_satisfaction": random.randint(-15, 10),
        "growth_potential": random.randint(-10, 5),
        "risk_level": random.randint(-5, 15)
    }
    
    # Generate next scenarios (use 2 random topics)
    next_scenarios = [
        "Staff Management",
        "Marketing Strategy",
        "Financial Planning",
        "Customer Service",
        "Technology Implementation"
    ]
    next_scenarios = random.sample(next_scenarios, 2)
    
    # Construct the full scenario
    scenario = {
        "description": scenario_description,
        "best_case": {
            "title": f"Strategic {topic} Initiative",
            "description": best_desc,
            "consequences": best_consequences,
            "next_scenarios": next_scenarios
        },
        "worst_case": {
            "title": f"Practical {topic} Approach",
            "description": worst_desc,
            "consequences": worst_consequences,
            "next_scenarios": next_scenarios
        }
    }
    
    return scenario

def generate_simulation_analysis(scenario_history, final_metrics, business_profile):
    """Generate a brief analysis of the user's decisions and predict business outlook"""
    
    # Format the scenario history for the prompt
    decisions_text = ""
    for i, scenario in enumerate(scenario_history):
        decisions_text += f"Decision {i+1}: {scenario['topic']}\n"
        decisions_text += f"Choice: {scenario['choice']} - {scenario['title']}\n"
        decisions_text += f"Impact: {scenario['consequences']}\n\n"
    
    # Format the final metrics
    metrics_text = "Final Business Metrics:\n"
    metrics_text += f"- Cash Flow: ${final_metrics['cash_flow']}\n"
    metrics_text += f"- Customer Satisfaction: {final_metrics['customer_satisfaction']}%\n"
    metrics_text += f"- Growth Potential: {final_metrics['growth_potential']}%\n"
    metrics_text += f"- Risk Level: {final_metrics['risk_level']}%\n"
    
    # Create the analysis prompt
    analysis_prompt = f"""You are a franchise business analyst. Review the following decisions made by a franchise owner in a simulation and provide a detailed analysis.

Business Profile:
{business_profile}

{decisions_text}
{metrics_text}

Please provide:
1. A detailed analysis (3-4 sentences) of the user's decision-making patterns and strategy, including specific examples from their choices
2. A comprehensive assessment (3-4 sentences) of the business's health and likely future performance based on current metrics, with specific numbers and trends
3. Two specific recommendations for future business decisions based on the observed patterns and current business state

Keep your response under 200 words and be direct and insightful. Focus on concrete examples and specific metrics. If the business is struggling, provide constructive feedback on how to improve. If it's doing well, suggest ways to maintain and build on the success."""

    try:
        # Prepare the API request
        url = "https://api.protobots.ai/proto_bots/generate_v2"
        
        # Headers
        headers = {
            "Authorization": f"Bearer {st.secrets['PROTOBOTS_API_KEY']}"
        }
        
        # Form data
        data = {
            "_id": "64f9ec54981dcfe5b966e5a3",  # Replace with your actual bot ID
            "stream": "false",
            "message.assistant.0": "I am a franchise business analyst. I will analyze your business decisions and provide detailed insights.",
            "message.user.1": analysis_prompt
        }
        
        # Make the API request
        response = requests.post(url, headers=headers, data=data)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse the response
            response_data = response.json()
            
            # Extract the analysis from the response
            # The response structure is: {"object": "```text\n...\n```"}
            analysis_text = response_data.get('object', '')
            
            if analysis_text:
                try:
                    # Clean the response text
                    # Remove any markdown code block markers if present
                    analysis_text = analysis_text.replace('```text', '').replace('```', '').strip()
                    
                    # Try to parse as JSON first
                    try:
                        analysis = json.loads(analysis_text)
                        if isinstance(analysis, str):
                            return analysis.strip()
                        elif isinstance(analysis, dict):
                            return analysis.get('analysis', '').strip()
                    except json.JSONDecodeError:
                        # If not JSON, return the text directly
                        return analysis_text.strip()
                except Exception as e:
                    print(f"Error processing analysis text: {str(e)}")
                    print("Raw response:", analysis_text)
                    raise Exception("Failed to process analysis text")
            else:
                print("No analysis found in response")
                print("Response:", response_data)
                raise Exception("No analysis found in response")
        else:
            print(f"API request failed with status code {response.status_code}")
            print("Response:", response.text)
            raise Exception(f"API request failed with status code {response.status_code}")
            
    except Exception as e:
        print(f"Error in API call: {str(e)}")
        # Fallback to detailed analysis based on metrics and history
        analysis = []
        
        # Analyze decision patterns
        best_case_count = sum(1 for s in scenario_history if s['choice'] == "Best Case")
        worst_case_count = sum(1 for s in scenario_history if s['choice'] == "Worst Case")
        
        if best_case_count > worst_case_count:
            analysis.append(f"Your decision-making approach shows a preference for ambitious, growth-oriented strategies, choosing the best-case option in {best_case_count} out of {len(scenario_history)} scenarios.")
        elif worst_case_count > best_case_count:
            analysis.append(f"Your decision-making approach shows a preference for conservative, risk-averse strategies, choosing the worst-case option in {worst_case_count} out of {len(scenario_history)} scenarios.")
        else:
            analysis.append(f"Your decision-making approach shows a balanced strategy, choosing an equal mix of ambitious and conservative options across {len(scenario_history)} scenarios.")
        
        # Analyze current business state
        if final_metrics['cash_flow'] < 50000:
            analysis.append(f"Your current cash position of ${final_metrics['cash_flow']} indicates financial strain. This may limit your ability to invest in growth opportunities.")
        elif final_metrics['cash_flow'] < 100000:
            analysis.append(f"Your current cash position of ${final_metrics['cash_flow']} is moderate. While stable, you may want to build reserves for future opportunities.")
        else:
            analysis.append(f"Your strong cash position of ${final_metrics['cash_flow']} provides a solid foundation for growth and investment opportunities.")
        
        # Analyze customer satisfaction
        if final_metrics['customer_satisfaction'] < 40:
            analysis.append(f"Customer satisfaction at {final_metrics['customer_satisfaction']}% needs immediate attention. Focus on improving service quality and customer experience.")
        elif final_metrics['customer_satisfaction'] < 60:
            analysis.append(f"Customer satisfaction at {final_metrics['customer_satisfaction']}% has room for improvement. Consider enhancing customer service initiatives.")
        else:
            analysis.append(f"Strong customer satisfaction at {final_metrics['customer_satisfaction']}% indicates effective customer service. Look for ways to maintain and build on this success.")
        
        # Analyze growth potential
        if final_metrics['growth_potential'] < 40:
            analysis.append(f"Growth potential at {final_metrics['growth_potential']}% suggests limited expansion opportunities. Focus on stabilizing current operations before pursuing growth.")
        elif final_metrics['growth_potential'] < 60:
            analysis.append(f"Growth potential at {final_metrics['growth_potential']}% shows moderate expansion possibilities. Look for strategic opportunities to accelerate growth.")
        else:
            analysis.append(f"High growth potential at {final_metrics['growth_potential']}% indicates strong expansion opportunities. Consider developing a detailed growth strategy.")
        
        # Analyze risk level
        if final_metrics['risk_level'] > 60:
            analysis.append(f"High risk level at {final_metrics['risk_level']}% requires immediate attention. Focus on risk mitigation and stability measures.")
        elif final_metrics['risk_level'] > 40:
            analysis.append(f"Moderate risk level at {final_metrics['risk_level']}% suggests careful monitoring. Consider implementing additional risk management strategies.")
        else:
            analysis.append(f"Low risk level at {final_metrics['risk_level']}% indicates stable operations. Look for opportunities to optimize while maintaining this stability.")
        
        # Add specific recommendations
        if final_metrics['cash_flow'] < 50000:
            analysis.append("Recommendations: 1) Implement cost-cutting measures to improve cash flow. 2) Focus on high-margin products or services to boost profitability.")
        elif final_metrics['customer_satisfaction'] < 40:
            analysis.append("Recommendations: 1) Conduct customer surveys to identify specific pain points. 2) Invest in staff training to improve service quality.")
        elif final_metrics['growth_potential'] < 40:
            analysis.append("Recommendations: 1) Review and optimize current operations. 2) Research new market opportunities aligned with your strengths.")
        else:
            analysis.append("Recommendations: 1) Develop a detailed expansion strategy. 2) Consider investing in technology or staff to support growth.")
        
        return "\n".join(analysis)

def generate_random_business_profile():
    """Generate a random business profile using the LLM"""
    
    prompt = """Generate a realistic business profile for a franchise. Include the following sections:
    - Industry
    - Location
    - Size
    - Target Market
    - Current Challenges (3-4 points)
    - Opportunities (3-4 points)
    - Goals (2-3 points)

    Format the response as a JSON object with these exact keys:
    {
        "industry": "string",
        "location": "string",
        "size": "string",
        "target_market": "string",
        "challenges": ["string"],
        "opportunities": ["string"],
        "goals": ["string"]
    }

    Make the profile realistic and specific, with concrete details that would be useful for generating business scenarios. Ensure the profile is unique and different from previous generations."""

    try:
        # Prepare the API request
        url = "https://api.protobots.ai/proto_bots/generate_v2"
        
        # Headers
        headers = {
            "Authorization": f"Bearer {st.secrets['PROTOBOTS_API_KEY']}"
        }
        
        # Form data
        data = {
            "_id": "64f9ec54981dcfe5b966e5a3",  # Replace with your actual bot ID
            "stream": "false",
            "message.assistant.0": "I am a business profile generator. I will create realistic franchise business profiles following the specified JSON structure.",
            "message.user.1": prompt
        }
        
        # Make the API request
        response = requests.post(url, headers=headers, data=data)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse the response
            response_data = response.json()
            
            # Extract the profile from the response
            # The response structure is: {"object": "```json\n{...}\n```"}
            profile_text = response_data.get('object', '')
            
            if profile_text:
                try:
                    # Clean the response text to ensure it's valid JSON
                    # Remove any markdown code block markers if present
                    profile_text = profile_text.replace('```json', '').replace('```', '').strip()
                    
                    # Parse the JSON response
                    profile = json.loads(profile_text)
                    
                    # Validate the required keys are present
                    required_keys = ["industry", "location", "size", "target_market", "challenges", "opportunities", "goals"]
                    if not all(key in profile for key in required_keys):
                        raise ValueError("Missing required keys in profile structure")
                    
                    # Format the profile as a markdown string
                    formatted_profile = f"""**Industry:** {profile['industry']}

**Location:** {profile['location']}

**Size:** {profile['size']}

**Target Market:** {profile['target_market']}

**Current Challenges:**
{chr(10).join(f"- {challenge}" for challenge in profile['challenges'])}

**Opportunities:**
{chr(10).join(f"- {opportunity}" for opportunity in profile['opportunities'])}

**Goals:**
{chr(10).join(f"- {goal}" for goal in profile['goals'])}"""
                    
                    print("Successfully generated new business profile")  # Debug print
                    return formatted_profile
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error: {str(e)}")
                    print("Raw response:", profile_text)
                    raise Exception("Failed to parse profile as JSON")
            else:
                print("No profile found in response")
                print("Response:", response_data)
                raise Exception("No profile found in response")
        else:
            print(f"API request failed with status code {response.status_code}")
            print("Response:", response.text)
            raise Exception(f"API request failed with status code {response.status_code}")
        
    except Exception as e:
        print(f"Error in API call: {str(e)}")
        # Instead of falling back to a hardcoded profile, raise the exception
        raise Exception(f"Failed to generate business profile: {str(e)}") 