"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Card, CardHeader, CardTitle } from "@/components/ui/card"
import { AlertCircle, Loader2 } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { DebugPanel } from "@/components/debug-panel"

interface BrandsResponse {
  brands: string[]
  error?: string
}

export default function BrandsPage() {
  const router = useRouter()
  const [brands, setBrands] = useState<string[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchBrands() {
      try {
        console.log("[v0] Fetching brands from /api/brands")
        const response = await fetch("/api/brands")
        const data: BrandsResponse = await response.json()

        if (data.error) {
          setError(String(data.error))
        } else {
          console.log("[v0] Received brands:", data.brands)
          setBrands(data.brands)
        }
      } catch (err) {
        console.error("[v0] Error fetching brands:", err)
        setError(err instanceof Error ? err.message : "Failed to load brands")
      } finally {
        setLoading(false)
      }
    }

    fetchBrands()
  }, [])

  const handleBrandClick = (brand: string) => {
    console.log("[v0] Navigating to shop with brand:", brand)
    router.push(`/shop?brands=${encodeURIComponent(brand)}`)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-[#C4A69D]" />
      </div>
    )
  }

  return (
    <>
      <div className="container mx-auto py-12 px-4">
        <h1 className="text-4xl font-serif mb-8 text-[#5C4A42] text-center">Available Brands</h1>

        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {brands.length === 0 && !error && (
          <Alert className="bg-white/80 border-[#E8DFD8]">
            <AlertDescription className="text-[#5C4A42]">
              No brands found in database. Run the Zara scraper to populate data.
            </AlertDescription>
          </Alert>
        )}

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 max-w-6xl mx-auto">
          {brands.map((brand) => (
            <Card
              key={brand}
              onClick={() => handleBrandClick(brand)}
              className="hover:shadow-lg transition-all cursor-pointer bg-white/80 border-[#E8DFD8] hover:border-[#C4A69D]"
            >
              <CardHeader>
                <CardTitle className="text-lg text-[#5C4A42]">{brand}</CardTitle>
              </CardHeader>
            </Card>
          ))}
        </div>
      </div>
      <DebugPanel />
    </>
  )
}
