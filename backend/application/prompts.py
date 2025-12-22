business_description_input = "Law firm specialized in labor law."

GENERATE_DOCUMENT_TYPES_PROMPT = """
You are an expert in business processes and document management. Based on the description of a business or sector, suggest a list of common and essential document types used within that field.

Business Description: {business_description_input}

Respond ONLY with a structured JSON object in the following format. Do not include any introductory text, explanations, or concluding remarks before or after the JSON block.

{{
  "suggested_document_types": [
    {{
      "name": "Document Type Name", // e.g., "Service Contract", "Commercial Proposal", "Employment Agreement". Use clear, business-appropriate terminology.
      "description": "A brief description of the document type and its purpose within the business context." // e.g., "Template for standard service agreements between the company and its clients."
    }}    
  ]
}}

Ensure the suggestions are relevant, specific to the business type described, and cover core operational or administrative needs.
"""

#------------------------------------------------------------------------------------------------------------------------------

document_type_name = "Service Contract"
document_type_description = "Standard template for service contracts between parties for service provision."

GENERATE_DOCUMENT_FIELDS_PROMPT = """
You are an expert in document structure and business processes.
Given a document type, identify and list the essential fields required to define that document.
These fields will be used to dynamically generate an HTML form for users to fill out.

The document type is: {document_type_name}
Description: {document_type_description}

IMPORTANT: Respond ONLY with the structured JSON data, nothing else. Do not add any introductory text, explanations, or concluding remarks before or after the JSON block. Only return the JSON object itself.

{{
  "document_type": "{document_type_name}",
  "description": "{document_type_description}",
  "fields": [
    {{
      "name": "field_identifier", // e.g., "Contracting Company", "Service Value", "Start Date". Use readable format with spaces and capitalization suitable for labels.
      "type": "html_input_type", // Use ONE OF THE FOLLOWING EXACT VALUES: "text", "email", "integer", "decimal", "date", "checkbox", "textarea", "select", "radio", "password", "tel", "url", "search", "range", "color", "hidden", "file".
                                  // Use "textarea" for fields that will hold longer, multi-line text (e.g., descriptions, notes, terms, addresses with multiple lines).
                                  // Use "text" for shorter, single-line text (e.g., names, codes, simple identifiers).
                                  // For numbers: use "integer" for whole numbers (e.g., number of employees) and "decimal" for numbers with fractional parts (e.g., monetary values, percentages).
                                  // These special "integer" and "decimal" types will be mapped to HTML <input type="number"> with appropriate "step" attributes in the frontend.
      "required": true/false, // Boolean, true if mandatory, false if optional
      "description": "Short explanation of the field's purpose. If this description implies a long or multi-line text input, use 'textarea' for the type."
    }}    
  ]
}}

For numeric fields, use "integer" for whole numbers and "decimal" for numbers with fractional parts, instead of the generic "number" type. The frontend will map "integer" to <input type="number" step="1"> and "decimal" to <input type="number" step="0.01"> (or similar precision).
For fields that are expected to contain longer, multi-line text (like detailed descriptions, notes, terms, comments), ALWAYS use "type": "textarea". Consider the field's "description" to determine if it's likely to hold substantial text. Use "type": "text" only for short, single-line inputs.
"""

#------------------------------------------------------------------------------------------------------------------------------
document_type_name = "Service Contract"
document_type_description = "Standard template for service contracts between parties for service provision."

filled_fields_json = '''
{
  "contracting_company": "TechSolutions Inc.",
  "service_provider": "AnotherParty Corp.",
  "service_description": "CRM Development",
  "contract_value": "$15,000",
  "execution_period": "6 months",
  "notice_period_days": 30,
  "penalty_percentage": 20
}
'''

GENERATE_DOCUMENT_CONTENT_PROMPT = """
You are an expert in drafting professional documents.
Generate the complete content for a document of type '{document_type_name}' described as: '{document_type_description}'.
Use the following field values provided by the user to populate the document:

{filled_fields_json}

Structure the document appropriately (e.g., title, sections, clauses, signature blocks), incorporating the provided data accurately and professionally.
Ensure the generated text is coherent, follows a logical flow, and adheres to standard conventions for this type of document.
If certain information is missing or marked as optional but impacts the structure, generate placeholder text or a standard clause indicating its absence (e.g., "[Optional clause not provided]" or "Standard terms apply unless otherwise specified").
Focus on clarity, correctness, and relevance to the field values given.
"""
