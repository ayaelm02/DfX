import os
import numpy as np
from PIL import Image
import openai
import streamlit as st
import json
from dataclasses import dataclass
from typing import List, Dict, Optional
import base64

@dataclass
class ObjectDescription:
    general_description: str
    components: List[str]
    dimensions: Dict[str, str]
    materials: List[str]
    key_features: List[str]
    intended_use: List[str]

@dataclass
class DesignBrainstorming:
    components_alternatives: List[Dict[str, List[str]]]
    material_options: List[Dict[str, List[str]]]
    ergonomic_considerations: List[Dict[str, List[str]]]
    market_analysis: Dict[str, List[str]]
    hazard_analysis: List[Dict[str, List[str]]]
    innovation_opportunities: List[str]
    design_tradeoffs: List[Dict[str, List[str]]]

@dataclass
class DfXSpecification:
    category: str
    specifications: List[str]
    requirements: List[str]
    constraints: List[str]
    recommendations: List[str]

def clean_json_response(text):
    """Clean the GPT response to get valid JSON."""
    start = text.find('{')
    end = text.rfind('}')
    
    if start == -1 or end == -1:
        raise ValueError("No valid JSON object found in response")
        
    json_str = text[start:end + 1]
    json_str = json_str.replace('json', '').replace('', '')
    return json_str.strip()

class DfXAnalyzer:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.categories = {
            'manufacturability': 'Manufacturing process and production specifications',
            'reliability': 'Product reliability and durability specifications',
            'sustainability': 'Environmental and resource efficiency specifications',
            'usability': 'User interaction and accessibility specifications',
            'cost': 'Cost-related specifications and requirements',
            'safety': 'Safety standards and requirements',
            'performance': 'Performance specifications and benchmarks',
            'maintainability': 'Maintenance and serviceability specifications',
            'scalability': 'Growth and adaptation specifications',
            'compliance': 'Regulatory and standards compliance specifications'
        }

    def encode_image(self, image_path):
        """Encode image to base64 string"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def generate_object_description(self, image_path: str) -> ObjectDescription:
        """Generate comprehensive object description from the design image"""
        base64_image = self.encode_image(image_path)
        
        prompt = """Analyze this design image and provide a comprehensive object description.
        
Format your response EXACTLY as a JSON object like this:
{
    "general_description": "detailed overview of the object",
    "components": [
        "component_1 with description",
        "component_2 with description",
        ...
    ],
    "dimensions": {
        "length": "value",
        "width": "value",
        "height": "value",
        "other_relevant_dimensions": "value"
    },
    "materials": [
        "material_1 with properties",
        "material_2 with properties",
        ...
    ],
    "key_features": [
        "feature_1 description",
        "feature_2 description",
        ...
    ],
    "intended_use": [
        "primary use case",
        "secondary use case",
        ...
    ]
}

Be as specific and technical as possible. Include estimated measurements and material properties where visible. Provide ONLY the JSON response, no other text."""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )

        try:
            response_text = response.choices[0].message.content
            json_str = clean_json_response(response_text)
            results = json.loads(json_str)
            
            return ObjectDescription(
                general_description=results['general_description'],
                components=results['components'],
                dimensions=results['dimensions'],
                materials=results['materials'],
                key_features=results['key_features'],
                intended_use=results['intended_use']
            )
                
        except (json.JSONDecodeError, Exception) as e:
            st.error(f"Error generating object description: {e}")
            return None

    def generate_brainstorming(self, image_path: str) -> DesignBrainstorming:
        """Generate comprehensive design brainstorming analysis"""
        base64_image = self.encode_image(image_path)
        
        prompt = """Analyze this design and provide a comprehensive brainstorming analysis for alternative design approaches.

Format your response EXACTLY as a JSON object like this:
{
    "components_alternatives": [
        {
            "component_name": [
                "alternative_approach_1 with pros/cons",
                "alternative_approach_2 with pros/cons",
                ...
            ]
        }
    ],
    "material_options": [
        {
            "component_or_area": [
                "material_option_1 with properties and justification",
                "material_option_2 with properties and justification",
                ...
            ]
        }
    ],
    "ergonomic_considerations": [
        {
            "interaction_point": [
                "ergonomic_consideration_1",
                "ergonomic_consideration_2",
                ...
            ]
        }
    ],
    "market_analysis": {
        "competitors": [
            "competitor_1 with key features",
            "competitor_2 with key features",
            ...
        ],
        "market_gaps": [
            "opportunity_1",
            "opportunity_2",
            ...
        ],
        "user_needs": [
            "unmet_need_1",
            "unmet_need_2",
            ...
        ]
    },
    "hazard_analysis": [
        {
            "hazard_category": [
                "potential_hazard_1 with mitigation",
                "potential_hazard_2 with mitigation",
                ...
            ]
        }
    ],
    "innovation_opportunities": [
        "innovation_idea_1",
        "innovation_idea_2",
        ...
    ],
    "design_tradeoffs": [
        {
            "tradeoff_category": [
                "option_1 with impact analysis",
                "option_2 with impact analysis",
                ...
            ]
        }
    ]
}

Provide detailed analysis with specific examples, materials, technologies, and approaches. Include pros/cons where relevant. Provide ONLY the JSON response, no other text."""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=4000
        )

        try:
            response_text = response.choices[0].message.content
            json_str = clean_json_response(response_text)
            results = json.loads(json_str)
            
            return DesignBrainstorming(
                components_alternatives=results['components_alternatives'],
                material_options=results['material_options'],
                ergonomic_considerations=results['ergonomic_considerations'],
                market_analysis=results['market_analysis'],
                hazard_analysis=results['hazard_analysis'],
                innovation_opportunities=results['innovation_opportunities'],
                design_tradeoffs=results['design_tradeoffs']
            )
                
        except (json.JSONDecodeError, Exception) as e:
            st.error(f"Error generating brainstorming analysis: {e}")
            return None

    def analyze_specifications(self, image_path: str, criteria: List[str]) -> Dict[str, DfXSpecification]:
        """Generate detailed specifications from the design image"""
        base64_image = self.encode_image(image_path)
        
        prompt = f"""Analyze this design image and generate comprehensive specifications for the following Design for X (DfX) categories: {', '.join(criteria)}

For each category, provide:
1. Detailed specifications (at least 5-7 specific technical requirements)
2. Key requirements (4-5 essential criteria that must be met)
3. Design constraints (3-4 limitations or boundaries)
4. Detailed recommendations (4-5 specific improvement suggestions)

Format your response EXACTLY as a JSON object like this:
{{
    "category_name": {{
        "specifications": [
            "detailed_spec_1",
            "detailed_spec_2",
            ...
        ],
        "requirements": [
            "requirement_1",
            "requirement_2",
            ...
        ],
        "constraints": [
            "constraint_1",
            "constraint_2",
            ...
        ],
        "recommendations": [
            "recommendation_1",
            "recommendation_2",
            ...
        ]
    }}
}}

Be as specific and technical as possible in the specifications. Include numerical values, standards, and precise requirements where applicable. Provide ONLY the JSON response, no other text."""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=4000
        )

        analysis_results = {}
        try:
            response_text = response.choices[0].message.content
            json_str = clean_json_response(response_text)
            results = json.loads(json_str)
            
            for category, data in results.items():
                spec = DfXSpecification(
                    category=category,
                    specifications=data['specifications'],
                    requirements=data['requirements'],
                    constraints=data['constraints'],
                    recommendations=data['recommendations']
                )
                analysis_results[category] = spec
                
        except json.JSONDecodeError as e:
            st.error(f"Error parsing GPT response: {e}")
            st.code(response_text, language='json')
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            
        return analysis_results

def main():
    st.set_page_config(page_title="DfX Analysis System", layout="wide")
    
    st.title("Design for X (DfX) Analysis System")
    st.write("Upload a design image for comprehensive DfX analysis.")
    
    api_key = st.text_input("Enter your OpenAI API key", type="password")
    
    if not api_key:
        st.warning("Please enter your OpenAI API key to proceed.")
        return
        
    uploaded_file = st.file_uploader("Upload design image", type=['png', 'jpg', 'jpeg'])
    
    dfx_options = {
        'manufacturability': 'Manufacturing process and production specifications',
        'reliability': 'Product reliability and durability specifications',
        'sustainability': 'Environmental and resource efficiency specifications',
        'usability': 'User interaction and accessibility specifications',
        'cost': 'Cost-related specifications and requirements',
        'safety': 'Safety standards and requirements',
        'performance': 'Performance specifications and benchmarks',
        'maintainability': 'Maintenance and serviceability specifications',
        'scalability': 'Growth and adaptation specifications',
        'compliance': 'Regulatory and standards compliance specifications'
    }
    
    selected_categories = st.multiselect(
        "Select DfX categories to analyze:",
        list(dfx_options.keys()),
        help="Select one or more categories"
    )
    
    if uploaded_file and selected_categories:
        with open("temp_image.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        analyzer = DfXAnalyzer(api_key)
        
        # Create tabs for different analyses
        tab1, tab2, tab3 = st.tabs(["Object Description", "Design Brainstorming", "DfX Specifications"])
        
        with tab1:
            with st.spinner("Analyzing object..."):
                object_desc = analyzer.generate_object_description("temp_image.jpg")
                
                if object_desc:
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.image(uploaded_file, caption="Design Image", use_column_width=True)
                    
                    with col2:
                        st.subheader("Object Description")
                        st.write("General Description")
                        st.write(object_desc.general_description)
                        
                        st.write("Components")
                        for comp in object_desc.components:
                            st.write(f"• {comp}")
                            
                        st.write("Dimensions")
                        for dim, value in object_desc.dimensions.items():
                            st.write(f"• {dim.title()}: {value}")
                            
                        st.write("Materials")
                        for material in object_desc.materials:
                            st.write(f"• {material}")
                            
                        st.write("Key Features")
                        for feature in object_desc.key_features:
                            st.write(f"• {feature}")
                            
                        st.write("Intended Use")
                        for use in object_desc.intended_use:
                            st.write(f"• {use}")
        
        with tab2:
            with st.spinner("Generating design alternatives..."):
                brainstorming = analyzer.generate_brainstorming("temp_image.jpg")
                
                if brainstorming:
                    st.subheader("Design Brainstorming Analysis")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        with st.expander("Component Alternatives", expanded=True):
                            for comp_alt in brainstorming.components_alternatives:
                                for comp_name, alternatives in comp_alt.items():
                                    st.write(f"{comp_name}")
                                    for alt in alternatives:
                                        st.write(f"• {alt}")
                                    st.write("")
                        
                        with st.expander("Material Options", expanded=True):
                            for mat_opt in brainstorming.material_options:
                                for area, materials in mat_opt.items():
                                    st.write(f"{area}")
                                    for material in materials:
                                        st.write(f"• {material}")
                                    st.write("")
                        
                        with st.expander("Ergonomic Considerations", expanded=True):
                            for ergo in brainstorming.ergonomic_considerations:
                                for point, considerations in ergo.items():
                                    st.write(f"{point}")
                                    for consideration in considerations:
                                        st.write(f"• {consideration}")
                                    st.write("")
                    
                    with col2:
                        with st.expander("Market Analysis", expanded=True):
                            st.write("Competitors")
                            for competitor in brainstorming.market_analysis['competitors']:
                                st.write(f"• {competitor}")
                            
                            st.write("\n*Market Gaps*")
                            for gap in brainstorming.market_analysis['market_gaps']:
                                st.write(f"• {gap}")
                            
                            st.write("\n*User Needs*")
                            for need in brainstorming.market_analysis['user_needs']:
                                st.write(f"• {need}")
                        
                        with st.expander("Hazard Analysis", expanded=True):
                            for hazard in brainstorming.hazard_analysis:
                                for category, hazards in hazard.items():
                                    st.write(f"{category}")
                                    for h in hazards:
                                        st.write(f"• {h}")
                                    st.write("")
                        
                        with st.expander("Innovation Opportunities", expanded=True):
                            for opportunity in brainstorming.innovation_opportunities:
                                st.write(f"• {opportunity}")
                        
                        with st.expander("Design Trade-offs", expanded=True):
                            for tradeoff in brainstorming.design_tradeoffs:
                                for category, options in tradeoff.items():
                                    st.write(f"{category}")
                                    for option in options:
                                        st.write(f"• {option}")
                                    st.write("")
        
        with tab3:
            with st.spinner("Generating specifications..."):
                specifications = analyzer.analyze_specifications("temp_image.jpg", selected_categories)
            
                if specifications:
                    st.subheader("DfX Specifications")
                    for category, spec in specifications.items():
                        with st.expander(f"{category.title()} Specifications", expanded=True):
                            st.subheader("Detailed Specifications")
                            for s in spec.specifications:
                                st.write(f"• {s}")
                            
                            st.subheader("Key Requirements")
                            for r in spec.requirements:
                                st.write(f"• {r}")
                            
                            st.subheader("Design Constraints")
                            for c in spec.constraints:
                                st.write(f"• {c}")
                            
                            st.subheader("Recommendations")
                            for r in spec.recommendations:
                                st.write(f"• {r}")
        
        # Add export functionality
        if st.sidebar.button("Export Complete Analysis"):
            export_data = {
                "object_description": {
                    "general_description": object_desc.general_description,
                    "components": object_desc.components,
                    "dimensions": object_desc.dimensions,
                    "materials": object_desc.materials,
                    "key_features": object_desc.key_features,
                    "intended_use": object_desc.intended_use
                },
                "brainstorming_analysis": {
                    "components_alternatives": brainstorming.components_alternatives,
                    "material_options": brainstorming.material_options,
                    "ergonomic_considerations": brainstorming.ergonomic_considerations,
                    "market_analysis": brainstorming.market_analysis,
                    "hazard_analysis": brainstorming.hazard_analysis,
                    "innovation_opportunities": brainstorming.innovation_opportunities,
                    "design_tradeoffs": brainstorming.design_tradeoffs
                },
                "specifications": {}
            }
            
            for category, spec in specifications.items():
                export_data["specifications"][category] = {
                    "specifications": spec.specifications,
                    "requirements": spec.requirements,
                    "constraints": spec.constraints,
                    "recommendations": spec.recommendations
                }
            
            st.sidebar.download_button(
                label="Download Complete Analysis",
                data=json.dumps(export_data, indent=2),
                file_name="dfx_complete_analysis.json",
                mime="application/json"
            )
        
        # Cleanup
        os.remove("temp_image.jpg")

if __name__ == "__main__":
    main()
