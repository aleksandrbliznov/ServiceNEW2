export default function Terms() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Terms of Service
            </h1>
            <p className="text-xl md:text-2xl text-blue-100 max-w-3xl mx-auto">
              Please read these terms carefully before using Service PRO
            </p>
          </div>
        </div>
      </section>

      {/* Content */}
      <section className="py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-lg shadow-lg p-8">
            <div className="prose max-w-none">
              <p className="text-lg text-gray-600 mb-8">
                Last updated: {new Date().toLocaleDateString()}
              </p>

              <h2 className="text-2xl font-bold text-gray-900 mb-4">1. Acceptance of Terms</h2>
              <p className="text-gray-600 mb-6">
                By accessing and using Service PRO, you accept and agree to be bound by the terms and provision of this agreement.
                If you do not agree to abide by the above, please do not use this service.
              </p>

              <h2 className="text-2xl font-bold text-gray-900 mb-4">2. Use License</h2>
              <p className="text-gray-600 mb-6">
                Permission is granted to temporarily download one copy of Service PRO for personal, non-commercial transitory
                viewing only. This is the grant of a license, not a transfer of title, and under this license you may not:
              </p>
              <ul className="list-disc pl-6 text-gray-600 mb-6">
                <li>modify or copy the materials</li>
                <li>use the materials for any commercial purpose or for any public display</li>
                <li>attempt to reverse engineer any software contained on Service PRO</li>
                <li>remove any copyright or other proprietary notations from the materials</li>
              </ul>

              <h2 className="text-2xl font-bold text-gray-900 mb-4">3. Service Provider Responsibilities</h2>
              <p className="text-gray-600 mb-6">
                Service providers agree to provide accurate information about their services, maintain proper licensing and insurance,
                and deliver services in a professional manner. All work must meet industry standards and local regulations.
              </p>

              <h2 className="text-2xl font-bold text-gray-900 mb-4">4. Customer Responsibilities</h2>
              <p className="text-gray-600 mb-6">
                Customers agree to provide accurate information about their service needs, be present during service delivery when required,
                and make payment promptly upon completion of satisfactory work.
              </p>

              <h2 className="text-2xl font-bold text-gray-900 mb-4">5. Payment Terms</h2>
              <p className="text-gray-600 mb-6">
                Payment is due upon completion of services unless otherwise agreed. We accept major credit cards and digital payment methods.
                Service fees are clearly stated before booking confirmation.
              </p>

              <h2 className="text-2xl font-bold text-gray-900 mb-4">6. Cancellation Policy</h2>
              <p className="text-gray-600 mb-6">
                Services may be cancelled up to 2 hours before the scheduled time without penalty. Cancellations within 2 hours may incur
                a cancellation fee. Emergency cancellations due to unforeseen circumstances will be handled on a case-by-case basis.
              </p>

              <h2 className="text-2xl font-bold text-gray-900 mb-4">7. Limitation of Liability</h2>
              <p className="text-gray-600 mb-6">
                Service PRO acts as a platform connecting customers with service providers. We are not liable for any damages, losses,
                or injuries arising from services provided through our platform. Users engage with service providers at their own risk.
              </p>

              <h2 className="text-2xl font-bold text-gray-900 mb-4">8. User Conduct</h2>
              <p className="text-gray-600 mb-6">
                Users agree not to use the platform for any unlawful purposes or to conduct any unlawful activity, including but not limited
                to fraud, embezzlement, money laundering, or insider trading.
              </p>

              <h2 className="text-2xl font-bold text-gray-900 mb-4">9. Privacy Policy</h2>
              <p className="text-gray-600 mb-6">
                Your privacy is important to us. Please review our Privacy Policy, which also governs your use of Service PRO,
                to understand our practices.
              </p>

              <h2 className="text-2xl font-bold text-gray-900 mb-4">10. Termination</h2>
              <p className="text-gray-600 mb-6">
                We may terminate or suspend your account and bar access to the service immediately, without prior notice or liability,
                under our sole discretion, for any reason whatsoever and without limitation, including but not limited to a breach of the Terms.
              </p>

              <h2 className="text-2xl font-bold text-gray-900 mb-4">11. Changes to Terms</h2>
              <p className="text-gray-600 mb-6">
                We reserve the right to modify or replace these Terms at any time. If a revision is material, we will try to provide
                at least 30 days notice prior to any new terms taking effect.
              </p>

              <h2 className="text-2xl font-bold text-gray-900 mb-4">12. Contact Information</h2>
              <p className="text-gray-600 mb-6">
                If you have any questions about these Terms of Service, please contact us at{' '}
                <a href="mailto:legal@servicepro.com" className="text-blue-600 hover:text-blue-700">
                  legal@servicepro.com
                </a>
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}