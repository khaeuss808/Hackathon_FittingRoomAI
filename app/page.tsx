"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Slider } from "@/components/ui/slider"

const SIZES = ["0", "2", "4", "6", "8", "10", "12", "14", "16"]
const HEIGHTS = [
  { value: "under_5", label: "< 5'" },
  { value: "5_to_5_5", label: "5'1\" - 5'5\"" },
  { value: "5_5_to_5_8", label: "5'5\" - 5'8\"" },
  { value: "over_5_9", label: "5'9\"+'" },
]
const STYLES = ["Casual", "Elegant", "Boho", "Minimalist", "Edgy", "Romantic"]

export default function HomePage() {
  const router = useRouter()
  const [selectedSize, setSelectedSize] = useState<string>("")
  const [selectedHeight, setSelectedHeight] = useState<string>("")
  const [priceRange, setPriceRange] = useState([0, 100])
  const [selectedStyles, setSelectedStyles] = useState<string[]>([])

  const toggleStyle = (style: string) => {
    setSelectedStyles((prev) => (prev.includes(style) ? prev.filter((s) => s !== style) : [...prev, style]))
  }

  const handleSearch = () => {
    const params = new URLSearchParams()

    if (selectedSize) params.set("sizes", selectedSize)
    if (selectedHeight) params.set("heights", selectedHeight)
    params.set("minPrice", priceRange[0].toString())
    params.set("maxPrice", priceRange[1].toString())
    // Join multiple styles into a single "aesthetic" query for Flask
    if (selectedStyles.length > 0) {
      params.set("aesthetic", selectedStyles.join(", "))
    }

    console.log("[v0] Searching with filters:", Object.fromEntries(params))
    router.push(`/shop?${params.toString()}`)
  }

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-2xl mx-auto">
        <Card className="p-8 bg-white/80 backdrop-blur border-[#E8DFD8]">
          <h1 className="text-3xl font-serif text-center mb-8 text-[#5C4A42]">Personalize Your Search</h1>

          {/* Size Selection */}
          <div className="mb-8">
            <Label className="text-base mb-3 block text-center text-[#5C4A42]">My size:</Label>
            <div className="grid grid-cols-4 md:grid-cols-8 gap-2">
              {SIZES.map((size) => (
                <Button
                  key={size}
                  variant={selectedSize === size ? "default" : "outline"}
                  onClick={() => setSelectedSize(size)}
                  className={`${
                    selectedSize === size
                      ? "bg-[#C4A69D] text-white hover:bg-[#B39589]"
                      : "bg-white border-[#E8DFD8] text-[#5C4A42] hover:bg-[#E8DFD8]"
                  }`}
                >
                  {size}
                </Button>
              ))}
            </div>
          </div>

          {/* Height Selection */}
          <div className="mb-8">
            <Label className="text-base mb-3 block text-center text-[#5C4A42]">Height:</Label>
            <RadioGroup value={selectedHeight} onValueChange={setSelectedHeight} className="grid grid-cols-2 gap-3">
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
                  <Label htmlFor={height.value} className="cursor-pointer text-[#5C4A42] flex-1">
                    {height.label}
                  </Label>
                </div>
              ))}
            </RadioGroup>
          </div>

          {/* Price Range */}
          <div className="mb-8">
            <Label className="text-base mb-3 block text-center text-[#5C4A42]">Price Range:</Label>
            <div className="px-2">
              <Slider value={priceRange} onValueChange={setPriceRange} max={200} step={10} className="mb-2" />
              <p className="text-center text-sm text-[#7A6B63]">
                ${priceRange[0]} - ${priceRange[1] === 200 ? "200+" : priceRange[1]}
              </p>
            </div>
          </div>

          {/* Style Selection */}
          <div className="mb-8">
            <Label className="text-base mb-3 block text-center text-[#5C4A42]">My style:</Label>
            <div className="grid grid-cols-2 gap-3">
              {STYLES.map((style) => (
                <Button
                  key={style}
                  variant={selectedStyles.includes(style) ? "default" : "outline"}
                  onClick={() => toggleStyle(style)}
                  className={`h-auto py-4 text-base ${
                    selectedStyles.includes(style)
                      ? "bg-[#C4A69D] text-white hover:bg-[#B39589]"
                      : "bg-white border-[#E8DFD8] text-[#5C4A42] hover:bg-[#E8DFD8]"
                  }`}
                >
                  {style}
                </Button>
              ))}
            </div>
          </div>

          {/* Search Button */}
          <Button
            onClick={handleSearch}
            className="w-full bg-[#C4A69D] hover:bg-[#B39589] text-white h-12 text-lg"
            disabled={selectedStyles.length === 0}
          >
            Find My Perfect Fit
          </Button>
        </Card>
      </div>
    </div>
  )
}
