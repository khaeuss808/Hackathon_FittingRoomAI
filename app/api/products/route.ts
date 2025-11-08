import { type NextRequest, NextResponse } from "next/server"

const FLASK_API_URL = process.env.FLASK_API_URL || "http://127.0.0.1:5001"

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const brand = searchParams.get("brand")

    const flaskUrl = brand ? `${FLASK_API_URL}/api/products?brand=${brand}` : `${FLASK_API_URL}/api/products`

    console.log("[v0] Fetching products from Flask:", flaskUrl)

    const response = await fetch(flaskUrl, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })

    if (!response.ok) {
      const errorText = await response.text()
      console.error("[v0] Flask API error:", response.status, errorText)
      return NextResponse.json(
        { error: `Backend API error: ${response.status}`, results: [] },
        { status: response.status },
      )
    }

    const data = await response.json()
    console.log("[v0] Flask returned products")

    return NextResponse.json(data)
  } catch (error) {
    console.error("[v0] Error connecting to Flask backend:", error)
    return NextResponse.json(
      {
        error: "Failed to connect to backend. Is Flask running on port 5001?",
        results: [],
      },
      { status: 500 },
    )
  }
}
