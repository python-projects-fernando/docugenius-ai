// src/constants/fieldTypes.ts

export const FIELD_TYPES = [
  { value: 'text', label: 'Text' },        // <-- Minúsculo
  { value: 'number', label: 'Number' },    // <-- Minúsculo
  { value: 'integer', label: 'Integer' },  // <-- Minúsculo
  { value: 'decimal', label: 'Decimal' },  // <-- Minúsculo
  { value: 'date', label: 'Date' },        // <-- Minúsculo
  { value: 'checkbox', label: 'Checkbox' }, // <-- Minúsculo
  { value: 'radio', label: 'Radio' },      // <-- Minúsculo
  { value: 'select', label: 'Select' },    // <-- Minúsculo
  { value: 'textarea', label: 'Textarea' }, // <-- Minúsculo
  { value: 'password', label: 'Password' }, // <-- Minúsculo
  { value: 'tel', label: 'Phone' },        // <-- Minúsculo
  { value: 'url', label: 'URL' },          // <-- Minúsculo
  { value: 'search', label: 'Search' },    // <-- Minúsculo
  { value: 'range', label: 'Range' },      // <-- Minúsculo
  { value: 'color', label: 'Color' },      // <-- Minúsculo
  { value: 'hidden', label: 'Hidden' },    // <-- Minúsculo
  { value: 'file', label: 'File' },        // <-- Minúsculo
] as const;

// Para tipagem forte, podemos criar um tipo a partir da constante
export type FieldType = typeof FIELD_TYPES[number]['value'];