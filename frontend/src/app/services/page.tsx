'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import SearchFilters from '@/components/SearchFilters'

interface Service {
  id: number
  name: string
  description: string
  price: number
  duration_hours: number
  category: string
  service_group_id: number
  handyman_id: number
  is_active: boolean
  is_approved: boolean
  example_images: string[]
  created_at: string
  service_group: {
    id: number
    name: string
  }
  handyman: {
    id: number
    first_name: string
    last_name: string
    average_score: number
  }
}

interface FilterState {
  search: string
  category: string
  location: string
  priceRange: [number, number]
  rating: number
  availability: string
  sortBy: string
}

export default function ServicesPage() {
  const [services, setServices] = useState<Service[]>([])
  const [filteredServices, setFilteredServices] = useState<Service[]>([])
  const [loading, setLoading] = useState(true)
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [compareMode, setCompareMode] = useState(false)
  const [compareList, setCompareList] = useState<number[]>([])

  useEffect(() => {
    fetchServices()
  }, [])

  const fetchServices = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/services', {
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      if (data.success) {
        setServices(data.data)
        setFilteredServices(data.data)
      } else {
        console.error('API returned success=false:', data)
        setServices([])
        setFilteredServices([])
      }
    } catch (error) {
      console.error('Error fetching services:', error)
      setServices([])
      setFilteredServices([])
    } finally {
      setLoading(false)
    }
  }

  const handleFiltersChange = (filters: FilterState) => {
    let filtered = services

    // Apply search filter
    if (filters.search) {
      filtered = filtered.filter(service =>
        service.name.toLowerCase().includes(filters.search.toLowerCase()) ||
        service.description.toLowerCase().includes(filters.search.toLowerCase())
      )
    }

    // Apply category filter
    if (filters.category !== 'all') {
      filtered = filtered.filter(service => service.category.toLowerCase() === filters.category.toLowerCase())
    }

    // Apply price range filter
    filtered = filtered.filter(service =>
      service.price >= filters.priceRange[0] && service.price <= filters.priceRange[1]
    )

    // Apply rating filter
    if (filters.rating > 0) {
      filtered = filtered.filter(service => service.handyman.average_score >= filters.rating)
    }

    // Apply sorting
    switch (filters.sortBy) {
      case 'rating':
        filtered.sort((a, b) => b.handyman.average_score - a.handyman.average_score)
        break
      case 'price_low':
        filtered.sort((a, b) => a.price - b.price)
        break
      case 'price_high':
        filtered.sort((a, b) => b.price - a.price)
        break
      case 'relevance':
      default:
        // Keep original order for relevance
        break
    }

    setFilteredServices(filtered)
  }

  const toggleCompare = (serviceId: number) => {
    if (compareList.includes(serviceId)) {
      setCompareList(compareList.filter(id => id !== serviceId))
    } else if (compareList.length < 3) {
      setCompareList([...compareList, serviceId])
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Our Services
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Browse our comprehensive range of professional services from trusted providers
          </p>
        </div>

        {/* Advanced Search Filters */}
        <SearchFilters onFiltersChange={handleFiltersChange} />

        {/* View Controls */}
        <div className="flex justify-between items-center mb-6">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded-lg transition-colors ${
                viewMode === 'grid'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              <i className="fas fa-th"></i>
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 rounded-lg transition-colors ${
                viewMode === 'list'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              <i className="fas fa-list"></i>
            </button>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setCompareMode(!compareMode)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                compareMode
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <i className="fas fa-balance-scale mr-2"></i>
              Compare ({compareList.length}/3)
            </button>
          </div>
        </div>

        {/* Services Grid */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="bg-white rounded-xl shadow-lg overflow-hidden animate-pulse">
                <div className="h-48 bg-gray-200"></div>
                <div className="p-6">
                  <div className="h-6 bg-gray-200 rounded mb-2"></div>
                  <div className="h-4 bg-gray-200 rounded mb-4"></div>
                  <div className="h-6 bg-gray-200 rounded w-1/3"></div>
                </div>
              </div>
            ))}
          </div>
        ) : filteredServices.length === 0 ? (
          <div className="text-center py-12">
            <i className="fas fa-search text-6xl text-gray-300 mb-4"></i>
            <h3 className="text-xl font-medium text-gray-900 mb-2">No services found</h3>
            <p className="text-gray-600">
              No services match your current search criteria. Try adjusting your filters.
            </p>
          </div>
        ) : (
          <div className={
            viewMode === 'grid'
              ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8'
              : 'space-y-6'
          }>
            {filteredServices.map((service) => (
              <div
                key={service.id}
                className={`bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow ${
                  viewMode === 'list' ? 'flex' : ''
                }`}
              >
                {/* Service Image */}
                <div className={`bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center ${
                  viewMode === 'grid' ? 'h-48' : 'h-32 w-32 flex-shrink-0'
                }`}>
                  {service.example_images && service.example_images.length > 0 ? (
                    <img
                      src={service.example_images[0]}
                      alt={service.name}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <i className="fas fa-tools text-white text-4xl"></i>
                  )}
                </div>

                {/* Service Info */}
                <div className={`${viewMode === 'grid' ? 'p-6' : 'p-4 flex-1'}`}>
                  <div className={`flex items-start justify-between mb-2 ${viewMode === 'list' ? 'flex-col space-y-2' : ''}`}>
                    <div className="flex-1">
                      <h3 className="text-xl font-semibold text-gray-900">
                        {service.name}
                      </h3>
                      {viewMode === 'list' && (
                        <p className="text-gray-600 text-sm mt-1">
                          {service.description}
                        </p>
                      )}
                    </div>
                    <span className="text-2xl font-bold text-green-600">
                      ${service.price}
                    </span>
                  </div>

                  {viewMode === 'grid' && (
                    <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                      {service.description}
                    </p>
                  )}

                  <div className={`flex items-center justify-between mb-4 ${viewMode === 'list' ? 'flex-wrap gap-2' : ''}`}>
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      <i className="fas fa-clock mr-1"></i>
                      {service.duration_hours}h
                    </span>
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                      {service.category}
                    </span>
                  </div>

                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center">
                      <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-medium mr-3">
                        {service.handyman.first_name[0]}{service.handyman.last_name[0]}
                      </div>
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {service.handyman.first_name} {service.handyman.last_name}
                        </div>
                        <div className="flex items-center">
                          <i className="fas fa-star text-yellow-400 text-xs mr-1"></i>
                          <span className="text-xs text-gray-600">
                            {service.handyman.average_score.toFixed(1)} rating
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <Link
                      href={`/services/${service.id}`}
                      className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-lg text-center font-medium hover:bg-blue-700 transition-colors"
                    >
                      View Details
                    </Link>
                    {compareMode && (
                      <button
                        onClick={() => toggleCompare(service.id)}
                        className={`px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                          compareList.includes(service.id)
                            ? 'bg-green-600 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                        }`}
                      >
                        <i className="fas fa-balance-scale"></i>
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}