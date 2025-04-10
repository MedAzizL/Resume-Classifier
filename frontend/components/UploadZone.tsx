'use client'

import React, { useState, useCallback } from 'react'
import { Upload } from 'lucide-react'

interface UploadZoneProps {
  onUpload: (file: File) => void
  loading: boolean
}

export default function UploadZone({ onUpload, loading }: UploadZoneProps) {
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onUpload(e.dataTransfer.files[0])
    }
  }, [onUpload])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault()
    if (e.target.files && e.target.files[0]) {
      onUpload(e.target.files[0])
    }
  }

  return (
    <div className="mb-8">
      <form
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        className="relative"
      >
        <input
          type="file"
          id="file-upload"
          className="hidden"
          accept=".pdf,.docx,.doc,.txt"
          onChange={handleChange}
          disabled={loading}
        />
        <label
          htmlFor="file-upload"
          className={`
            flex flex-col items-center justify-center
            w-full h-64 border-2 border-dashed rounded-lg
            cursor-pointer transition-all
            ${dragActive 
              ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' 
              : 'border-gray-300 dark:border-gray-700 hover:border-blue-400'
            }
            ${loading ? 'opacity-50 cursor-not-allowed' : ''}
          `}
        >
          <div className="flex flex-col items-center justify-center pt-5 pb-6">
            <Upload className={`w-12 h-12 mb-4 ${loading ? 'animate-bounce' : ''} text-gray-400`} />
            <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
              <span className="font-semibold">
                {loading ? 'Processing...' : 'Click to upload'}
              </span> or drag and drop
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              PDF, DOCX, or TXT (MAX. 16MB)
            </p>
          </div>
        </label>
      </form>
    </div>
  )
}

