import Link from 'next/link'

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="col-span-1 md:col-span-1">
            <div className="flex items-center mb-4">
              <i className="fas fa-tools text-blue-400 text-2xl mr-3"></i>
              <h3 className="text-xl font-bold">Service PRO</h3>
            </div>
            <p className="text-gray-300 text-sm mb-4">
              Your trusted platform connecting clients with professional service providers.
              Quality service at your fingertips.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-300 hover:text-blue-400 transition-colors">
                <i className="fab fa-facebook text-xl"></i>
              </a>
              <a href="#" className="text-gray-300 hover:text-blue-400 transition-colors">
                <i className="fab fa-twitter text-xl"></i>
              </a>
              <a href="#" className="text-gray-300 hover:text-blue-400 transition-colors">
                <i className="fab fa-linkedin text-xl"></i>
              </a>
              <a href="#" className="text-gray-300 hover:text-blue-400 transition-colors">
                <i className="fab fa-instagram text-xl"></i>
              </a>
            </div>
          </div>

          {/* Services */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Services</h4>
            <ul className="space-y-2">
              <li>
                <Link href="/services?category=plumbing" className="text-gray-300 hover:text-blue-400 text-sm transition-colors">
                  Plumbing
                </Link>
              </li>
              <li>
                <Link href="/services?category=electrical" className="text-gray-300 hover:text-blue-400 text-sm transition-colors">
                  Electrical
                </Link>
              </li>
              <li>
                <Link href="/services?category=cleaning" className="text-gray-300 hover:text-blue-400 text-sm transition-colors">
                  Cleaning
                </Link>
              </li>
              <li>
                <Link href="/services?category=construction" className="text-gray-300 hover:text-blue-400 text-sm transition-colors">
                  Construction
                </Link>
              </li>
              <li>
                <Link href="/services?category=gardening" className="text-gray-300 hover:text-blue-400 text-sm transition-colors">
                  Gardening
                </Link>
              </li>
            </ul>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2">
              <li>
                <Link href="/" className="text-gray-300 hover:text-blue-400 text-sm transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link href="/services" className="text-gray-300 hover:text-blue-400 text-sm transition-colors">
                  All Services
                </Link>
              </li>
              <li>
                <Link href="/register" className="text-gray-300 hover:text-blue-400 text-sm transition-colors">
                  Become a Provider
                </Link>
              </li>
              <li>
                <Link href="/about" className="text-gray-300 hover:text-blue-400 text-sm transition-colors">
                  About Us
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-gray-300 hover:text-blue-400 text-sm transition-colors">
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Contact Info</h4>
            <div className="space-y-3">
              <div className="flex items-start space-x-3">
                <i className="fas fa-map-marker-alt text-blue-400 mt-1"></i>
                <div className="text-gray-300 text-sm">
                  123 Service Street<br />
                  City, State 12345
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <i className="fas fa-phone text-blue-400"></i>
                <span className="text-gray-300 text-sm">+1 (555) 123-4567</span>
              </div>
              <div className="flex items-center space-x-3">
                <i className="fas fa-envelope text-blue-400"></i>
                <span className="text-gray-300 text-sm">info@servicepro.com</span>
              </div>
              <div className="flex items-center space-x-3">
                <i className="fas fa-clock text-blue-400"></i>
                <span className="text-gray-300 text-sm">24/7 Available</span>
              </div>
            </div>
          </div>
        </div>

        <hr className="my-8 border-gray-700" />

        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="text-gray-300 text-sm mb-4 md:mb-0">
            © 2025 Service PRO. All rights reserved. | Made with <i className="fas fa-heart text-red-500 mx-1"></i> for better service
          </div>
          <div className="flex space-x-6">
            <Link href="/privacy" className="text-gray-300 hover:text-blue-400 text-sm transition-colors">
              Privacy Policy
            </Link>
            <Link href="/terms" className="text-gray-300 hover:text-blue-400 text-sm transition-colors">
              Terms of Service
            </Link>
            <Link href="/support" className="text-gray-300 hover:text-blue-400 text-sm transition-colors">
              Support
            </Link>
          </div>
        </div>
      </div>
    </footer>
  )
}