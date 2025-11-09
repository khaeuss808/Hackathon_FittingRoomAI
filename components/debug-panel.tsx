"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { AlertCircle, CheckCircle2, XCircle } from "lucide-react"

interface HealthCheck {
  status: string
  checks: {
    nextjs: boolean
    flask: boolean
    flaskUrl: string
    timestamp: string
  }
  error?: string
}

export function DebugPanel() {
  const [health, setHealth] = useState<HealthCheck | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function checkHealth() {
      try {
        const response = await fetch("/api/health")
        const data = await response.json()
        setHealth(data)
      } catch (error) {
        console.error("Health check failed:", error)
      } finally {
        setLoading(false)
      }
    }

    checkHealth()
    // Refresh every 5 seconds
    const interval = setInterval(checkHealth, 5001)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return null
  }

  return (
    <Card className="fixed bottom-4 right-4 w-80 shadow-lg z-50">
      <CardHeader className="pb-3">
        <CardTitle className="text-sm flex items-center gap-2">
          Integration Status
          {health?.status === "healthy" ? (
            <CheckCircle2 className="h-4 w-4 text-green-500" />
          ) : (
            <XCircle className="h-4 w-4 text-red-500" />
          )}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-2 text-xs">
        <div className="flex items-center justify-between">
          <span>Next.js Frontend</span>
          <Badge variant={health?.checks.nextjs ? "default" : "destructive"}>
            {health?.checks.nextjs ? "Connected" : "Error"}
          </Badge>
        </div>
        <div className="flex items-center justify-between">
          <span>Flask Backend</span>
          <Badge variant={health?.checks.flask ? "default" : "destructive"}>
            {health?.checks.flask ? "Connected" : "Disconnected"}
          </Badge>
        </div>
        <div className="text-muted-foreground">Flask URL: {health?.checks.flaskUrl}</div>
        {health?.error && (
          <div className="flex items-start gap-1 text-red-600">
            <AlertCircle className="h-3 w-3 mt-0.5 flex-shrink-0" />
            <span className="text-xs">{health.error}</span>
          </div>
        )}
        {!health?.checks.flask && (
          <div className="mt-2 p-2 bg-yellow-50 border border-yellow-200 rounded text-yellow-800">
            <p className="font-medium">Flask not running</p>
            <p className="mt-1">Run: cd backend && python main.py</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
