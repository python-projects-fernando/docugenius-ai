export const FIELD_TYPES = [
  { value: 'text', label: 'Text' },
  { value: 'number', label: 'Number' },
  { value: 'integer', label: 'Integer' },
  { value: 'decimal', label: 'Decimal' },
  { value: 'date', label: 'Date' },
  { value: 'checkbox', label: 'Checkbox' },
  { value: 'radio', label: 'Radio' },
  { value: 'select', label: 'Select' },
  { value: 'textarea', label: 'Textarea' },
  { value: 'password', label: 'Password' },
  { value: 'tel', label: 'Phone' },
  { value: 'url', label: 'URL' },
  { value: 'search', label: 'Search' },
  { value: 'range', label: 'Range' },
  { value: 'color', label: 'Color' },
  { value: 'hidden', label: 'Hidden' },
  { value: 'file', label: 'File' },
] as const;

export type FieldType = typeof FIELD_TYPES[number]['value'];