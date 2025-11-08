import { NextResponse } from "next/server"

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:5001"

export async function GET() {
  try {
    console.log("[v0] Fetching brands from Flask API")

    const response = await fetch(`${API_BASE}/api/brands`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })

    if (!response.ok) {
      throw new Error(`Flask API returned ${response.status}`)
    }

    const data = await response.json()
    console.log("[v0] Found brands:", data.brands?.length || 0)

    return NextResponse.json(data)
  } catch (error) {
    console.error("[v0] Brands API error:", error)
    return NextResponse.json({ error: "Failed to fetch brands", brands: [] }, { status: 500 })
  }
}
