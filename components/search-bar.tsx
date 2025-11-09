"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Search } from "lucide-react"

interface SearchBarProps {
  variant?: "hero" | "header"
  placeholder?: string
}

export function SearchBar({
  variant = "header",
  placeholder = "Search for clothing, styles, or describe what you're looking for...",
}: SearchBarProps) {
  const router = useRouter()
  const [query, setQuery] = useState("")

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      console.log("[v0] NLP Search query:", query)
      router.push(`/shop?query=${encodeURIComponent(query)}`)
    }
  }

  if (variant === "hero") {
    return (
      <form onSubmit={handleSearch} className="w-full max-w-2xl mx-auto mb-8">
        <div className="relative glass-search">
          <Input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={placeholder}
            className="h-14 pl-6 pr-32 text-lg border border-white/30 bg-white/40 backdrop-blur-xl text-[#5C4A42] placeholder:text-[#7A6B63] rounded-2xl shadow-lg focus-visible:ring-2 focus-visible:ring-[#C4A69D]/50"
          />
          <Button
            type="submit"
            className="absolute right-2 top-2 bg-[#C4A69D] hover:bg-[#B39589] text-white h-10 rounded-xl"
          >
            <Search className="w-4 h-4 mr-2" />
            Search
          </Button>
        </div>
        <p className="text-xs text-[#7A6B63] text-center mt-2">
          Try: "casual summer dress" or "professional work attire"
        </p>
      </form>
    )
  }

  return (
    <form onSubmit={handleSearch} className="relative max-w-md">
      <Input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder={placeholder}
        className="pr-10 border border-white/30 bg-white/60 backdrop-blur-lg text-[#5C4A42] placeholder:text-[#7A6B63] rounded-xl focus-visible:ring-2 focus-visible:ring-[#C4A69D]/50"
      />
      <Button
        type="submit"
        size="icon"
        variant="ghost"
        className="absolute right-0 top-0 h-full text-[#5C4A42] hover:text-[#C4A69D]"
      >
        <Search className="w-4 h-4" />
      </Button>
    </form>
  )
}
