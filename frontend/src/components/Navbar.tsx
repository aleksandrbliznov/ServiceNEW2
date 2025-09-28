'use client'

import { useState } from 'react'
import Link from 'next/link'

interface User {
  id: number
  first_name: string
  last_name: string
  email: string
  role: string
}

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false)
  const [user, setUser] = useState<User | null>(null) // This will be replaced with actual auth context

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            {/* Logo */}
            <div className="flex-shrink-0 flex items-center">
              <Link href="/" className="text-2xl font-bold text-blue-600 hover:text-blue-700 transition-colors">
                <i className="fas fa-tools mr-2"></i>
                Service PRO
              </Link>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:ml-8 md:flex md:space-x-4">
              <Link
                href="/"
                className="bg-gray-100 hover:bg-blue-100 text-gray-700 hover:text-blue-600 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 border border-gray-200 hover:border-blue-200 shadow-sm hover:shadow-md"
              >
                Home
              </Link>
              <Link
                href="/services"
                className="bg-gray-100 hover:bg-blue-100 text-gray-700 hover:text-blue-600 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 border border-gray-200 hover:border-blue-200 shadow-sm hover:shadow-md"
              >
                Services
              </Link>
              <Link
                href="/about"
                className="bg-gray-100 hover:bg-blue-100 text-gray-700 hover:text-blue-600 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 border border-gray-200 hover:border-blue-200 shadow-sm hover:shadow-md"
              >
                About
              </Link>
            </div>
          </div>

          {/* Desktop Auth Buttons */}
          <div className="hidden md:ml-4 md:flex md:items-center md:space-x-4">
            {!user ? (
              <>
                <Link
                  href="/register"
                  className="bg-gray-100 text-gray-700 hover:bg-gray-200 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                >
                  Sign Up
                </Link>
                <Link
                  href="/login"
                  className="bg-blue-600 text-white hover:bg-blue-700 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                >
                  Sign In
                </Link>
              </>
            ) : (
              <div className="relative">
                <button className="flex items-center space-x-2 text-gray-700 hover:text-blue-600">
                  <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                    {user.first_name?.[0]}{user.last_name?.[0]}
                  </div>
                  <span className="text-sm font-medium">{user.first_name}</span>
                  <i className="fas fa-chevron-down text-xs"></i>
                </button>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-700 hover:text-blue-600 focus:outline-none focus:text-blue-600"
            >
              <i className={`fas ${isOpen ? 'fa-times' : 'fa-bars'} text-xl`}></i>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-2 sm:px-3 bg-white border-t">
            <Link
              href="/"
              className="bg-gray-100 hover:bg-blue-100 text-gray-700 hover:text-blue-600 block px-4 py-3 mx-2 rounded-lg text-base font-medium transition-all duration-200 border border-gray-200 hover:border-blue-200 shadow-sm"
              onClick={() => setIsOpen(false)}
            >
              Home
            </Link>
            <Link
              href="/services"
              className="bg-gray-100 hover:bg-blue-100 text-gray-700 hover:text-blue-600 block px-4 py-3 mx-2 rounded-lg text-base font-medium transition-all duration-200 border border-gray-200 hover:border-blue-200 shadow-sm"
              onClick={() => setIsOpen(false)}
            >
              Services
            </Link>
            <Link
              href="/about"
              className="bg-gray-100 hover:bg-blue-100 text-gray-700 hover:text-blue-600 block px-4 py-3 mx-2 rounded-lg text-base font-medium transition-all duration-200 border border-gray-200 hover:border-blue-200 shadow-sm"
              onClick={() => setIsOpen(false)}
            >
              About
            </Link>

            {!user ? (
              <div className="pt-4 pb-2 border-t border-gray-200">
                <Link
                  href="/register"
                  className="block w-full text-center bg-gray-100 text-gray-700 hover:bg-gray-200 px-4 py-2 rounded-lg text-base font-medium mb-2"
                  onClick={() => setIsOpen(false)}
                >
                  Sign Up
                </Link>
                <Link
                  href="/login"
                  className="block w-full text-center bg-blue-600 text-white hover:bg-blue-700 px-4 py-2 rounded-lg text-base font-medium"
                  onClick={() => setIsOpen(false)}
                >
                  Sign In
                </Link>
              </div>
            ) : (
              <div className="pt-4 pb-2 border-t border-gray-200">
                <div className="flex items-center px-3 py-2">
                  <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white text-lg font-medium mr-3">
                    {user.first_name?.[0]}{user.last_name?.[0]}
                  </div>
                  <div>
                    <div className="text-base font-medium text-gray-800">{user.first_name} {user.last_name}</div>
                    <div className="text-sm text-gray-500">{user.email}</div>
                  </div>
                </div>
                <Link
                  href="/dashboard"
                  className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-blue-600"
                  onClick={() => setIsOpen(false)}
                >
                  Dashboard
                </Link>
                <button className="block w-full text-left px-3 py-2 text-base font-medium text-gray-700 hover:text-blue-600">
                  Sign Out
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  )
}