"use client"

import { useState, useEffect, Suspense } from "react"
import { useSearchParams } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Slider } from "@/components/ui/slider"
import { X, ChevronLeft, ChevronRight } from "lucide-react"
import { Header } from "@/components/header"
import Image from "next/image"

const API_BASE = process.env.NEXT_PUBLIC_API_URL || ""

interface Product {
  id?: string
  name: string
  product_name?: string
  brand: string
  price: number
  price_raw?: number
  image_url?: string
  image?: string
  product_url?: string
  url?: string
  category?: string
  availability?: string
  styles?: string
}

function ShopContent() {
  const searchParams = useSearchParams()
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [total, setTotal] = useState(0)
  const perPage = 20

  // Filter states
  const [keywords, setKeywords] = useState<string[]>([])
  const [priceRange, setPriceRange] = useState([0, 200])
  const [selectedColors, setSelectedColors] = useState<string[]>([])
  const [selectedSizes, setSelectedSizes] = useState<string[]>([])

  useEffect(() => {
    // Parse initial search params
    const aesthetic = searchParams.get("aesthetic")
    if (aesthetic) {
      setKeywords([aesthetic])
    }
    const minPrice = searchParams.get("min_price")
    const maxPrice = searchParams.get("max_price")
    if (minPrice && maxPrice) {
      setPriceRange([Number.parseInt(minPrice), Number.parseInt(maxPrice)])
    }
  }, [searchParams])

  useEffect(() => {
    fetchProducts()
  }, [page, keywords, priceRange])

  const fetchProducts = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE}/api/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          styles: keywords,
          min_price: priceRange[0],
          max_price: priceRange[1],
          page,
          per_page: perPage,
        }),
      })

      if (!response.ok) {
        throw new Error(`API returned ${response.status}`)
      }

      const data = await response.json()
      console.log("Fetched products:", data)
      setProducts(data.products || [])
      setTotal(data.total || 0)
      setTotalPages(Math.ceil((data.total || 0) / perPage))
    } catch (error) {
      console.error("Error fetching products:", error)
      setProducts([])
      setTotal(0)
      setTotalPages(1)
    } finally {
      setLoading(false)
    }
  }

  const addKeyword = (keyword: string) => {
    if (keyword && !keywords.includes(keyword)) {
      setKeywords([...keywords, keyword])
      setPage(1)
    }
  }

  const removeKeyword = (keyword: string) => {
    setKeywords(keywords.filter((k) => k !== keyword))
    setPage(1)
  }

  const formatPrice = (product: Product) => {
    const price = product.price ?? product.price_raw ?? 0
    return `$${Number(price).toFixed(2)}`
  }

  return (
    <>
      <Header />
      <main className="min-h-screen bg-[#F5F1ED]">
        <div className="flex flex-col lg:flex-row">
          {/* Filters Sidebar */}
          <aside className="w-full lg:w-80 bg-white p-6 lg:min-h-screen">
            <h2 className="text-2xl font-serif text-[#5C4A42] mb-6">Filters</h2>

            {/* Keywords */}
            <div className="mb-6">
              <h3 className="text-lg font-medium text-[#5C4A42] mb-3">Keywords</h3>
              <div className="flex flex-wrap gap-2 mb-3">
                {keywords.map((keyword) => (
                  <button
                    key={keyword}
                    onClick={() => removeKeyword(keyword)}
                    className="inline-flex items-center gap-1 px-3 py-1 bg-[#C4A69D] text-white rounded-full text-sm"
                  >
                    {keyword}
                    <X className="w-3 h-3" />
                  </button>
                ))}
              </div>
              <input
                type="text"
                placeholder="Add keyword..."
                className="w-full px-3 py-2 border border-[#D4C4BC] rounded-lg text-sm"
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    addKeyword((e.target as HTMLInputElement).value)
                    ;(e.target as HTMLInputElement).value = ""
                  }
                }}
              />
            </div>

            {/* Price Range */}
            <div className="mb-6">
              <h3 className="text-lg font-medium text-[#5C4A42] mb-3">
                Price: ${priceRange[0]} - ${priceRange[1]}
              </h3>
              <Slider min={0} max={500} step={10} value={priceRange} onValueChange={setPriceRange} />
            </div>

            {/* Apply Filters Button */}
            <Button
              onClick={() => {
                setPage(1)
                fetchProducts()
              }}
              className="w-full bg-[#C4A69D] hover:bg-[#B09589] text-white"
            >
              Apply Filters
            </Button>
          </aside>

          {/* Products Grid */}
          <div className="flex-1 p-6">
            <div className="mb-6 flex justify-between items-center">
              <p className="text-[#6B5A52]">{loading ? "Loading..." : `${total} items found`}</p>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page === 1 || loading}
                  className="border-[#D4C4BC]"
                >
                  <ChevronLeft className="w-4 h-4" />
                </Button>
                <span className="px-3 py-1 text-[#6B5A52]">
                  Page {page} of {totalPages}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  disabled={page === totalPages || loading}
                  className="border-[#D4C4BC]"
                >
                  <ChevronRight className="w-4 h-4" />
                </Button>
              </div>
            </div>

            {loading ? (
              <div className="text-center py-20 text-[#6B5A52]">Loading products...</div>
            ) : products.length === 0 ? (
              <div className="text-center py-20 text-[#6B5A52]">No products found. Try adjusting your filters.</div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {products.map((product, idx) => (
                  <div
                    key={product.id || idx}
                    className="bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow"
                  >
                    <div className="aspect-square relative bg-[#E8DFD8]">
                      {(product.image_url || product.image) && (
                        <Image
                          src={product.image_url || product.image || ""}
                          alt={product.name || product.product_name || "Product"}
                          fill
                          className="object-cover"
                        />
                      )}
                    </div>
                    <div className="p-4">
                      <h3 className="text-sm font-medium text-[#5C4A42] mb-1 line-clamp-2">
                        {product.name || product.product_name || "Unnamed Product"}
                      </h3>
                      <p className="text-xs text-[#6B5A52]">${product.price || "N/A"}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </>
  )
}

export default function ShopPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-[#F5F1ED] flex items-center justify-center">Loading...</div>}>
      <ShopContent />
    </Suspense>
  )
}
