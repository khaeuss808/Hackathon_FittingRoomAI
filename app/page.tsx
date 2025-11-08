"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { Slider } from "@/components/ui/slider"
import { X } from "lucide-react"
import { Header } from "@/components/header"

export default function HomePage() {
  const router = useRouter()
  const [selectedSizes, setSelectedSizes] = useState<string[]>([])
  const [selectedHeight, setSelectedHeight] = useState<string>("")
  const [priceRange, setPriceRange] = useState([0, 200])
  const [aesthetic, setAesthetic] = useState("")
  const [selectedBrands, setSelectedBrands] = useState<string[]>([])

  const sizes = ["0", "2", "4", "6", "8", "10", "12", "14", "16"]
  const heights = [
    { value: "<5'", label: "< 5'" },
    { value: "<5'1-5'5", label: "< 5'1 - 5'5" },
    { value: "<5'5-5'8", label: "< 5'5 - 5'8" },
    { value: "<5'9+", label: "< 5'9+" },
  ]
  const brands = ["H&M", "Zara", "Everlane", "Reformation", "Patagonia"]

  const handleSizeToggle = (size: string) => {
    setSelectedSizes((prev) => (prev.includes(size) ? prev.filter((s) => s !== size) : [...prev, size]))
  }

  const handleBrandToggle = (brand: string) => {
    setSelectedBrands((prev) => (prev.includes(brand) ? prev.filter((b) => b !== brand) : [...prev, brand]))
  }

  const handleSearch = () => {
    const params = new URLSearchParams()
    if (selectedSizes.length) params.set("sizes", selectedSizes.join(","))
    if (selectedHeight) params.set("height", selectedHeight)
    params.set("min_price", priceRange[0].toString())
    params.set("max_price", priceRange[1].toString())
    if (aesthetic) params.set("aesthetic", aesthetic)
    if (selectedBrands.length) params.set("brands", selectedBrands.join(","))

    router.push(`/shop?${params.toString()}`)
  }

  return (
    <>
      <Header />
      <main className="min-h-screen bg-[#F5F1ED] py-12 px-4">
        <div className="max-w-2xl mx-auto">
          <div className="bg-white rounded-3xl shadow-sm p-8 md:p-12">
            <h1 className="text-3xl md:text-4xl font-serif text-center text-[#5C4A42] mb-8">Personalize Your Search</h1>

            {/* Size Selection */}
            <div className="mb-8">
              <h2 className="text-lg font-medium text-[#5C4A42] mb-4 text-center">My size:</h2>
              <div className="flex flex-wrap justify-center gap-3">
                {sizes.map((size) => (
                  <button
                    key={size}
                    onClick={() => handleSizeToggle(size)}
                    className={`w-12 h-12 flex items-center justify-center border-2 rounded-lg transition-colors ${
                      selectedSizes.includes(size)
                        ? "border-[#C4A69D] bg-[#C4A69D]/10 text-[#5C4A42]"
                        : "border-[#D4C4BC] text-[#8C7A72] hover:border-[#C4A69D]"
                    }`}
                  >
                    {size}
                  </button>
                ))}
              </div>
            </div>

            {/* Height Selection */}
            <div className="mb-8">
              <h2 className="text-lg font-medium text-[#5C4A42] mb-4 text-center">Height:</h2>
              <RadioGroup value={selectedHeight} onValueChange={setSelectedHeight}>
                <div className="flex flex-wrap justify-center gap-4">
                  {heights.map((height) => (
                    <div key={height.value} className="flex items-center space-x-2">
                      <RadioGroupItem value={height.value} id={height.value} />
                      <Label htmlFor={height.value} className="text-[#5C4A42] cursor-pointer">
                        {height.label}
                      </Label>
                    </div>
                  ))}
                </div>
              </RadioGroup>
            </div>

            {/* Price Range */}
            <div className="mb-8">
              <h2 className="text-lg font-medium text-[#5C4A42] mb-4 text-center">Price Range:</h2>
              <div className="px-4">
                <Slider min={0} max={500} step={10} value={priceRange} onValueChange={setPriceRange} className="mb-3" />
                <div className="flex justify-between text-sm text-[#8C7A72]">
                  <span>${priceRange[0]}</span>
                  <span>${priceRange[1]}</span>
                </div>
              </div>
            </div>

            {/* Aesthetic Input */}
            <div className="mb-8">
              <h2 className="text-lg font-medium text-[#5C4A42] mb-4 text-center">What&apos;s your vibe?</h2>
              <input
                type="text"
                placeholder="e.g., clean girl aesthetic, cottagecore, minimalist..."
                value={aesthetic}
                onChange={(e) => setAesthetic(e.target.value)}
                className="w-full px-4 py-3 border-2 border-[#D4C4BC] rounded-lg focus:outline-none focus:border-[#C4A69D] text-[#5C4A42] placeholder:text-[#B8A8A0]"
              />
            </div>

            {/* Brands Selection */}
            <div className="mb-8">
              <h2 className="text-lg font-medium text-[#5C4A42] mb-4 text-center">Brands I like:</h2>
              <div className="flex flex-wrap justify-center gap-3">
                {selectedBrands.map((brand) => (
                  <button
                    key={brand}
                    onClick={() => handleBrandToggle(brand)}
                    className="inline-flex items-center gap-2 px-4 py-2 bg-[#C4A69D] text-white rounded-full hover:bg-[#B09589] transition-colors"
                  >
                    {brand}
                    <X className="w-4 h-4" />
                  </button>
                ))}
              </div>
              <div className="flex flex-wrap justify-center gap-3 mt-3">
                {brands
                  .filter((brand) => !selectedBrands.includes(brand))
                  .map((brand) => (
                    <button
                      key={brand}
                      onClick={() => handleBrandToggle(brand)}
                      className="px-4 py-2 border-2 border-[#D4C4BC] text-[#5C4A42] rounded-full hover:border-[#C4A69D] transition-colors"
                    >
                      + {brand}
                    </button>
                  ))}
              </div>
            </div>

            {/* Search Button */}
            <div className="text-center">
              <Button
                onClick={handleSearch}
                className="bg-[#C4A69D] hover:bg-[#B09589] text-white px-12 py-6 text-lg rounded-full"
              >
                Find My Perfect Fit
              </Button>
            </div>
          </div>
        </div>
      </main>
    </>
  )
}
