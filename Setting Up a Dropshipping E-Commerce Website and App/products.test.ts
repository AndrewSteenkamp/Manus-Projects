import { describe, it, expect, beforeAll } from "vitest";
import { appRouter } from "./routers";
import type { Context } from "./_core/context";
import * as db from "./db";

// Mock context for testing
const createMockContext = (userId?: number): Context => ({
  user: userId ? { id: userId, openId: "test-user", name: "Test User", role: "user" } : undefined,
  req: {} as any,
  res: {} as any,
});

describe("Product Routes", () => {
  it("should list all products", async () => {
    const caller = appRouter.createCaller(createMockContext());
    const products = await caller.products.list();
    
    expect(products).toBeDefined();
    expect(Array.isArray(products)).toBe(true);
    expect(products.length).toBeGreaterThan(0);
  });

  it("should get featured products", async () => {
    const caller = appRouter.createCaller(createMockContext());
    const products = await caller.products.featured();
    
    expect(products).toBeDefined();
    expect(Array.isArray(products)).toBe(true);
    products.forEach(product => {
      expect(product.isFeatured).toBe(true);
    });
  });

  it("should get product by id", async () => {
    const caller = appRouter.createCaller(createMockContext());
    const product = await caller.products.byId({ id: 1 });
    
    expect(product).toBeDefined();
    if (product) {
      expect(product.id).toBe(1);
      expect(product.name).toBeDefined();
      expect(product.price).toBeDefined();
    }
  });

  it("should get products by category", async () => {
    const caller = appRouter.createCaller(createMockContext());
    const products = await caller.products.byCategory({ category: "iPhone 16" });
    
    expect(products).toBeDefined();
    expect(Array.isArray(products)).toBe(true);
    products.forEach(product => {
      expect(product.category).toBe("iPhone 16");
    });
  });
});

describe("Cart Routes", () => {
  const testUserId = 1;

  it("should add item to cart (authenticated)", async () => {
    const caller = appRouter.createCaller(createMockContext(testUserId));
    
    const result = await caller.cart.add({
      productId: 1,
      quantity: 2,
    });
    
    expect(result.success).toBe(true);
  });

  it("should get cart items (authenticated)", async () => {
    const caller = appRouter.createCaller(createMockContext(testUserId));
    const items = await caller.cart.items();
    
    expect(items).toBeDefined();
    expect(Array.isArray(items)).toBe(true);
  });

  it("should fail to add to cart (unauthenticated)", async () => {
    const caller = appRouter.createCaller(createMockContext());
    
    await expect(
      caller.cart.add({ productId: 1, quantity: 1 })
    ).rejects.toThrow();
  });

  it("should update cart item quantity", async () => {
    const caller = appRouter.createCaller(createMockContext(testUserId));
    
    // First add an item
    await caller.cart.add({ productId: 2, quantity: 1 });
    
    // Get the cart items to find the ID
    const items = await caller.cart.items();
    const item = items.find(i => i.product?.id === 2);
    
    if (item) {
      const result = await caller.cart.updateQuantity({
        id: item.id,
        quantity: 3,
      });
      
      expect(result.success).toBe(true);
    }
  });

  it("should remove item from cart", async () => {
    const caller = appRouter.createCaller(createMockContext(testUserId));
    
    // Add an item first
    await caller.cart.add({ productId: 3, quantity: 1 });
    
    // Get the cart items
    const items = await caller.cart.items();
    const item = items.find(i => i.product?.id === 3);
    
    if (item) {
      const result = await caller.cart.remove({ id: item.id });
      expect(result.success).toBe(true);
    }
  });

  it("should clear cart", async () => {
    const caller = appRouter.createCaller(createMockContext(testUserId));
    
    // Add some items
    await caller.cart.add({ productId: 1, quantity: 1 });
    await caller.cart.add({ productId: 2, quantity: 1 });
    
    // Clear cart
    const result = await caller.cart.clear();
    expect(result.success).toBe(true);
    
    // Verify cart is empty
    const items = await caller.cart.items();
    expect(items.length).toBe(0);
  });
});

describe("Database Functions", () => {
  it("should get all products from database", async () => {
    const products = await db.getAllProducts();
    expect(products).toBeDefined();
    expect(Array.isArray(products)).toBe(true);
  });

  it("should get featured products from database", async () => {
    const products = await db.getFeaturedProducts();
    expect(products).toBeDefined();
    expect(Array.isArray(products)).toBe(true);
    expect(products.length).toBeLessThanOrEqual(6);
  });

  it("should get product by id from database", async () => {
    const product = await db.getProductById(1);
    if (product) {
      expect(product.id).toBe(1);
      expect(product.name).toBeDefined();
    }
  });

  it("should get products by category from database", async () => {
    const products = await db.getProductsByCategory("Galaxy S25");
    expect(products).toBeDefined();
    expect(Array.isArray(products)).toBe(true);
    products.forEach(product => {
      expect(product.category).toBe("Galaxy S25");
    });
  });
});
