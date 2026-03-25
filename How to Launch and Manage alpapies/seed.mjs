import { drizzle } from "drizzle-orm/mysql2";
import { categories, products, suppliers } from "../drizzle/schema.js";

const db = drizzle(process.env.DATABASE_URL);

async function seed() {
  console.log("🌱 Seeding database...");

  // Create categories
  console.log("Creating categories...");
  await db.insert(categories).values([
    {
      name: "Phone Cases",
      slug: "phone-cases",
      description: "Protective and stylish cases for all phone models",
      imageUrl: "https://placehold.co/200x200/3B82F6/FFFFFF?text=Cases",
    },
    {
      name: "Screen Protectors",
      slug: "screen-protectors",
      description: "Premium tempered glass and film protectors",
      imageUrl: "https://placehold.co/200x200/3B82F6/FFFFFF?text=Screen",
    },
    {
      name: "Chargers & Cables",
      slug: "chargers-cables",
      description: "Fast charging solutions and durable cables",
      imageUrl: "https://placehold.co/200x200/3B82F6/FFFFFF?text=Chargers",
    },
    {
      name: "Wireless Accessories",
      slug: "wireless-accessories",
      description: "Bluetooth earbuds, speakers, and more",
      imageUrl: "https://placehold.co/200x200/3B82F6/FFFFFF?text=Wireless",
    },
  ]);

  // Create supplier
  console.log("Creating supplier...");
  await db.insert(suppliers).values({
    name: "ZQ Dropshipping",
    website: "https://www.zqdropshipping.com",
    email: "support@zqdropshipping.com",
    notes: "Primary supplier sourcing from 1688.com with worldwide shipping",
    isActive: 1,
  });

  // Get category IDs
  const categoriesData = await db.select().from(categories);
  const phoneCasesId = categoriesData.find(c => c.slug === "phone-cases")?.id || 1;
  const screenProtectorsId = categoriesData.find(c => c.slug === "screen-protectors")?.id || 2;
  const chargersId = categoriesData.find(c => c.slug === "chargers-cables")?.id || 3;
  const wirelessId = categoriesData.find(c => c.slug === "wireless-accessories")?.id || 4;

  // Get supplier ID
  const suppliersData = await db.select().from(suppliers);
  const supplierId = suppliersData[0]?.id || 1;

  // Create products
  console.log("Creating products...");
  await db.insert(products).values([
    // Phone Cases
    {
      name: "Premium Leather Wallet Case - iPhone 15 Pro",
      slug: "premium-leather-wallet-case-iphone-15-pro",
      description: "Genuine leather wallet case with card slots and kickstand. Premium quality with RFID protection.",
      shortDescription: "Genuine leather with card slots and RFID protection",
      categoryId: phoneCasesId,
      price: 2499, // $24.99
      compareAtPrice: 3999,
      costPrice: 1200,
      sku: "LC-IP15P-BLK",
      stock: 150,
      imageUrl: "https://placehold.co/600x600/3B82F6/FFFFFF?text=Leather+Case",
      isActive: 1,
      isFeatured: 1,
      supplierId,
      supplierProductId: "1688-LC-001",
    },
    {
      name: "Shockproof Armor Case - Samsung Galaxy S24",
      slug: "shockproof-armor-case-samsung-s24",
      description: "Military-grade drop protection with reinforced corners. Slim profile with raised edges for screen protection.",
      shortDescription: "Military-grade protection, slim design",
      categoryId: phoneCasesId,
      price: 1899,
      compareAtPrice: 2999,
      costPrice: 800,
      sku: "AC-S24-BLK",
      stock: 200,
      imageUrl: "https://placehold.co/600x600/3B82F6/FFFFFF?text=Armor+Case",
      isActive: 1,
      isFeatured: 1,
      supplierId,
      supplierProductId: "1688-AC-002",
    },
    {
      name: "Clear Crystal Case - iPhone 15",
      slug: "clear-crystal-case-iphone-15",
      description: "Ultra-clear TPU case that showcases your phone's original design. Anti-yellowing technology.",
      shortDescription: "Crystal clear, anti-yellowing TPU",
      categoryId: phoneCasesId,
      price: 1299,
      compareAtPrice: 1999,
      costPrice: 500,
      sku: "CC-IP15-CLR",
      stock: 300,
      imageUrl: "https://placehold.co/600x600/3B82F6/FFFFFF?text=Clear+Case",
      isActive: 1,
      isFeatured: 0,
      supplierId,
      supplierProductId: "1688-CC-003",
    },

    // Screen Protectors
    {
      name: "Tempered Glass Screen Protector - iPhone 15 Pro Max",
      slug: "tempered-glass-screen-protector-iphone-15-pro-max",
      description: "9H hardness tempered glass with oleophobic coating. Easy bubble-free installation. 2-pack included.",
      shortDescription: "9H hardness, 2-pack, bubble-free",
      categoryId: screenProtectorsId,
      price: 1499,
      compareAtPrice: 2499,
      costPrice: 600,
      sku: "TG-IP15PM-2PK",
      stock: 500,
      imageUrl: "https://placehold.co/600x600/3B82F6/FFFFFF?text=Screen+Protector",
      isActive: 1,
      isFeatured: 1,
      supplierId,
      supplierProductId: "1688-TG-004",
    },
    {
      name: "Privacy Screen Protector - Samsung Galaxy S24 Ultra",
      slug: "privacy-screen-protector-samsung-s24-ultra",
      description: "Anti-spy tempered glass that darkens screen from side angles. Protects your privacy in public.",
      shortDescription: "Anti-spy, 9H hardness, privacy protection",
      categoryId: screenProtectorsId,
      price: 1999,
      compareAtPrice: 3499,
      costPrice: 900,
      sku: "PS-S24U-BLK",
      stock: 250,
      imageUrl: "https://placehold.co/600x600/3B82F6/FFFFFF?text=Privacy+Screen",
      isActive: 1,
      isFeatured: 1,
      supplierId,
      supplierProductId: "1688-PS-005",
    },

    // Chargers & Cables
    {
      name: "65W GaN Fast Charger - USB-C PD",
      slug: "65w-gan-fast-charger-usb-c-pd",
      description: "Compact GaN technology charger with 65W power delivery. Charges laptops, tablets, and phones. Foldable plug.",
      shortDescription: "65W GaN, compact, universal charging",
      categoryId: chargersId,
      price: 3499,
      compareAtPrice: 5999,
      costPrice: 1500,
      sku: "CH-GAN65-WHT",
      stock: 180,
      imageUrl: "https://placehold.co/600x600/3B82F6/FFFFFF?text=GaN+Charger",
      isActive: 1,
      isFeatured: 1,
      supplierId,
      supplierProductId: "1688-CH-006",
    },
    {
      name: "Braided USB-C to Lightning Cable - 6ft",
      slug: "braided-usb-c-lightning-cable-6ft",
      description: "MFi certified braided cable with reinforced connectors. Supports fast charging up to 20W. 2-pack.",
      shortDescription: "MFi certified, braided, 2-pack",
      categoryId: chargersId,
      price: 1799,
      compareAtPrice: 2999,
      costPrice: 700,
      sku: "CB-USBC-LT-6FT",
      stock: 400,
      imageUrl: "https://placehold.co/600x600/3B82F6/FFFFFF?text=Cable",
      isActive: 1,
      isFeatured: 0,
      supplierId,
      supplierProductId: "1688-CB-007",
    },

    // Wireless Accessories
    {
      name: "True Wireless Earbuds Pro - ANC",
      slug: "true-wireless-earbuds-pro-anc",
      description: "Active noise cancellation with 30-hour battery life. IPX7 waterproof. Premium sound quality with deep bass.",
      shortDescription: "ANC, 30hr battery, IPX7 waterproof",
      categoryId: wirelessId,
      price: 5999,
      compareAtPrice: 9999,
      costPrice: 2500,
      sku: "TWE-PRO-BLK",
      stock: 120,
      imageUrl: "https://placehold.co/600x600/3B82F6/FFFFFF?text=Earbuds",
      isActive: 1,
      isFeatured: 1,
      supplierId,
      supplierProductId: "1688-TWE-008",
    },
    {
      name: "15W Wireless Charging Pad",
      slug: "15w-wireless-charging-pad",
      description: "Fast 15W wireless charging for compatible devices. LED indicator and non-slip surface. Includes USB-C cable.",
      shortDescription: "15W fast charging, LED indicator",
      categoryId: wirelessId,
      price: 2499,
      compareAtPrice: 3999,
      costPrice: 1000,
      sku: "WC-PAD-15W",
      stock: 220,
      imageUrl: "https://placehold.co/600x600/3B82F6/FFFFFF?text=Wireless+Pad",
      isActive: 1,
      isFeatured: 0,
      supplierId,
      supplierProductId: "1688-WC-009",
    },
  ]);

  console.log("✅ Database seeded successfully!");
  process.exit(0);
}

seed().catch((error) => {
  console.error("❌ Seeding failed:", error);
  process.exit(1);
});
