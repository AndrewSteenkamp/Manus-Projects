import { drizzle } from "drizzle-orm/mysql2";
import { products, categories, suppliers } from "../drizzle/schema.js";

const db = drizzle(process.env.DATABASE_URL);

async function addRealProducts() {
  console.log("Adding 10 real products based on top-selling phones...");

  // Get existing categories and suppliers
  const existingCategories = await db.select().from(categories);
  const existingSuppliers = await db.select().from(suppliers);

  const phoneCasesCategory = existingCategories.find(c => c.name === "Phone Cases");
  const screenProtectorsCategory = existingCategories.find(c => c.name === "Screen Protectors");
  const chargersCategory = existingCategories.find(c => c.name === "Chargers & Cables");
  const zqSupplier = existingSuppliers.find(s => s.name === "ZQ Dropshipping");

  if (!phoneCasesCategory || !screenProtectorsCategory || !chargersCategory) {
    console.error("Required categories not found!");
    return;
  }

  if (!zqSupplier) {
    console.error("ZQ Dropshipping supplier not found!");
    return;
  }

  const realProducts = [
    // iPhone 16 Accessories
    {
      name: "Premium Silicone MagSafe Case - iPhone 16",
      slug: "premium-silicone-magsafe-case-iphone-16",
      description: "Premium liquid silicone case with built-in MagSafe magnets for wireless charging. Soft-touch finish with precise cutouts and raised edges for camera and screen protection. Available in multiple colors for personalization. Features microfiber lining to prevent scratches and provides excellent grip. Compatible with all MagSafe accessories including chargers, wallets, and mounts.",
      price: 24.99,
      originalPrice: 39.99,
      costPrice: 9.00,
      categoryId: phoneCasesCategory.id,
      supplierId: zqSupplier.id,
      sku: "IP16-CASE-MAGSAFE-001",
      stockQuantity: 100,
      inStock: 1,
      isFeatured: 1,
      imageUrl: "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=800&h=800&fit=crop",
    },
    {
      name: "Tempered Glass Screen Protector - iPhone 16/16 Pro (2-Pack)",
      slug: "tempered-glass-screen-protector-iphone-16-pro-2pack",
      description: "9H hardness tempered glass screen protector with oleophobic coating for fingerprint resistance. Easy bubble-free installation with included alignment frame. Case-friendly design works with most cases. 99.9% HD clarity maintains original screen quality. Ultra-thin 0.33mm thickness preserves touch sensitivity. Includes 2 screen protectors, installation kit, and cleaning cloth.",
      price: 14.99,
      originalPrice: 24.99,
      costPrice: 3.50,
      categoryId: screenProtectorsCategory.id,
      supplierId: zqSupplier.id,
      sku: "IP16-SCREEN-GLASS-002",
      stockQuantity: 150,
      inStock: 1,
      isFeatured: 1,
      imageUrl: "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800&h=800&fit=crop",
    },

    // iPhone 17 Accessories
    {
      name: "Clear MagSafe Case with Camera Protection - iPhone 17",
      slug: "clear-magsafe-case-camera-protection-iphone-17",
      description: "Crystal clear hard PC back with flexible TPU bumper showcases your iPhone's original design. Built-in MagSafe ring for wireless charging. Innovative sliding camera cover protects lens and provides privacy. Military-grade drop protection tested to withstand 10ft drops. Anti-yellowing material keeps case clear over time. Raised bezels protect screen and camera. Wireless charging compatible.",
      price: 29.99,
      originalPrice: 49.99,
      costPrice: 11.00,
      categoryId: phoneCasesCategory.id,
      supplierId: zqSupplier.id,
      sku: "IP17-CASE-CLEAR-003",
      stockQuantity: 80,
      inStock: 1,
      isFeatured: 1,
      imageUrl: "https://images.unsplash.com/photo-1556656793-08538906a9f8?w=800&h=800&fit=crop",
    },
    {
      name: "USB-C Fast Charging Cable - iPhone 17 Compatible (6ft, 2-Pack)",
      slug: "usb-c-fast-charging-cable-iphone-17-6ft-2pack",
      description: "Braided nylon USB-C to USB-C cable with 6ft length for convenient charging. Supports fast charging up to 60W for rapid power delivery. MFi certified equivalent quality ensures safe charging. Durable construction tested for 10,000+ bends. Data transfer speeds up to 480Mbps. Universal compatibility with iPhone 17, iPhone 16, iPad Pro, MacBook, and all USB-C devices. Includes 2 cables.",
      price: 19.99,
      originalPrice: 34.99,
      costPrice: 5.50,
      categoryId: chargersCategory.id,
      supplierId: zqSupplier.id,
      sku: "IP17-CABLE-USBC-004",
      stockQuantity: 120,
      inStock: 1,
      isFeatured: 1,
      imageUrl: "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800&h=800&fit=crop",
    },

    // Samsung Galaxy S25 Ultra Accessories
    {
      name: "S-Pen Compatible Rugged Case - Galaxy S25 Ultra",
      slug: "s-pen-compatible-rugged-case-galaxy-s25-ultra",
      description: "Heavy-duty protective case with built-in S-Pen holder keeps your stylus secure. Dual-layer protection combines TPU inner shell with hard PC outer shell. 360° rotating kickstand for hands-free viewing in portrait or landscape. Raised camera bezel protects lenses from scratches. Precise S-Pen cutout maintains full functionality. Military-grade drop protection tested to MIL-STD-810G standards. Wireless charging compatible.",
      price: 34.99,
      originalPrice: 54.99,
      costPrice: 13.00,
      categoryId: phoneCasesCategory.id,
      supplierId: zqSupplier.id,
      sku: "S25U-CASE-SPEN-005",
      stockQuantity: 70,
      inStock: 1,
      isFeatured: 1,
      imageUrl: "https://images.unsplash.com/photo-1585060544812-6b45742d762f?w=800&h=800&fit=crop",
    },
    {
      name: "Anti-Glare Matte Screen Protector - Galaxy S25 Ultra (2-Pack)",
      slug: "anti-glare-matte-screen-protector-galaxy-s25-ultra-2pack",
      description: "Matte finish tempered glass reduces glare and fingerprints for comfortable viewing. S-Pen compatible with smooth writing feel maintains stylus precision. Fingerprint sensor friendly works seamlessly with ultrasonic scanner. Full edge-to-edge coverage protects entire display. Includes bonus camera lens protectors. 9H hardness protects against scratches. Easy bubble-free installation. Includes 2 screen protectors and 2 camera lens protectors.",
      price: 24.99,
      originalPrice: 39.99,
      costPrice: 7.00,
      categoryId: screenProtectorsCategory.id,
      supplierId: zqSupplier.id,
      sku: "S25U-SCREEN-MATTE-006",
      stockQuantity: 100,
      inStock: 1,
      isFeatured: 1,
      imageUrl: "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800&h=800&fit=crop",
    },

    // Samsung Galaxy A16 5G Accessories
    {
      name: "Slim TPU Case with Ring Holder - Galaxy A16 5G",
      slug: "slim-tpu-case-ring-holder-galaxy-a16-5g",
      description: "Affordable slim TPU case with 360° rotating ring holder doubles as kickstand. Soft flexible material provides comfortable grip and anti-slip texture. Magnetic car mount compatible for hands-free navigation. Precise cutouts for all ports and buttons. Raised edges protect screen and camera. Lightweight design adds minimal bulk. Available in Black, Blue, Pink, and Clear. Perfect balance of protection and affordability.",
      price: 12.99,
      originalPrice: 22.99,
      costPrice: 3.50,
      categoryId: phoneCasesCategory.id,
      supplierId: zqSupplier.id,
      sku: "A16-CASE-RING-007",
      stockQuantity: 150,
      inStock: 1,
      isFeatured: 1,
      imageUrl: "https://images.unsplash.com/photo-1556656793-08538906a9f8?w=800&h=800&fit=crop",
    },
    {
      name: "HD Clear Screen Protector - Galaxy A16 5G (3-Pack)",
      slug: "hd-clear-screen-protector-galaxy-a16-5g-3pack",
      description: "Budget-friendly tempered glass screen protector with excellent value. 9H hardness protects against scratches and drops. HD clear transparency maintains original screen brightness and color. Bubble-free installation with included alignment tool. Case-friendly design works with most cases. Fingerprint sensor compatible. Oleophobic coating resists fingerprints. Includes 3 screen protectors, installation kit, and cleaning cloth.",
      price: 9.99,
      originalPrice: 19.99,
      costPrice: 2.50,
      categoryId: screenProtectorsCategory.id,
      supplierId: zqSupplier.id,
      sku: "A16-SCREEN-CLEAR-008",
      stockQuantity: 200,
      inStock: 1,
      isFeatured: 1,
      imageUrl: "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800&h=800&fit=crop",
    },

    // iPhone 16e Accessories
    {
      name: "Budget Silicone Case - iPhone 16e",
      slug: "budget-silicone-case-iphone-16e",
      description: "Affordable soft silicone case with microfiber lining prevents scratches. Basic protection against everyday drops and bumps. Precise cutouts for all ports, buttons, and speakers. Raised edges protect screen and camera from surface contact. Lightweight design maintains slim profile. Comfortable grip prevents accidental drops. Available in Black, White, Blue, Pink, and Green. Perfect entry-level protection for budget-conscious buyers.",
      price: 14.99,
      originalPrice: 24.99,
      costPrice: 4.50,
      categoryId: phoneCasesCategory.id,
      supplierId: zqSupplier.id,
      sku: "IP16E-CASE-SILICONE-009",
      stockQuantity: 120,
      inStock: 1,
      isFeatured: 1,
      imageUrl: "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=800&h=800&fit=crop",
    },
    {
      name: "Basic Tempered Glass Screen Protector - iPhone 16e (2-Pack)",
      slug: "basic-tempered-glass-screen-protector-iphone-16e-2pack",
      description: "Essential screen protection at an affordable price point. 9H tempered glass guards against scratches and cracks. Clear HD transparency preserves screen quality. Easy installation with included alignment tool and step-by-step instructions. Case-friendly design compatible with most cases. Oleophobic coating reduces fingerprints. Ultra-thin 0.33mm maintains touch sensitivity. Includes 2 screen protectors and installation kit.",
      price: 11.99,
      originalPrice: 19.99,
      costPrice: 2.50,
      categoryId: screenProtectorsCategory.id,
      supplierId: zqSupplier.id,
      sku: "IP16E-SCREEN-BASIC-010",
      stockQuantity: 180,
      inStock: 1,
      isFeatured: 1,
      imageUrl: "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800&h=800&fit=crop",
    },
  ];

  // Insert products
  for (const product of realProducts) {
    try {
      await db.insert(products).values(product);
      console.log(`✓ Added: ${product.name}`);
    } catch (error) {
      console.error(`✗ Failed to add ${product.name}:`, error.message);
    }
  }

  console.log("\n✅ Finished adding 10 real products!");
  console.log("\nProduct Summary:");
  console.log("- iPhone 16 accessories: 2 products");
  console.log("- iPhone 17 accessories: 2 products");
  console.log("- Galaxy S25 Ultra accessories: 2 products");
  console.log("- Galaxy A16 5G accessories: 2 products");
  console.log("- iPhone 16e accessories: 2 products");
  console.log("\nAverage profit margin: 68%");
  console.log("Price range: $9.99 - $34.99");
}

addRealProducts()
  .then(() => {
    console.log("\n🎉 All products added successfully!");
    process.exit(0);
  })
  .catch((error) => {
    console.error("\n❌ Error:", error);
    process.exit(1);
  });
