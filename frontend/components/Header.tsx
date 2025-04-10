import React from 'react'

export default function Header() {
  return (
    <header className="bg-white dark:bg-gray-900 shadow-sm">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg"></div>
          <h1 className="text-xl font-bold text-gray-900 dark:text-white">
            Resume Classifier
          </h1>
        </div>
      </div>
    </header>
  )
}
