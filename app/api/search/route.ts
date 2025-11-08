import { type NextRequest, NextResponse } from "next/server"

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:5001"

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    console.log("[v0] Search API called with:", body)

    const params = new URLSearchParams()

    if (body.styles && body.styles.length > 0) {
      params.append("aesthetic", body.styles.join(" "))
    }
    if (body.min_price) {
      params.append("minPrice", body.min_price.toString())
    }
    if (body.max_price) {
      params.append("maxPrice", body.max_price.toString())
    }
    if (body.sizes && body.sizes.length > 0) {
      params.append("sizes", body.sizes.join(","))
    }
    if (body.brands && body.brands.length > 0) {
      params.append("brands", body.brands.join(","))
    }
    params.append("page", (body.page || 1).toString())
    params.append("limit", (body.per_page || 20).toString())

    const response = await fetch(`${API_BASE}/api/search?${params.toString()}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })

    if (!response.ok) {
      const errorText = await response.text()
      console.error("[v0] Flask API error:", response.status, errorText)
      throw new Error(`Flask API returned ${response.status}`)
    }

    const data = await response.json()
    console.log("[v0] Found products:", data.results?.length || 0)

    return NextResponse.json(data)
  } catch (error) {
    console.error("[v0] Search API error:", error)
    return NextResponse.json({ error: "Search failed", results: [], total: 0 }, { status: 500 })
  }
}
