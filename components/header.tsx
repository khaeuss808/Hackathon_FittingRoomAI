"use client"

import Link from "next/link"
import { Search, Menu } from "lucide-react"
import { useState } from "react"
import { useRouter } from "next/navigation"
import Image from "next/image"

export function Header() {
  const [searchQuery, setSearchQuery] = useState("")
  const router = useRouter()

  const handleSearch = () => {
    if (searchQuery.trim()) {
      router.push(`/shop?query=${encodeURIComponent(searchQuery)}`)
    }
  }

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#F5F1ED]/95 backdrop-blur-sm border-b border-[#C4A69D]/20 h-16">
      <div className="container mx-auto h-full px-4 flex items-center justify-between">

        {/* Left: Logo */}
        <Link href="/" className="flex-shrink-0">
          <Image
            src="/logo.png"
            alt="The Fitting Room"
            width={80}
            height={40}
            className="object-contain"
            priority
          />
        </Link>

        {/* Right side group: nav + search */}
        <div className="flex items-center gap-6">
          
          {/* Nav (now LEFT of search bar) */}
          <nav className="hidden md:flex items-center gap-8">
            <Link href="/about" className="text-[#5C4A42] hover:text-[#C4A69D] transition-colors font-serif">
              About
            </Link>
            <Link href="/shop" className="text-[#5C4A42] hover:text-[#C4A69D] transition-colors font-serif">
              Shop
            </Link>
            <Link href="/brands" className="text-[#5C4A42] hover:text-[#C4A69D] transition-colors font-serif">
              Brands
            </Link>
          </nav>

          {/* Search (md+) */}
          <div className="hidden md:flex glass-search-bar items-center gap-2 px-4 py-2 rounded-full w-64">
            <Search className="w-4 h-4 text-[#C4A69D] shrink-0" />
            <input
              type="text"
              placeholder="search styles"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              className="flex-1 bg-transparent border-none outline-none text-[#5C4A42] placeholder:text-[#C4A69D]/60 text-sm font-serif"
            />
          </div>

          {/* Mobile menu button */}
          <button className="md:hidden p-2" aria-label="Open menu">
            <Menu className="w-6 h-6 text-[#5C4A42]" />
          </button>
        </div>
      </div>
    </header>
  )
}
