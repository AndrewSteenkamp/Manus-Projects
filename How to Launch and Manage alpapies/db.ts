import { eq, desc } from "drizzle-orm";
import { drizzle } from "drizzle-orm/mysql2";
import { 
  InsertUser, 
  users, 
  payments, 
  InsertPayment,
  products, 
  InsertProduct, 
  categories, 
  InsertCategory, 
  cartItems, 
  InsertCartItem, 
  orders, 
  InsertOrder, 
  orderItems, 
  InsertOrderItem, 
  suppliers, 
  InsertSupplier 
} from "../drizzle/schema";
import { ENV } from './_core/env';

let _db: ReturnType<typeof drizzle> | null = null;

// Lazily create the drizzle instance so local tooling can run without a DB.
export async function getDb() {
  if (!_db && process.env.DATABASE_URL) {
    try {
      _db = drizzle(process.env.DATABASE_URL);
    } catch (error) {
      console.warn("[Database] Failed to connect:", error);
      _db = null;
    }
  }
  return _db;
}

export async function upsertUser(user: InsertUser): Promise<void> {
  if (!user.openId) {
    throw new Error("User openId is required for upsert");
  }

  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot upsert user: database not available");
    return;
  }

  try {
    const values: InsertUser = {
      openId: user.openId,
    };
    const updateSet: Record<string, unknown> = {};

    const textFields = ["name", "email", "loginMethod"] as const;
    type TextField = (typeof textFields)[number];

    const assignNullable = (field: TextField) => {
      const value = user[field];
      if (value === undefined) return;
      const normalized = value ?? null;
      values[field] = normalized;
      updateSet[field] = normalized;
    };

    textFields.forEach(assignNullable);

    if (user.lastSignedIn !== undefined) {
      values.lastSignedIn = user.lastSignedIn;
      updateSet.lastSignedIn = user.lastSignedIn;
    }
    if (user.role !== undefined) {
      values.role = user.role;
      updateSet.role = user.role;
    } else if (user.openId === ENV.ownerOpenId) {
      values.role = 'admin';
      updateSet.role = 'admin';
    }

    if (!values.lastSignedIn) {
      values.lastSignedIn = new Date();
    }

    if (Object.keys(updateSet).length === 0) {
      updateSet.lastSignedIn = new Date();
    }

    await db.insert(users).values(values).onDuplicateKeyUpdate({
      set: updateSet,
    });
  } catch (error) {
    console.error("[Database] Failed to upsert user:", error);
    throw error;
  }
}

export async function getUserByOpenId(openId: string) {
  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot get user: database not available");
    return undefined;
  }

  const result = await db.select().from(users).where(eq(users.openId, openId)).limit(1);

  return result.length > 0 ? result[0] : undefined;
}

// Product queries
export async function getAllProducts(filters?: { categoryId?: number; isFeatured?: boolean; isActive?: boolean; search?: string }) {
  const db = await getDb();
  if (!db) return [];

  let query = db.select().from(products).$dynamic();

  if (filters?.categoryId) {
    query = query.where(eq(products.categoryId, filters.categoryId));
  }
  if (filters?.isFeatured !== undefined) {
    query = query.where(eq(products.isFeatured, filters.isFeatured ? 1 : 0));
  }
  if (filters?.isActive !== undefined) {
    query = query.where(eq(products.isActive, filters.isActive ? 1 : 0));
  }

  return await query;
}

export async function getProductById(id: number) {
  const db = await getDb();
  if (!db) return undefined;

  const result = await db.select().from(products).where(eq(products.id, id)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

export async function getProductBySlug(slug: string) {
  const db = await getDb();
  if (!db) return undefined;

  const result = await db.select().from(products).where(eq(products.slug, slug)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

export async function createProduct(product: InsertProduct) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db.insert(products).values(product);
  // Return the product to get its ID after insertion
  const inserted = await db.select().from(products).where(eq(products.slug, product.slug)).limit(1);
  return inserted[0]?.id || 0;
}

export async function updateProduct(id: number, updates: Partial<InsertProduct>) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db.update(products).set(updates).where(eq(products.id, id));
}

export async function deleteProduct(id: number) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db.delete(products).where(eq(products.id, id));
}

// Category queries
export async function getAllCategories() {
  const db = await getDb();
  if (!db) return [];

  return await db.select().from(categories);
}

export async function getCategoryById(id: number) {
  const db = await getDb();
  if (!db) return undefined;

  const result = await db.select().from(categories).where(eq(categories.id, id)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

export async function createCategory(category: InsertCategory) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db.insert(categories).values(category);
  const inserted = await db.select().from(categories).where(eq(categories.slug, category.slug)).limit(1);
  return inserted[0]?.id || 0;
}

// Cart queries
export async function getCartItems(userId: number) {
  const db = await getDb();
  if (!db) return [];

  return await db.select().from(cartItems).where(eq(cartItems.userId, userId));
}

export async function addToCart(item: InsertCartItem) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  // Check if item already exists in cart
  const existing = await db
    .select()
    .from(cartItems)
    .where(eq(cartItems.userId, item.userId))
    .limit(1);
  
  const existingItem = existing.find(e => e.productId === item.productId);

  if (existingItem) {
    // Update quantity
    await db
      .update(cartItems)
      .set({ quantity: existingItem.quantity + (item.quantity || 1) })
      .where(eq(cartItems.id, existingItem.id));
    return existingItem.id;
  } else {
    // Insert new item
    await db.insert(cartItems).values(item);
    const allItems = await db.select().from(cartItems).where(eq(cartItems.userId, item.userId));
    const inserted = allItems.find(i => i.productId === item.productId);
    return inserted?.id || 0;
  }
}

export async function updateCartItem(id: number, quantity: number) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db.update(cartItems).set({ quantity }).where(eq(cartItems.id, id));
}

export async function removeFromCart(id: number) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db.delete(cartItems).where(eq(cartItems.id, id));
}

export async function clearCart(userId: number) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db.delete(cartItems).where(eq(cartItems.userId, userId));
}

// Order queries
export async function createOrder(order: InsertOrder) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db.insert(orders).values(order);
  const inserted = await db.select().from(orders).where(eq(orders.orderNumber, order.orderNumber)).limit(1);
  return inserted[0]?.id || 0;
}

export async function createOrderItem(item: InsertOrderItem) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db.insert(orderItems).values(item);
  return 0; // Order items don't need to return ID
}

export async function getOrdersByUser(userId: number) {
  const db = await getDb();
  if (!db) return [];

  return await db.select().from(orders).where(eq(orders.userId, userId));
}

export async function getOrderById(id: number) {
  const db = await getDb();
  if (!db) return undefined;

  const result = await db.select().from(orders).where(eq(orders.id, id)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

export async function getOrderItems(orderId: number) {
  const db = await getDb();
  if (!db) return [];

  return await db.select().from(orderItems).where(eq(orderItems.orderId, orderId));
}

export async function getAllOrders() {
  const db = await getDb();
  if (!db) return [];

  return await db.select().from(orders);
}

export async function updateOrderStatus(id: number, status: string, trackingNumber?: string, trackingUrl?: string) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const updates: any = { status };
  if (trackingNumber) updates.trackingNumber = trackingNumber;
  if (trackingUrl) updates.trackingUrl = trackingUrl;

  await db.update(orders).set(updates).where(eq(orders.id, id));
}

// Supplier queries
export async function getAllSuppliers() {
  const db = await getDb();
  if (!db) return [];

  return await db.select().from(suppliers);
}

export async function getSupplierById(id: number) {
  const db = await getDb();
  if (!db) return undefined;

  const result = await db.select().from(suppliers).where(eq(suppliers.id, id)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

export async function createSupplier(supplier: InsertSupplier) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db.insert(suppliers).values(supplier);
  const inserted = await db.select().from(suppliers).where(eq(suppliers.name, supplier.name)).limit(1);
  return inserted[0]?.id || 0;
}

export async function updateSupplier(id: number, updates: Partial<InsertSupplier>) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db.update(suppliers).set(updates).where(eq(suppliers.id, id));
}

// Payment operations
export async function createPayment(payment: InsertPayment) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  
  await db.insert(payments).values(payment);
  const inserted = await db.select().from(payments)
    .where(eq(payments.orderId, payment.orderId))
    .orderBy(desc(payments.createdAt))
    .limit(1);
  return inserted[0]?.id || 0;
}

export async function getPaymentByOrderId(orderId: number) {
  const db = await getDb();
  if (!db) return undefined;
  
  const result = await db.select().from(payments).where(eq(payments.orderId, orderId)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

export async function updatePaymentStatus(
  paymentId: number,
  status: 'pending' | 'completed' | 'failed' | 'cancelled' | 'refunded',
  processorPaymentId?: string
) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  
  const updateData: any = { status };
  if (processorPaymentId) {
    updateData.processorPaymentId = processorPaymentId;
  }
  if (status === 'completed') {
    updateData.completedAt = new Date();
  }
  
  await db.update(payments).set(updateData).where(eq(payments.id, paymentId));
}
