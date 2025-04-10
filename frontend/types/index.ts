export interface Classification {
  category: string
  confidence: number
  top_predictions: {
    category: string
    confidence: number
  }[]
  model_type: string
}

export interface ParsedData {
  email: string | null
  phone: string | null
  urls: string[]
  skills: string[]
  education: string[]
  experience_years: number
}

export interface ClassificationResult {
  classification: Classification
  parsed_data: ParsedData
  text_preview: string
}

