"use client"

import { useState } from "react"
import { Search } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useRouter } from "next/navigation"
import Image from "next/image"

export default function Home() {
  const [showFilters, setShowFilters] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedSize, setSelectedSize] = useState<string>("")
  const [selectedBrands, setSelectedBrands] = useState<string[]>([])
  const [priceRange, setPriceRange] = useState([0, 100])
  const router = useRouter()

  const sizes = ["0", "2", "4", "6", "8", "10", "12", "14", "16"]
  const brands = ["Zara", "H&M", "Abercrombie", "Urban Outfitters"]

  const handleSearch = () => {
    if (searchQuery.trim()) {
      router.push(`/shop?query=${encodeURIComponent(searchQuery)}`)
    }
  }

  const handleGetStarted = () => {
    setShowFilters(!showFilters)
  }

  const handleFilterSubmit = () => {
    const params = new URLSearchParams()
    if (selectedSize) params.set("sizes", selectedSize)
    if (selectedBrands.length > 0) params.set("brands", selectedBrands.join(","))
    params.set("minPrice", priceRange[0].toString())
    params.set("maxPrice", priceRange[1].toString())

    router.push(`/shop?${params.toString()}`)
  }

  const toggleBrand = (brand: string) => {
    setSelectedBrands((prev) => (prev.includes(brand) ? prev.filter((b) => b !== brand) : [...prev, brand]))
  }

  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-4">
      <div className="mb-12">
        <Image src="/logo.png" alt="The Fitting Room" width={300} height={100} className="object-contain" />
      </div>

      {/* Hero Section */}
      <div className="w-full max-w-2xl text-center space-y-8">
        <h1 className="text-5xl md:text-6xl font-serif text-[#C4A69D] mb-8">Find your fit</h1>

        <div className="relative">
          <div className="glass-search-bar flex items-center gap-3 px-6 py-4 rounded-full">
            <Search className="w-5 h-5 text-[#C4A69D] shrink-0" />
            <input
              type="text"
              placeholder="search styles"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              className="flex-1 bg-transparent border-none outline-none text-[#5C4A42] placeholder:text-[#C4A69D]/60 font-serif"
            />
          </div>
        </div>

        {/* Get Started Button */}
        <Button
          onClick={handleGetStarted}
          size="lg"
          className="bg-[#C4A69D] hover:bg-[#B89888] text-white px-12 py-6 rounded-full text-lg font-serif"
        >
          Get Started Now
        </Button>

        {showFilters && (
          <div className="mt-12 glass-card p-8 rounded-3xl space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <h2 className="text-2xl font-serif text-[#C4A69D]">Personalize Your Search</h2>

            {/* Size Selection */}
            <div className="space-y-4">
              <label className="text-sm font-serif text-[#5C4A42]">My size:</label>
              <div className="flex flex-wrap gap-2">
                {sizes.map((size) => (
                  <button
                    key={size}
                    onClick={() => setSelectedSize(size)}
                    className={`px-6 py-2 rounded-full border-2 font-serif transition-all ${
                      selectedSize === size
                        ? "border-[#C4A69D] bg-[#C4A69D] text-white"
                        : "border-[#C4A69D]/30 bg-white/50 text-[#5C4A42] hover:border-[#C4A69D]"
                    }`}
                  >
                    {size}
                  </button>
                ))}
              </div>
            </div>

            {/* Brand Selection */}
            <div className="space-y-4">
              <label className="text-sm font-serif text-[#5C4A42]">My brands:</label>
              <div className="flex flex-wrap gap-2">
                {brands.map((brand) => (
                  <button
                    key={brand}
                    onClick={() => toggleBrand(brand)}
                    className={`px-6 py-2 rounded-full border-2 font-serif transition-all ${
                      selectedBrands.includes(brand)
                        ? "border-[#C4A69D] bg-[#C4A69D] text-white"
                        : "border-[#C4A69D]/30 bg-white/50 text-[#5C4A42] hover:border-[#C4A69D]"
                    }`}
                  >
                    {brand}
                  </button>
                ))}
              </div>
            </div>

            {/* Price Range */}
            <div className="space-y-4">
              <label className="text-sm font-serif text-[#5C4A42]">Price Range:</label>
              <div className="space-y-2">
                <input
                  type="range"
                  min="0"
                  max="500"
                  value={priceRange[1]}
                  onChange={(e) => setPriceRange([0, Number.parseInt(e.target.value)])}
                  className="w-full accent-[#C4A69D]"
                />
                <p className="text-center font-serif text-[#5C4A42]">
                  ${priceRange[0]} - ${priceRange[1]}+
                </p>
              </div>
            </div>

            <Button
              onClick={handleFilterSubmit}
              size="lg"
              className="w-full bg-[#C4A69D] hover:bg-[#B89888] text-white py-6 rounded-full text-lg font-serif"
            >
              Find My Perfect Fit
            </Button>
          </div>
        )}
      </div>
    </main>
  )
}
