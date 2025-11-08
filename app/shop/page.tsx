"use client"

import { useEffect, useState } from "react"
import { useSearchParams } from "next/navigation"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { AlertCircle, Loader2 } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"
import Image from "next/image"

interface Product {
  id: number
  name: string
  brand: string
  price: number
  image: string
  url: string
  color?: string
  availability?: string
}

interface SearchResponse {
  results: Product[]
  total: number
  page: number
  limit: number
  totalPages: number
  error?: string
}

export default function ShopPage() {
  const searchParams = useSearchParams()
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [total, setTotal] = useState(0)

  useEffect(() => {
    const aesthetic = searchParams.get("aesthetic")
    const sizes = searchParams.get("sizes")
    const heights = searchParams.get("heights")
    const minPrice = searchParams.get("minPrice")
    const maxPrice = searchParams.get("maxPrice")

    console.log("[v0] Shop page filters:", { aesthetic, sizes, heights, minPrice, maxPrice })

    fetchProducts(currentPage)
  }, [searchParams, currentPage])

  async function fetchProducts(page: number) {
    setLoading(true)
    setError(null)

    try {
      const params = new URLSearchParams(searchParams.toString())
      params.set("page", page.toString())
      params.set("limit", "20")

      console.log("[v0] Fetching products with params:", params.toString())

      const response = await fetch(`/api/search?${params.toString()}`)
      const data: SearchResponse = await response.json()

      if (data.error) {
        setError(data.error)
        setProducts([])
        setTotal(0)
        setTotalPages(1)
      } else {
        const productList = data.results || []
        console.log("[v0] Received", productList.length, "products")
        setProducts(productList)
        setTotal(data.total || 0)
        setTotalPages(data.totalPages || 1)
      }
    } catch (err) {
      console.error("[v0] Error fetching products:", err)
      setError(err instanceof Error ? err.message : "Failed to load products")
      setProducts([])
      setTotal(0)
      setTotalPages(1)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-[#C4A69D]" />
      </div>
    )
  }

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-serif mb-6 text-[#5C4A42]">Your Perfect Fit</h1>

        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {products.length === 0 && !error && (
          <Alert className="bg-white/80 border-[#E8DFD8]">
            <AlertDescription className="text-[#5C4A42]">
              No products found matching your filters. Try adjusting your preferences or make sure your Flask backend is
              running on port 5001.
            </AlertDescription>
          </Alert>
        )}

        {total > 0 && (
          <p className="text-[#7A6B63] mb-6">
            Showing {products.length} of {total} products
          </p>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">
          {products.map((product) => (
            <Card
              key={product.id}
              className="flex flex-col bg-white border-[#E8DFD8] hover:shadow-lg transition-shadow"
            >
              <CardHeader className="p-0">
                <div className="relative aspect-square bg-[#F5F1ED]">
                  {product.image ? (
                    <Image
                      src={product.image || "/placeholder.svg"}
                      alt={product.name}
                      fill
                      className="object-cover rounded-t-lg"
                      unoptimized
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-[#7A6B63]">No image</div>
                  )}
                </div>
              </CardHeader>
              <CardContent className="flex-1 p-4">
                <CardTitle className="text-base mb-2 line-clamp-2 text-[#5C4A42]">{product.name}</CardTitle>
                <div className="flex items-center justify-between mb-2">
                  <Badge className="bg-[#E8DFD8] text-[#5C4A42] hover:bg-[#E8DFD8]">{product.brand}</Badge>
                  <span className="font-bold text-lg text-[#5C4A42]">${product.price.toFixed(2)}</span>
                </div>
                {product.color && <p className="text-sm text-[#7A6B63]">Color: {product.color}</p>}
              </CardContent>
              <CardFooter className="p-4 pt-0">
                {product.url ? (
                  <Button className="w-full bg-[#C4A69D] hover:bg-[#B39589] text-white" asChild>
                    <a href={product.url} target="_blank" rel="noopener noreferrer">
                      View Product
                    </a>
                  </Button>
                ) : (
                  <Button className="w-full" disabled>
                    No Link Available
                  </Button>
                )}
              </CardFooter>
            </Card>
          ))}
        </div>

        {totalPages > 1 && (
          <div className="flex items-center justify-center gap-2">
            <Button
              variant="outline"
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              disabled={currentPage === 1}
              className="border-[#E8DFD8] text-[#5C4A42] hover:bg-[#E8DFD8]"
            >
              Previous
            </Button>
            <span className="text-sm text-[#7A6B63]">
              Page {currentPage} of {totalPages}
            </span>
            <Button
              variant="outline"
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages}
              className="border-[#E8DFD8] text-[#5C4A42] hover:bg-[#E8DFD8]"
            >
              Next
            </Button>
          </div>
        )}
      </div>
    </div>
  )
}
