# DfX Analysis System

## Overview

The DfX (Design for X) Analysis System is a comprehensive tool for analyzing design images to extract valuable insights across various aspects of product design and development. This application leverages AI-powered analysis to provide object descriptions, design brainstorming, and detailed specifications for selected DfX categories.

---

## Features

### 1. Object Description
Generates a comprehensive description of the uploaded design image, including:
- General overview
- List of components
- Dimensions (length, width, height, etc.)
- Materials and their properties
- Key features
- Intended use cases

### 2. Design Brainstorming
Provides alternative design approaches and analysis, including:
- Component alternatives with pros and cons
- Material options and justifications
- Ergonomic considerations
- Market analysis, including competitors, gaps, and user needs
- Hazard analysis and mitigations
- Innovation opportunities
- Design trade-offs with impact analysis

### 3. DfX Specifications
Generates detailed specifications for selected DfX categories, including:
- *Specifications*: Technical details and benchmarks
- *Requirements*: Essential criteria
- *Constraints*: Limitations or boundaries
- *Recommendations*: Suggestions for improvement

### 4. Export Functionality
Enables users to export the complete analysis as a JSON file for documentation and further use.

---

## Requirements

### Software
- Python 3.8+
- Streamlit
- OpenAI Python SDK
- Pillow
- NumPy

### Hardware
Compatible with systems that support Python and Streamlit.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/Design_For_X.git
   cd dfx-analysis-system