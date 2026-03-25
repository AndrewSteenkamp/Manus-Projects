import { drizzle } from "drizzle-orm/mysql2";
import { products } from "../drizzle/schema.ts";

const db = drizzle(process.env.DATABASE_URL);

const seedProducts = [
  // iPhone 16 Accessories
  {
    name: "iPhone 16 Pro Max Premium Leather Case",
    description: "Genuine leather case with MagSafe compatibility. Precision-cut openings for all ports and buttons. Available in multiple colors.",
    price: "29.99",
    compareAtPrice: "49.99",
    category: "iPhone 16",
    imageUrl: "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=800",
    stockQuantity: 150,
    isActive: true,
    isFeatured: true,
    sku: "IP16-CASE-LEATHER-001",
    source1688Url: "https://detail.1688.com/offer/example1.html",
    supplierName: "Premium Tech Accessories Co.",
    source1688Price: "8.50",
    supplierConfidenceScore: 85,
    tags: JSON.stringify(["leather", "magsafe", "premium", "iphone16"])
  },
  {
    name: "iPhone 16 Tempered Glass Screen Protector (2-Pack)",
    description: "9H hardness tempered glass with oleophobic coating. Easy installation kit included. Case-friendly design.",
    price: "12.99",
    compareAtPrice: "24.99",
    category: "iPhone 16",
    imageUrl: "https://images.unsplash.com/photo-1556656793-08538906a9f8?w=800",
    stockQuantity: 300,
    isActive: true,
    isFeatured: true,
    sku: "IP16-SCREEN-GLASS-002",
    source1688Url: "https://detail.1688.com/offer/example2.html",
    supplierName: "Glass Shield Manufacturing",
    source1688Price: "2.80",
    supplierConfidenceScore: 90,
    tags: JSON.stringify(["screen protector", "tempered glass", "2-pack", "iphone16"])
  },
  {
    name: "iPhone 16 MagSafe Wireless Charger - 15W Fast Charging",
    description: "Official MagSafe compatible wireless charger with 15W fast charging. LED indicator and overheating protection.",
    price: "34.99",
    compareAtPrice: "59.99",
    category: "iPhone 16",
    imageUrl: "https://images.unsplash.com/photo-1591290619762-c588f7e4e86b?w=800",
    stockQuantity: 200,
    isActive: true,
    isFeatured: true,
    sku: "IP16-CHARGE-MAGSAFE-003",
    source1688Url: "https://detail.1688.com/offer/example3.html",
    supplierName: "FastCharge Electronics",
    source1688Price: "12.00",
    supplierConfidenceScore: 88,
    tags: JSON.stringify(["magsafe", "wireless", "fast charging", "iphone16"])
  },
  {
    name: "iPhone 16 Clear Shockproof Case with Camera Protection",
    description: "Military-grade drop protection with raised bezels for camera and screen. Crystal clear design shows off your phone.",
    price: "19.99",
    compareAtPrice: "34.99",
    category: "iPhone 16",
    imageUrl: "https://images.unsplash.com/photo-1585060544812-6b45742d762f?w=800",
    stockQuantity: 250,
    isActive: true,
    isFeatured: false,
    sku: "IP16-CASE-CLEAR-004",
    source1688Url: "https://detail.1688.com/offer/example4.html",
    supplierName: "Armor Shield Co.",
    source1688Price: "5.20",
    supplierConfidenceScore: 82,
    tags: JSON.stringify(["clear case", "shockproof", "camera protection", "iphone16"])
  },
  
  // Galaxy S25 Accessories
  {
    name: "Galaxy S25 Ultra Carbon Fiber Case",
    description: "Slim carbon fiber texture case with anti-fingerprint coating. Precise cutouts for S Pen access.",
    price: "24.99",
    compareAtPrice: "44.99",
    category: "Galaxy S25",
    imageUrl: "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800",
    stockQuantity: 180,
    isActive: true,
    isFeatured: true,
    sku: "S25-CASE-CARBON-005",
    source1688Url: "https://detail.1688.com/offer/example5.html",
    supplierName: "Carbon Tech Accessories",
    source1688Price: "7.00",
    supplierConfidenceScore: 87,
    tags: JSON.stringify(["carbon fiber", "slim", "s pen", "galaxys25"])
  },
  {
    name: "Galaxy S25 Privacy Screen Protector",
    description: "Anti-spy tempered glass keeps your screen private from side viewing angles. Full coverage edge-to-edge.",
    price: "16.99",
    compareAtPrice: "29.99",
    category: "Galaxy S25",
    imageUrl: "https://images.unsplash.com/photo-1609921212029-bb5a28e60960?w=800",
    stockQuantity: 220,
    isActive: true,
    isFeatured: true,
    sku: "S25-SCREEN-PRIVACY-006",
    source1688Url: "https://detail.1688.com/offer/example6.html",
    supplierName: "Privacy Shield Tech",
    source1688Price: "4.50",
    supplierConfidenceScore: 91,
    tags: JSON.stringify(["privacy", "screen protector", "anti-spy", "galaxys25"])
  },
  {
    name: "Galaxy S25 45W Super Fast Charger with Cable",
    description: "Official 45W PD charger with USB-C to USB-C cable. Charges S25 Ultra to 100% in under 1 hour.",
    price: "39.99",
    compareAtPrice: "69.99",
    category: "Galaxy S25",
    imageUrl: "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800",
    stockQuantity: 150,
    isActive: true,
    isFeatured: false,
    sku: "S25-CHARGE-45W-007",
    source1688Url: "https://detail.1688.com/offer/example7.html",
    supplierName: "SuperCharge Electronics",
    source1688Price: "13.50",
    supplierConfidenceScore: 86,
    tags: JSON.stringify(["45w", "fast charging", "usb-c", "galaxys25"])
  },
  {
    name: "Galaxy S25 Wallet Case with Card Holder",
    description: "Premium PU leather wallet case with 3 card slots and kickstand. RFID blocking protection included.",
    price: "27.99",
    compareAtPrice: "49.99",
    category: "Galaxy S25",
    imageUrl: "https://images.unsplash.com/photo-1591337676887-a217a6970a8a?w=800",
    stockQuantity: 160,
    isActive: true,
    isFeatured: false,
    sku: "S25-CASE-WALLET-008",
    source1688Url: "https://detail.1688.com/offer/example8.html",
    supplierName: "Wallet Case Pro",
    source1688Price: "8.00",
    supplierConfidenceScore: 84,
    tags: JSON.stringify(["wallet", "card holder", "rfid", "galaxys25"])
  },
  
  // Universal Accessories
  {
    name: "Universal Phone Ring Holder - 360° Rotation",
    description: "Strong adhesive ring holder works with all phones. Doubles as a kickstand. Compatible with magnetic car mounts.",
    price: "8.99",
    compareAtPrice: "14.99",
    category: "Universal",
    imageUrl: "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=800",
    stockQuantity: 500,
    isActive: true,
    isFeatured: false,
    sku: "UNI-RING-HOLDER-009",
    source1688Url: "https://detail.1688.com/offer/example9.html",
    supplierName: "Universal Tech Supplies",
    source1688Price: "1.80",
    supplierConfidenceScore: 80,
    tags: JSON.stringify(["ring holder", "universal", "kickstand", "magnetic"])
  },
  {
    name: "3-in-1 Wireless Charging Station",
    description: "Charge iPhone, Apple Watch, and AirPods simultaneously. Foldable design perfect for travel. 18W fast charging.",
    price: "49.99",
    compareAtPrice: "89.99",
    category: "Universal",
    imageUrl: "https://images.unsplash.com/photo-1591290619762-c588f7e4e86b?w=800",
    stockQuantity: 120,
    isActive: true,
    isFeatured: true,
    sku: "UNI-CHARGE-3IN1-010",
    source1688Url: "https://detail.1688.com/offer/example10.html",
    supplierName: "MultiCharge Solutions",
    source1688Price: "18.00",
    supplierConfidenceScore: 89,
    tags: JSON.stringify(["3-in-1", "wireless", "charging station", "foldable"])
  },
  {
    name: "USB-C to Lightning Cable - 6ft Braided",
    description: "MFi certified fast charging cable. Military-grade braided nylon for extra durability. Supports data transfer.",
    price: "14.99",
    compareAtPrice: "24.99",
    category: "Universal",
    imageUrl: "https://images.unsplash.com/photo-1591337676887-a217a6970a8a?w=800",
    stockQuantity: 400,
    isActive: true,
    isFeatured: false,
    sku: "UNI-CABLE-USBC-011",
    source1688Url: "https://detail.1688.com/offer/example11.html",
    supplierName: "Cable Masters Inc",
    source1688Price: "3.50",
    supplierConfidenceScore: 83,
    tags: JSON.stringify(["usb-c", "lightning", "braided", "mfi"])
  },
  {
    name: "Portable Power Bank 20000mAh with PD Fast Charging",
    description: "High-capacity power bank charges iPhone 16 up to 4 times. Dual USB ports + USB-C PD. LED display shows battery level.",
    price: "44.99",
    compareAtPrice: "79.99",
    category: "Universal",
    imageUrl: "https://images.unsplash.com/photo-1609592806955-e3c8e1ebd9c1?w=800",
    stockQuantity: 180,
    isActive: true,
    isFeatured: true,
    sku: "UNI-POWERBANK-20K-012",
    source1688Url: "https://detail.1688.com/offer/example12.html",
    supplierName: "PowerTech Solutions",
    source1688Price: "16.00",
    supplierConfidenceScore: 92,
    tags: JSON.stringify(["power bank", "20000mah", "pd charging", "portable"])
  }
];

async function seed() {
  console.log("🌱 Starting product seed...");
  
  try {
    for (const product of seedProducts) {
      await db.insert(products).values(product);
      console.log(`✅ Added: ${product.name}`);
    }
    
    console.log(`\n🎉 Successfully seeded ${seedProducts.length} products!`);
    process.exit(0);
  } catch (error) {
    console.error("❌ Seed failed:", error);
    process.exit(1);
  }
}

seed();
