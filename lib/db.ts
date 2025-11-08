import Database from "better-sqlite3"
import path from "path"

// Use the fittingroom.db from the backend data folder
const DB_PATH = process.env.DATABASE_PATH || path.join(process.cwd(), "..", "backend", "data", "fittingroom.db")

let db: Database.Database | null = null

export function getDatabase() {
  if (!db) {
    try {
      db = new Database(DB_PATH, { readonly: false })
      db.pragma("journal_mode = WAL")
      console.log("[v0] Database connected:", DB_PATH)
    } catch (error) {
      console.error("[v0] Database connection error:", error)
      throw error
    }
  }
  return db
}

export interface Product {
  id: number
  source?: string
  reference?: string
  name: string
  brand: string
  price: number
  price_cents?: number
  currency?: string
  image_url?: string
  product_url?: string
  sizes?: string
  colors?: string
  color?: string
  styles?: string
  category?: string
  description?: string
  raw?: string
  scraped_at?: string
  created_at?: string
}

export interface SearchParams {
  styles?: string[]
  min_price?: number
  max_price?: number
  sizes?: string[]
  brands?: string[]
  page?: number
  limit?: number
}

export function searchProducts(params: SearchParams): { results: Product[]; total: number } {
  const db = getDatabase()

  const { styles = [], min_price, max_price, sizes = [], brands = [], page = 1, limit = 20 } = params

  let query = "SELECT * FROM products WHERE 1=1"
  const queryParams: any[] = []

  if (styles.length > 0) {
    const styleConditions = styles
      .map(() => "(styles LIKE ? OR name LIKE ? OR description LIKE ? OR category LIKE ?)")
      .join(" OR ")
    query += " AND (" + styleConditions + ")"
    styles.forEach((keyword) => {
      const pattern = "%" + keyword + "%"
      queryParams.push(pattern, pattern, pattern, pattern)
    })
  }

  if (min_price !== undefined) {
    query += " AND price >= ?"
    queryParams.push(min_price)
  }

  if (max_price !== undefined) {
    query += " AND price <= ?"
    queryParams.push(max_price)
  }

  if (sizes.length > 0) {
    const sizeConditions = sizes.map(() => "sizes LIKE ?").join(" OR ")
    query += " AND (" + sizeConditions + ")"
    sizes.forEach((size) => queryParams.push("%" + size + "%"))
  }

  if (brands.length > 0) {
    const brandConditions = brands.map(() => "brand LIKE ?").join(" OR ")
    query += " AND (" + brandConditions + ")"
    brands.forEach((brand) => queryParams.push("%" + brand + "%"))
  }

  // Get total count
  const countQuery = query.replace("SELECT *", "SELECT COUNT(*) as count")
  const countResult = db.prepare(countQuery).get(...queryParams) as { count: number }
  const total = countResult.count

  // Add pagination
  query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
  const offset = (page - 1) * limit
  queryParams.push(limit, offset)

  const results = db.prepare(query).all(...queryParams) as Product[]

  return { results, total }
}

export function getAllBrands(): { brand: string; count: number; image_url?: string }[] {
  const db = getDatabase()

  const query = `
    SELECT 
      brand, 
      COUNT(*) as count,
      (SELECT image_url FROM products p2 WHERE p2.brand = products.brand AND image_url IS NOT NULL LIMIT 1) as image_url
    FROM products 
    GROUP BY brand 
    ORDER BY count DESC
  `

  return db.prepare(query).all() as { brand: string; count: number; image_url?: string }[]
}

export function getProductById(id: number): Product | undefined {
  const db = getDatabase()
  return db.prepare("SELECT * FROM products WHERE id = ?").get(id) as Product | undefined
}
