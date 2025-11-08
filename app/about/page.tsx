import Image from "next/image"
import { Header } from "@/components/header"

export default function AboutPage() {
  return (
    <>
      <Header />
      <main className="min-h-screen bg-[#F5F1ED] py-12 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-3xl shadow-sm p-8 md:p-12">
            <h1 className="text-4xl md:text-5xl font-serif text-center text-[#5C4A42] mb-8">About The Fitting Room</h1>

            <div className="space-y-6 text-[#6B5A52] leading-relaxed">
              <p className="text-lg">
                Welcome to The Fitting Room, where fashion meets personalization. We believe that everyone deserves to
                feel confident and comfortable in what they wear.
              </p>

              <p className="text-lg">
                Our mission is simple: help you discover clothing that truly fits your unique style, body type, and
                lifestyle. No more endless scrolling through items that don&apos;t match your preferences. No more
                buying pieces that don&apos;t quite work.
              </p>

              <div className="my-8 rounded-2xl overflow-hidden">
                <Image
                  src="/images/design-mode/Screenshot%202025-11-08%20012041.png"
                  alt="Shopping experience"
                  width={800}
                  height={400}
                  className="w-full h-auto"
                />
              </div>

              <p className="text-lg">
                We use your personal style preferences, measurements, and favorite aesthetics to curate a shopping
                experience tailored just for you. Every recommendation is handpicked to match your criteria, ensuring
                that every piece you discover is one you&apos;ll love.
              </p>

              <div className="bg-[#F9F6F3] rounded-2xl p-6 md:p-8 mt-8">
                <h2 className="text-2xl font-serif text-[#C4A69D] mb-4">Our Values</h2>
                <ul className="space-y-3 text-[#6B5A52]">
                  <li className="flex items-start">
                    <span className="text-[#C4A69D] mr-2">•</span>
                    <span>
                      <strong>Personalization first</strong> - your style is unique
                    </span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-[#C4A69D] mr-2">•</span>
                    <span>
                      <strong>Quality over quantity</strong> - curated selections
                    </span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-[#C4A69D] mr-2">•</span>
                    <span>
                      <strong>Inclusive sizing</strong> - fashion for every body
                    </span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </main>
    </>
  )
}
