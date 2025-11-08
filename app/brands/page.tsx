import Image from "next/image"
import { Header } from "@/components/header"

async function getBrands() {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:5001"}/api/brands`, {
      cache: "no-store",
    })

    if (!res.ok) {
      throw new Error("Failed to fetch brands")
    }

    const data = await res.json()
    return data.brands || []
  } catch (error) {
    console.error("[v0] Error fetching brands:", error)
    return []
  }
}

export default async function BrandsPage() {
  const brandsData = await getBrands()

  const brands = brandsData.map((b: any) => ({
    name: b.brand,
    description: `Shop ${b.count} products from ${b.brand}`,
    productCount: b.count,
    image: b.image_url || `https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=800&h=600&fit=crop`,
  }))

  return (
    <>
      <Header />
      <main className="min-h-screen bg-[#F5F1ED] py-12 px-4">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-4xl md:text-5xl font-serif text-center text-[#5C4A42] mb-4">Featured Brands</h1>
          <p className="text-center text-[#6B5A52] mb-12 max-w-2xl mx-auto">
            We partner with brands that share our commitment to quality, sustainability, and inclusive design
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {brands.map((brand) => (
              <div
                key={brand.name}
                className="bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="aspect-[4/3] relative bg-[#E8DFD8]">
                  <Image src={brand.image || "/placeholder.svg"} alt={brand.name} fill className="object-cover" />
                </div>
                <div className="p-6">
                  <h3 className="text-2xl font-serif text-[#5C4A42] mb-2">{brand.name}</h3>
                  <p className="text-[#6B5A52] mb-4">{brand.description}</p>
                  <div className="flex gap-2">
                    <span className="text-xs px-3 py-1 bg-[#F9F6F3] text-[#8C7A72] rounded-full">
                      {brand.productCount} products
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </>
  )
}
