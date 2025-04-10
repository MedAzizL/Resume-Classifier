'use client'

import React from 'react'
import { ClassificationResult } from '@/types'
import { Briefcase, Mail, Phone, Link, Code, GraduationCap, Calendar } from 'lucide-react'

interface ResultsDisplayProps {
  results: ClassificationResult
}

export default function ResultsDisplay({ results }: ResultsDisplayProps) {
  const { classification, parsed_data } = results

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Classification Results */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">
          Classification Results
        </h2>
        
        <div className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-lg font-semibold text-gray-700 dark:text-gray-300">
              Primary Category:
            </span>
            <span className="text-2xl font-bold text-blue-600 dark:text-blue-400">
              {classification.category}
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-4">
            <div
              className="bg-gradient-to-r from-blue-500 to-purple-600 h-4 rounded-full transition-all"
              style={{ width: `${classification.confidence * 100}%` }}
            ></div>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Confidence: {(classification.confidence * 100).toFixed(1)}%
          </p>
        </div>

        {/* Top Predictions */}
        <div className="mt-6">
          <h3 className="text-lg font-semibold mb-3 text-gray-900 dark:text-white">
            Top Predictions:
          </h3>
          <div className="space-y-2">
            {classification.top_predictions.map((pred, idx) => (
              <div key={idx} className="flex items-center justify-between">
                <span className="text-gray-700 dark:text-gray-300">
                  {idx + 1}. {pred.category}
                </span>
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  {(pred.confidence * 100).toFixed(1)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Parsed Data */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">
          Extracted Information
        </h2>

        <div className="grid md:grid-cols-2 gap-4">
          {/* Contact Info */}
          {parsed_data.email && (
            <div className="flex items-start space-x-3">
              <Mail className="w-5 h-5 text-blue-500 mt-1" />
              <div>
                <p className="font-semibold text-gray-700 dark:text-gray-300">Email</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">{parsed_data.email}</p>
              </div>
            </div>
          )}

          {parsed_data.phone && (
            <div className="flex items-start space-x-3">
              <Phone className="w-5 h-5 text-green-500 mt-1" />
              <div>
                <p className="font-semibold text-gray-700 dark:text-gray-300">Phone</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">{parsed_data.phone}</p>
              </div>
            </div>
          )}

          {parsed_data.experience_years > 0 && (
            <div className="flex items-start space-x-3">
              <Calendar className="w-5 h-5 text-purple-500 mt-1" />
              <div>
                <p className="font-semibold text-gray-700 dark:text-gray-300">Experience</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {parsed_data.experience_years} years
                </p>
              </div>
            </div>
          )}

          {/* URLs */}
          {parsed_data.urls && parsed_data.urls.length > 0 && (
            <div className="flex items-start space-x-3">
              <Link className="w-5 h-5 text-orange-500 mt-1" />
              <div className="flex-1">
                <p className="font-semibold text-gray-700 dark:text-gray-300">Links</p>
                <div className="space-y-1">
                  {parsed_data.urls.slice(0, 3).map((url, idx) => (
                    <a
                      key={idx}
                      href={url.startsWith('http') ? url : `https://${url}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-blue-600 dark:text-blue-400 hover:underline block truncate"
                    >
                      {url}
                    </a>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Skills */}
        {parsed_data.skills && parsed_data.skills.length > 0 && (
          <div className="mt-6">
            <div className="flex items-center space-x-2 mb-3">
              <Code className="w-5 h-5 text-indigo-500" />
              <h3 className="font-semibold text-gray-700 dark:text-gray-300">Skills</h3>
            </div>
            <div className="flex flex-wrap gap-2">
              {parsed_data.skills.map((skill, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-sm"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Education */}
        {parsed_data.education && parsed_data.education.length > 0 && (
          <div className="mt-6">
            <div className="flex items-center space-x-2 mb-3">
              <GraduationCap className="w-5 h-5 text-red-500" />
              <h3 className="font-semibold text-gray-700 dark:text-gray-300">Education</h3>
            </div>
            <ul className="space-y-2">
              {parsed_data.education.map((edu, idx) => (
                <li key={idx} className="text-sm text-gray-600 dark:text-gray-400">
                  {edu}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

