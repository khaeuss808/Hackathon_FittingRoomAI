import { type NextRequest, NextResponse } from "next/server"

const FLASK_API_URL = process.env.FLASK_API_URL || "http://127.0.0.1:5001"

export async function GET(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params
    const flaskUrl = `${FLASK_API_URL}/api/product/${id}`

    console.log("[v0] Fetching product from Flask:", flaskUrl)

    const response = await fetch(flaskUrl, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })

    if (!response.ok) {
      if (response.status === 404) {
        return NextResponse.json({ error: "Product not found" }, { status: 404 })
      }
      const errorText = await response.text()
      console.error("[v0] Flask API error:", response.status, errorText)
      return NextResponse.json({ error: `Backend API error: ${response.status}` }, { status: response.status })
    }

    const data = await response.json()
    console.log("[v0] Flask returned product:", data.name)

    return NextResponse.json(data)
  } catch (error) {
    console.error("[v0] Error connecting to Flask backend:", error)
    return NextResponse.json(
      {
        error: "Failed to connect to backend. Is Flask running on port 5001?",
      },
      { status: 500 },
    )
  }
}
