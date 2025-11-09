import { Card } from "@/components/ui/card"
import Image from "next/image"

export default function AboutPage() {
  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <Card className="p-8 md:p-12 bg-white/80 backdrop-blur border-[#E8DFD8]">
          <h1 className="text-4xl md:text-5xl font-serif text-center mb-6 text-[#5C4A42]">About The Fitting Room</h1>

          <div className="prose prose-lg max-w-none">
            <p className="text-lg text-[#7A6B63] font-sans leading-relaxed mb-6">
              Welcome to The Fitting Room, where fashion meets personalization. We believe that everyone deserves to
              feel confident and comfortable in what they wear.
            </p>

            <p className="text-lg text-[#7A6B63] font-sans leading-relaxed mb-6">
              Our mission is simple: help you discover clothing that truly fits your unique style, body type, and
              lifestyle. No more endless scrolling through items that don't match your preferences. No more buying
              pieces that don't quite work.
            </p>

            <div className="relative w-full h-64 md:h-96 my-8 rounded-lg overflow-hidden">
              <Image src="/about.png" alt="The Fitting Room store" fill className="object-cover" />
            </div>

            <h2 className="text-2xl font-serif text-[#5C4A42] mt-8 mb-4">How It Works</h2>

            <div className="space-y-4 mb-8">
              <div className="flex gap-4">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-[#C4A69D] flex items-center justify-center text-white font-bold">
                  1
                </div>
                <div>
                  <h3 className="font-bold text-[#5C4A42] mb-1">Tell Us About Yourself</h3>
                  <p className="text-[#7A6B63] font-sans">
                    Share your size, height, style preferences, and budget to personalize your experience.
                  </p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-[#C4A69D] flex items-center justify-center text-white font-bold">
                  2
                </div>
                <div>
                  <h3 className="font-bold text-[#5C4A42] mb-1">Browse Curated Results</h3>
                  <p className="text-[#7A6B63] font-sans">
                    We search across multiple brands to find pieces that match your specific criteria.
                  </p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-[#C4A69D] flex items-center justify-center text-white font-bold">
                  3
                </div>
                <div>
                  <h3 className="font-bold text-[#5C4A42] mb-1">Find Your Perfect Fit</h3>
                  <p className="text-[#7A6B63] font-sans">
                    Discover clothing that works for you, with direct links to purchase from trusted retailers.
                  </p>
                </div>
              </div>
            </div>

            <h2 className="text-2xl font-serif text-[#5C4A42] mt-8 mb-4">Our Vision</h2>

            <p className="text-lg text-[#7A6B63] font-sans leading-relaxed mb-6">
              We're building more than just a search engine. We're creating a personalized shopping experience that
              understands your needs and helps you build a wardrobe you love. Our AI-powered recommendations learn from
              your preferences to suggest pieces that truly fit your style.
            </p>

            <p className="text-lg text-[#7A6B63] font-sans leading-relaxed">
              Join us in revolutionizing the way you shop for clothes. Welcome to your fitting room.
            </p>
          </div>
        </Card>
      </div>
    </div>
  )
}
