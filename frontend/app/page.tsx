'use client'

import { useState } from 'react'
import UploadZone from '@/components/UploadZone'
import ResultsDisplay from '@/components/ResultsDisplay'
import { ClassificationResult } from '@/types'

export default function Home() {
  const [results, setResults] = useState<ClassificationResult | null>(null)
  const [loading, setLoading] = useState(false)

  const handleUpload = async (file: File) => {
    setLoading(true)
    setResults(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/classify`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Classification failed')
      }

      const data = await response.json()
      setResults(data)
    } catch (error) {
      console.error('Error:', error)
      alert('Failed to classify resume. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            AI Resume Classifier
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            Upload your resume and let AI analyze and classify it instantly
          </p>
        </div>

        <UploadZone onUpload={handleUpload} loading={loading} />
        {results && <ResultsDisplay results={results} />}
      </div>
    </div>
  )
}
