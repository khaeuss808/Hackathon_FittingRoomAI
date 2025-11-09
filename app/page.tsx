"use client"

import { useState } from "react"
import { Search } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useRouter } from "next/navigation"
import Image from "next/image"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"

export default function Home() {
  const router = useRouter()

  const [showFilters, setShowFilters] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedHeight, setSelectedHeight] = useState<string>("")
  const [selectedSize, setSelectedSize] = useState<string>("")
  const [selectedBrands, setSelectedBrands] = useState<string[]>([])
  const [priceRange, setPriceRange] = useState<number[]>([0, 100])

  const HEIGHTS = [
    { value: "under_5", label: "< 5'" },
    { value: "5_to_5_5", label: "5'1\" - 5'5\"" },
    { value: "5_5_to_5_8", label: "5'5\" - 5'8\"" },
    { value: "over_5_9", label: "5'9\"+" },
  ] as const

  const sizes = ["0", "2", "4", "6", "8", "10", "12", "14", "16"]
  const brands = ["Zara", "H&M", "Abercrombie", "Urban Outfitters"]

  const handleSearch = () => {
    if (searchQuery.trim()) {
      router.push(`/shop?query=${encodeURIComponent(searchQuery)}`)
    }
  }

  const handleGetStarted = () => {
    setShowFilters((s) => !s)
  }

  const handleFilterSubmit = () => {
    const params = new URLSearchParams()
    if (selectedSize) params.set("sizes", selectedSize)
    if (selectedHeight) params.set("heights", selectedHeight)
    if (selectedBrands.length > 0) params.set("brands", selectedBrands.join(","))
    params.set("minPrice", priceRange[0].toString())
    params.set("maxPrice", priceRange[1].toString())

    router.push(`/shop?${params.toString()}`)
  }

  const toggleBrand = (brand: string) => {
    setSelectedBrands((prev) =>
      prev.includes(brand) ? prev.filter((b) => b !== brand) : [...prev, brand]
    )
  }

  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-4">
      {/* Logo */}
      <div className="mb-12">
        <Image
          src="/logo.png"
          alt="The Fitting Room"
          width={300}
          height={100}
          className="object-contain"
        />
      </div>

      {/* Hero */}
      <div className="w-full max-w-2xl text-center space-y-8">
        <h1 className="text-5xl md:text-6xl font-serif text-[#C4A69D] mb-8">
          Find your fit
        </h1>

        {/* Search */}
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
              aria-label="Search styles"
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

        {/* Filters Card */}
        {showFilters && (
          <div className="mt-12 glass-card p-8 rounded-3xl space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <h2 className="text-2xl font-serif text-[#C4A69D]">
              Personalize Your Search
            </h2>

            {/* Size */}
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

            {/* Height (moved into the white box, right under Size) */}
            <div className="space-y-4">
              <Label className="text-sm font-serif text-[#5C4A42]">Height:</Label>
              <RadioGroup
                value={selectedHeight}
                onValueChange={setSelectedHeight}
                className="grid grid-cols-2 gap-3"
              >
                {HEIGHTS.map((height) => (
                  <div
                    key={height.value}
                    className={`flex items-center space-x-2 border rounded-lg p-4 cursor-pointer transition-colors ${
                      selectedHeight === height.value
                        ? "border-[#C4A69D] bg-[#C4A69D]/10"
                        : "border-[#E8DFD8] hover:bg-[#E8DFD8]/50"
                    }`}
                    onClick={() => setSelectedHeight(height.value)}
                  >
                    <RadioGroupItem value={height.value} id={height.value} />
                    <Label
                      htmlFor={height.value}
                      className="cursor-pointer text-[#5C4A42] flex-1"
                    >
                      {height.label}
                    </Label>
                  </div>
                ))}
              </RadioGroup>
            </div>

            {/* Brands */}
            <div className="space-y-4">
              <label className="text-sm font-serif text-[#5C4A42]">
                My brands:
              </label>
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

            {/* Price */}
            <div className="space-y-4">
              <label className="text-sm font-serif text-[#5C4A42]">
                Price Range:
              </label>
              <div className="space-y-2">
                <input
                  type="range"
                  min="0"
                  max="500"
                  value={priceRange[1]}
                  onChange={(e) =>
                    setPriceRange([0, Number.parseInt(e.target.value)])
                  }
                  className="w-full accent-[#C4A69D]"
                  aria-label="Max price"
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
