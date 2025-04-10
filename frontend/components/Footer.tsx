import React from 'react'

export default function Footer() {
  return (
    <footer className="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800">
      <div className="container mx-auto px-4 py-6">
        <div className="text-center text-gray-600 dark:text-gray-400">
          <p>&copy; 2025 Resume Classifier. Built with AI & Love.</p>
          <p className="mt-2 text-sm">
            Powered by Hugging Face, Flask, Next.js & Azure
          </p>
        </div>
      </div>
    </footer>
  )
}
