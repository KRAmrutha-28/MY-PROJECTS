import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Load Gemini Model
model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_report(query, context):

    prompt = f"""
You are a Senior Research Analyst,
Technical Writer,
and AI Research Assistant.

Your task is to generate a professional
research report using ONLY the
information available in the provided context.

USER QUERY:
{query}

RETRIEVED CONTEXT:
{context}

Instructions:

1. Analyze all retrieved information carefully.
2. If the query asks for comparison,
   generate a comparison report.
3. If the query asks for explanation,
   generate an explanatory report.
4. Use professional and technical language.
5. Do NOT invent facts not present
   in the context.
6. Use bullet points where appropriate.
7. Highlight important findings.
8. Mention strengths and weaknesses.
9. Mention suitable use cases.
10. Provide a clear conclusion.

Generate the report using the following structure:

# Executive Summary

Provide a concise overview.

# Introduction

Explain the topic and importance.

# Key Findings

Summarize important observations.

# Feature Comparison

Compare technologies if applicable.

# Detailed Analysis

Provide technical analysis.

# Advantages

List strengths and benefits.

# Disadvantages

List drawbacks and challenges.

# Best Use Cases

Describe suitable use cases.

# Limitations

Mention restrictions and assumptions.

# Conclusion

Summarize findings.

# References

List evidence used from retrieved context.
"""

    try:

        print(
            "Generating report using Gemini..."
        )

        response = model.generate_content(
            prompt
        )

        print(
            "Gemini report generated successfully."
        )

        return response.text

    except Exception as e:

        print(
            "=================================="
        )
        print(
            "Gemini API Error:"
        )
        print(
            str(e)
        )
        print(
            "Switching to fallback mode..."
        )
        print(
            "=================================="
        )

        fallback_report = f"""
# AI Service Unavailable

The Gemini API is currently unavailable.

The system has automatically switched
to fallback mode.

No application failure occurred.

## User Query

{query}

## Retrieved Context

{context}

## Fallback Analysis

The AI model could not be reached.

To ensure uninterrupted operation,
the system is displaying the retrieved
evidence directly from the knowledge base.

The retrieved content remains available
for review and analysis.

## Status

Fallback Mode Activated Successfully

## Recommendation

Retry report generation after the
Gemini service becomes available.
"""

        return fallback_report