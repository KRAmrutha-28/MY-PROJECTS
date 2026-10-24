from reports.pdf_generator import create_pdf

sample_report = """
# Research Report

## Executive Summary

Selenium is an open-source browser automation framework.

## Key Findings

- Supports Chrome
- Supports Firefox
- Supports Edge

## Conclusion

Selenium is widely used for web automation.
"""

create_pdf(
    sample_report,
    "sample_report.pdf"
)

print("PDF Created Successfully")