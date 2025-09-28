import Link from 'next/link'

export default function Support() {
  const supportOptions = [
    {
      icon: 'fas fa-question-circle',
      title: 'Help Center',
      description: 'Browse our comprehensive help articles and FAQs',
      action: 'Visit Help Center',
      href: '#'
    },
    {
      icon: 'fas fa-envelope',
      title: 'Email Support',
      description: 'Send us an email and we\'ll get back to you within 24 hours',
      action: 'Send Email',
      href: 'mailto:support@servicepro.com'
    },
    {
      icon: 'fas fa-phone',
      title: 'Phone Support',
      description: 'Speak directly with our support team',
      action: 'Call Now',
      href: 'tel:+1234567890'
    },
    {
      icon: 'fas fa-comments',
      title: 'Live Chat',
      description: 'Get instant help through our live chat system',
      action: 'Start Chat',
      href: '#'
    }
  ]

  const faqs = [
    {
      question: 'How do I book a service?',
      answer: 'Simply browse our services, select a professional, choose your preferred time, and confirm your booking. You\'ll receive a confirmation email with all the details.'
    },
    {
      question: 'What if I need to cancel or reschedule?',
      answer: 'You can cancel or reschedule up to 2 hours before the appointment through your dashboard. Cancellations within 2 hours may incur a small fee.'
    },
    {
      question: 'Are all professionals background checked?',
      answer: 'Yes, every professional on our platform undergoes thorough background checks, license verification, and reference checks before they can offer services.'
    },
    {
      question: 'How do I pay for services?',
      answer: 'Payment is processed securely through our platform. You can pay with credit card, debit card, or digital wallets. Payment is held until the service is completed to your satisfaction.'
    },
    {
      question: 'What if I\'m not satisfied with the service?',
      answer: 'Your satisfaction is guaranteed. If you\'re not happy with the service, contact us within 24 hours and we\'ll work to make it right or provide a refund.'
    }
  ]

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Support Center
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-blue-100 max-w-3xl mx-auto">
              We're here to help you get the most out of Service PRO
            </p>
          </div>
        </div>
      </section>

      {/* Support Options */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Get Help
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Choose the support option that works best for you
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {supportOptions.map((option, index) => (
              <div key={index} className="bg-gray-50 rounded-xl p-6 hover:shadow-lg transition-shadow">
                <div className="w-12 h-12 bg-blue-100 rounded-lg mx-auto mb-4 flex items-center justify-center">
                  <i className={`${option.icon} text-blue-600 text-xl`}></i>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2 text-center">
                  {option.title}
                </h3>
                <p className="text-gray-600 text-center mb-4">
                  {option.description}
                </p>
                <div className="text-center">
                  <Link
                    href={option.href}
                    className="inline-flex items-center text-blue-600 font-medium hover:text-blue-700"
                  >
                    {option.action}
                    <i className="fas fa-arrow-right ml-2"></i>
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Frequently Asked Questions
            </h2>
            <p className="text-xl text-gray-600">
              Quick answers to common questions
            </p>
          </div>

          <div className="space-y-6">
            {faqs.map((faq, index) => (
              <div key={index} className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  {faq.question}
                </h3>
                <p className="text-gray-600">
                  {faq.answer}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section className="py-16 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Still Need Help?
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Our support team is here to assist you with any questions or concerns
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="mailto:support@servicepro.com"
              className="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors shadow-lg"
            >
              <i className="fas fa-envelope mr-2"></i>
              Email Support
            </a>
            <a
              href="tel:+1234567890"
              className="border-2 border-blue-600 text-blue-600 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-600 hover:text-white transition-colors"
            >
              <i className="fas fa-phone mr-2"></i>
              Call Support
            </a>
          </div>
        </div>
      </section>
    </div>
  )
}