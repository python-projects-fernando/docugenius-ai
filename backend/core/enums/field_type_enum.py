from enum import Enum

class FieldType(Enum):
    TEXT = "text"
    EMAIL = "email"
    NUMBER = "number"
    INTEGER = "integer"
    DECIMAL = "decimal"
    DATE = "date"
    CHECKBOX = "checkbox"
    TEXTAREA = "textarea"
    SELECT = "select"
    RADIO = "radio"
    PASSWORD = "password"
    TEL = "tel"
    URL = "url"
    SEARCH = "search"
    RANGE = "range"
    COLOR = "color"
    HIDDEN = "hidden"
    FILE = "file"

    def description(self) -> str:
        descriptions = {
            FieldType.TEXT: "Single-line text input.",
            FieldType.EMAIL: "Email address input.",
            FieldType.NUMBER: "Generic number input (integer or decimal).",
            FieldType.INTEGER: "Whole number input.",
            FieldType.DECIMAL: "Decimal number input.",
            FieldType.DATE: "Date picker input.",
            FieldType.CHECKBOX: "Checkbox for boolean selection.",
            FieldType.TEXTAREA: "Multi-line text input.",
            FieldType.SELECT: "Dropdown selection.",
            FieldType.RADIO: "Radio button group.",
            FieldType.PASSWORD: "Password input (masked).",
            FieldType.TEL: "Telephone number input.",
            FieldType.URL: "URL input.",
            FieldType.SEARCH: "Search input.",
            FieldType.RANGE: "Slider input.",
            FieldType.COLOR: "Color picker input.",
            FieldType.HIDDEN: "Hidden input field.",
            FieldType.FILE: "File upload input.",
        }
        return descriptions.get(self, f"Description for {self.name} not defined.")