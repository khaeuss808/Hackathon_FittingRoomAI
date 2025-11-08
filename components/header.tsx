import Link from "next/link"
import { Menu } from "lucide-react"
import Image from "next/image"

export function Header() {
  return (
    <header className="bg-[#F5F1ED] border-b border-[#E8DFD8] px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <Link href="/" className="flex items-center">
          <div className="relative w-48 h-12">
            <Image src="/logo.jpg" alt="The Fitting Room" fill className="object-contain" />
          </div>
        </Link>

        <nav className="hidden md:flex items-center gap-8">
          <Link href="/about" className="text-[#5C4A42] hover:text-[#C4A69D] transition-colors">
            About
          </Link>
          <Link href="/brands" className="text-[#5C4A42] hover:text-[#C4A69D] transition-colors">
            Brands
          </Link>
          <Link href="/shop" className="text-[#5C4A42] hover:text-[#C4A69D] transition-colors">
            Shop
          </Link>
        </nav>

        <button className="md:hidden text-[#5C4A42]">
          <Menu className="w-6 h-6" />
        </button>
      </div>
    </header>
  )
}
