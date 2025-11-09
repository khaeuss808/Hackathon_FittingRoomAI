import { NextResponse } from "next/server"

const FLASK_API_URL = process.env.FLASK_API_URL || "http://127.0.0.1:5001"

export async function GET() {
  const checks = {
    nextjs: true,
    flask: false,
    flaskUrl: FLASK_API_URL,
    timestamp: new Date().toISOString(),
  }

  try {
    const response = await fetch(`${FLASK_API_URL}/api/brands`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    })

    checks.flask = response.ok

    return NextResponse.json({
      status: checks.flask ? "healthy" : "flask_unreachable",
      checks,
    })
  } catch (error) {
    return NextResponse.json(
      {
        status: "error",
        checks,
        error: error instanceof Error ? error.message : "Unknown error",
      },
      { status: 503 },
    )
  }
}
