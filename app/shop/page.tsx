"use client"

import { useEffect, useState } from "react"
import { useSearchParams } from "next/navigation"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { AlertCircle, Loader2 } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"
import Image from "next/image"

type Product = {
  id: string
  name: string
  brand: string
  price: number
  image_url?: string
  product_url?: string
  color?: string
  availability?: string
}

type ApiProduct = {
  product_id?: string | number
  reference?: string | number
  name: string
  brand: string
  price?: number
  price_cents?: number
  image_url?: string
  product_url?: string
  color?: string
  availability?: string
}

type SearchResponseLoose = {
  // backend might return either `results` or `products`
  results?: ApiProduct[]
  products?: ApiProduct[]
  total?: number
  page?: number
  limit?: number
  totalPages?: number
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
    fetchProducts(currentPage)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams, currentPage])

  async function fetchProducts(page: number) {
    setLoading(true)
    setError(null)
    try {
      const params = new URLSearchParams(searchParams.toString())
      params.set("page", String(page))
      params.set("limit", "20")

      const res = await fetch(`/api/search?${params.toString()}`)
      const data: SearchResponseLoose = await res.json()

      if (data.error) throw new Error(data.error)

      const raw: ApiProduct[] = (data.results ?? data.products ?? []) as ApiProduct[]

      const normalized: Product[] = raw.map((p, i) => ({
        id: String(p.product_id ?? p.reference ?? i),
        name: p.name,
        brand: p.brand,
        price:
          typeof p.price === "number"
            ? p.price
            : typeof p.price_cents === "number"
            ? Math.round(p.price_cents) / 100
            : 0,
        image_url: p.image_url,
        product_url: p.product_url,
        color: p.color,
        availability: p.availability,
      }))

      setProducts(normalized)
      const computedTotal = typeof data.total === "number" ? data.total : normalized.length
      setTotal(computedTotal)
      setTotalPages(data.totalPages ?? 1)
    } catch (e) {
      console.error("[shop] fetch error:", e)
      setError(e instanceof Error ? e.message : "Failed to load products")
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

        {!error && total === 0 && (
          <Alert className="bg-white/80 border-[#E8DFD8]">
            <AlertDescription>No products found. Try adjusting your filters.</AlertDescription>
          </Alert>
        )}

        {total > 0 && (
          <p className="text-[#7A6B63] mb-6">
            Showing {products.length} of {total} products
          </p>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">
          {products.map((product) => (
            <Card key={product.id} className="flex flex-col bg-white border-[#E8DFD8] hover:shadow-lg transition-shadow">
              <CardHeader className="p-0">
                <div className="relative aspect-square bg-[#F5F1ED] rounded-t-lg overflow-hidden">
                  {product.image_url ? (
                    <Image
                      src={product.image_url}
                      alt={product.name}
                      fill
                      className="object-cover"
                      unoptimized
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-[#7A6B63]">
                      No image
                    </div>
                  )}
                </div>
              </CardHeader>
              <CardContent className="flex-1 p-4">
                <CardTitle className="text-base mb-2 line-clamp-2 text-[#5C4A42]">
                  {product.name}
                </CardTitle>
                <div className="flex items-center justify-between mb-2">
                  <Badge className="bg-[#E8DFD8] text-[#5C4A42] hover:bg-[#E8DFD8]">
                    {product.brand}
                  </Badge>
                  <span className="font-bold text-lg text-[#5C4A42]">
                    ${product.price.toFixed(2)}
                  </span>
                </div>
                {product.color && (
                  <p className="text-sm text-[#7A6B63]">Color: {product.color}</p>
                )}
              </CardContent>
              <CardFooter className="p-4 pt-0">
                {product.product_url ? (
                  <Button className="w-full bg-[#C4A69D] hover:bg-[#B39589] text-white" asChild>
                    <a href={product.product_url} target="_blank" rel="noopener noreferrer">
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
            <Button disabled={currentPage === 1} onClick={() => setCurrentPage(p => Math.max(p - 1, 1))}>
              Previous
            </Button>
            <span>Page {currentPage} of {totalPages}</span>
            <Button disabled={currentPage === totalPages} onClick={() => setCurrentPage(p => Math.min(p + 1, totalPages))}>
              Next
            </Button>
          </div>
        )}
      </div>
    </div>
  )
}