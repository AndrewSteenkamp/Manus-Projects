import { COOKIE_NAME } from "@shared/const";
import { getSessionCookieOptions } from "./_core/cookies";
import { systemRouter } from "./_core/systemRouter";
import { publicProcedure, router, protectedProcedure } from "./_core/trpc";
import { createPayment, getPaymentByOrderId } from "./db";
import { z } from "zod";
import {
  getAllProducts,
  getProductById,
  getProductBySlug,
  createProduct,
  updateProduct,
  deleteProduct,
  getAllCategories,
  createCategory,
  getCartItems,
  addToCart,
  updateCartItem,
  removeFromCart,
  clearCart,
  createOrder,
  createOrderItem,
  getOrdersByUser,
  getOrderById,
  getOrderItems,
  getAllOrders,
  updateOrderStatus,
  getAllSuppliers,
  createSupplier,
  updateSupplier,
} from "./db";

export const appRouter = router({
    // if you need to use socket.io, read and register route in server/_core/index.ts, all api should start with '/api/' so that the gateway can route correctly
  system: systemRouter,
  auth: router({
    me: publicProcedure.query(opts => opts.ctx.user),
    logout: publicProcedure.mutation(({ ctx }) => {
      const cookieOptions = getSessionCookieOptions(ctx.req);
      ctx.res.clearCookie(COOKIE_NAME, { ...cookieOptions, maxAge: -1 });
      return {
        success: true,
      } as const;
    }),
  }),

  // Public product procedures
  products: router({
    list: publicProcedure
      .input(z.object({
        categoryId: z.number().optional(),
        isFeatured: z.boolean().optional(),
        search: z.string().optional(),
      }).optional())
      .query(async ({ input }) => {
        return await getAllProducts({ ...input, isActive: true });
      }),
    
    getBySlug: publicProcedure
      .input(z.string())
      .query(async ({ input }) => {
        return await getProductBySlug(input);
      }),
    getByIds: publicProcedure
      .input(z.array(z.number()))
      .query(async ({ input }) => {
        if (input.length === 0) return [];
        const products = await Promise.all(input.map(id => getProductById(id)));
        return products.filter(p => p !== undefined);
      }),
    
    getById: publicProcedure
      .input(z.number())
      .query(async ({ input }) => {
        return await getProductById(input);
      }),
  }),

  // Categories
  categories: router({
    list: publicProcedure.query(async () => {
      return await getAllCategories();
    }),
  }),

  // Shopping cart procedures
  cart: router({
    get: protectedProcedure.query(async ({ ctx }) => {
      const items = await getCartItems(ctx.user.id);
      // Enrich with product details
      const enriched = await Promise.all(
        items.map(async (item) => {
          const product = await getProductById(item.productId);
          return { ...item, product };
        })
      );
      return enriched;
    }),

    add: protectedProcedure
      .input(z.object({
        productId: z.number(),
        quantity: z.number().min(1).default(1),
      }))
      .mutation(async ({ ctx, input }) => {
        return await addToCart({
          userId: ctx.user.id,
          productId: input.productId,
          quantity: input.quantity,
        });
      }),

    update: protectedProcedure
      .input(z.object({
        id: z.number(),
        quantity: z.number().min(0),
      }))
      .mutation(async ({ input }) => {
        if (input.quantity === 0) {
          await removeFromCart(input.id);
        } else {
          await updateCartItem(input.id, input.quantity);
        }
        return { success: true };
      }),

    remove: protectedProcedure
      .input(z.number())
      .mutation(async ({ input }) => {
        await removeFromCart(input);
        return { success: true };
      }),

    clear: protectedProcedure.mutation(async ({ ctx }) => {
      await clearCart(ctx.user.id);
      return { success: true };
    }),
  }),

  // Order procedures
  orders: router({
    create: protectedProcedure
      .input(z.object({
        shippingName: z.string(),
        shippingEmail: z.string().email(),
        shippingPhone: z.string().optional(),
        shippingAddress: z.string(),
        shippingCity: z.string(),
        shippingState: z.string().optional(),
        shippingZip: z.string(),
        shippingCountry: z.string(),
        notes: z.string().optional(),
      }))
      .mutation(async ({ ctx, input }) => {
        // Get cart items
        const cartItems = await getCartItems(ctx.user.id);
        if (cartItems.length === 0) {
          throw new Error("Cart is empty");
        }

        // Calculate totals
        let subtotal = 0;
        const orderItemsData = await Promise.all(
          cartItems.map(async (item) => {
            const product = await getProductById(item.productId);
            if (!product) throw new Error(`Product ${item.productId} not found`);
            const itemTotal = product.price * item.quantity;
            subtotal += itemTotal;
            return {
              productId: product.id,
              productName: product.name,
              productImage: product.imageUrl,
              quantity: item.quantity,
              price: product.price,
              total: itemTotal,
            };
          })
        );

        const shippingCost = 0; // TODO: Calculate based on location
        const tax = 0; // TODO: Calculate based on location
        const total = subtotal + shippingCost + tax;

        // Generate order number
        const orderNumber = `ORD-${Date.now()}-${Math.random().toString(36).substr(2, 9).toUpperCase()}`;

        // Create order
        const orderId = await createOrder({
          orderNumber,
          userId: ctx.user.id,
          status: "pending",
          subtotal,
          shippingCost,
          tax,
          total,
          currency: "USD",
          ...input,
        });

        // Create order items
        await Promise.all(
          orderItemsData.map((item) =>
            createOrderItem({ orderId, ...item })
          )
        );

        // Clear cart
        await clearCart(ctx.user.id);

        return { orderId, orderNumber };
      }),

    list: protectedProcedure.query(async ({ ctx }) => {
      return await getOrdersByUser(ctx.user.id);
    }),

    getById: protectedProcedure
      .input(z.number())
      .query(async ({ ctx, input }) => {
        const order = await getOrderById(input);
        if (!order || order.userId !== ctx.user.id) {
          throw new Error("Order not found");
        }
        const items = await getOrderItems(input);
        return { ...order, items };
      }),
  }),

  // Admin procedures
  admin: router({
    // Product management
    products: router({
      list: protectedProcedure
        .use(({ ctx, next }) => {
          if (ctx.user.role !== 'admin') throw new Error('Admin access required');
          return next({ ctx });
        })
        .query(async () => {
          return await getAllProducts();
        }),

      create: protectedProcedure
        .use(({ ctx, next }) => {
          if (ctx.user.role !== 'admin') throw new Error('Admin access required');
          return next({ ctx });
        })
        .input(z.object({
          name: z.string(),
          slug: z.string(),
          description: z.string().optional(),
          shortDescription: z.string().optional(),
          categoryId: z.number(),
          price: z.number(),
          compareAtPrice: z.number().optional(),
          costPrice: z.number().optional(),
          sku: z.string().optional(),
          stock: z.number().default(0),
          imageUrl: z.string().optional(),
          images: z.string().optional(),
          isFeatured: z.boolean().default(false),
          supplierId: z.number().optional(),
          supplierProductId: z.string().optional(),
          supplierUrl: z.string().optional(),
        }))
        .mutation(async ({ input }) => {
          const id = await createProduct({
            ...input,
            isActive: 1,
            isFeatured: input.isFeatured ? 1 : 0,
          });
          return { id };
        }),

      update: protectedProcedure
        .use(({ ctx, next }) => {
          if (ctx.user.role !== 'admin') throw new Error('Admin access required');
          return next({ ctx });
        })
        .input(z.object({
          id: z.number(),
          updates: z.object({
            name: z.string().optional(),
            description: z.string().optional(),
            price: z.number().optional(),
            stock: z.number().optional(),
            isActive: z.boolean().optional(),
            isFeatured: z.boolean().optional(),
          }),
        }))
        .mutation(async ({ input }) => {
          const updates: any = { ...input.updates };
          if (updates.isActive !== undefined) {
            updates.isActive = updates.isActive ? 1 : 0;
          }
          if (updates.isFeatured !== undefined) {
            updates.isFeatured = updates.isFeatured ? 1 : 0;
          }
          await updateProduct(input.id, updates);
          return { success: true };
        }),

      delete: protectedProcedure
        .use(({ ctx, next }) => {
          if (ctx.user.role !== 'admin') throw new Error('Admin access required');
          return next({ ctx });
        })
        .input(z.number())
        .mutation(async ({ input }) => {
          await deleteProduct(input);
          return { success: true };
        }),
    }),

    // Order management
    orders: router({
      list: protectedProcedure
        .use(({ ctx, next }) => {
          if (ctx.user.role !== 'admin') throw new Error('Admin access required');
          return next({ ctx });
        })
        .query(async () => {
          return await getAllOrders();
        }),

      updateStatus: protectedProcedure
        .use(({ ctx, next }) => {
          if (ctx.user.role !== 'admin') throw new Error('Admin access required');
          return next({ ctx });
        })
        .input(z.object({
          id: z.number(),
          status: z.enum(["pending", "processing", "shipped", "delivered", "cancelled"]),
          trackingNumber: z.string().optional(),
          trackingUrl: z.string().optional(),
        }))
        .mutation(async ({ input }) => {
          await updateOrderStatus(input.id, input.status, input.trackingNumber, input.trackingUrl);
          return { success: true };
        }),
    }),

    // Category management
    categories: router({
      create: protectedProcedure
        .use(({ ctx, next }) => {
          if (ctx.user.role !== 'admin') throw new Error('Admin access required');
          return next({ ctx });
        })
        .input(z.object({
          name: z.string(),
          slug: z.string(),
          description: z.string().optional(),
          imageUrl: z.string().optional(),
        }))
        .mutation(async ({ input }) => {
          const id = await createCategory(input);
          return { id };
        }),
    }),

    // Supplier management
    suppliers: router({
      list: protectedProcedure
        .use(({ ctx, next }) => {
          if (ctx.user.role !== 'admin') throw new Error('Admin access required');
          return next({ ctx });
        })
        .query(async () => {
          return await getAllSuppliers();
        }),

      create: protectedProcedure
        .use(({ ctx, next }) => {
          if (ctx.user.role !== 'admin') throw new Error('Admin access required');
          return next({ ctx });
        })
        .input(z.object({
          name: z.string(),
          contactName: z.string().optional(),
          email: z.string().optional(),
          phone: z.string().optional(),
          website: z.string().optional(),
          apiKey: z.string().optional(),
          apiEndpoint: z.string().optional(),
        }))
        .mutation(async ({ input }) => {
          const id = await createSupplier(input);
          return { id };
        }),

      update: protectedProcedure
        .use(({ ctx, next }) => {
          if (ctx.user.role !== 'admin') throw new Error('Admin access required');
          return next({ ctx });
        })
        .input(z.object({
          id: z.number(),
          updates: z.object({
            name: z.string().optional(),
            contactName: z.string().optional(),
            email: z.string().optional(),
            phone: z.string().optional(),
            website: z.string().optional(),
            apiKey: z.string().optional(),
            apiEndpoint: z.string().optional(),
            isActive: z.boolean().optional(),
          }),
        }))
        .mutation(async ({ input }) => {
          const updates: any = { ...input.updates };
          if (updates.isActive !== undefined) {
            updates.isActive = updates.isActive ? 1 : 0;
          }
          await updateSupplier(input.id, updates);
          return { success: true };
        }),
    }),
  }),

  // Payment procedures
  payment: router({
    createPayment: protectedProcedure
      .input(z.object({
        orderId: z.number(),
        processor: z.enum(['stripe', 'payfast', 'paystack', 'paypal']),
        amount: z.number(),
        currency: z.string().default('USD'),
      }))
      .mutation(async ({ input, ctx }) => {
        const payment = await createPayment({
          orderId: input.orderId,
          processor: input.processor,
          amount: input.amount.toString(),
          currency: input.currency,
          status: 'pending',
          customerEmail: ctx.user.email || '',
          customerName: ctx.user.name || '',
        });
        return { paymentId: payment };
      }),
    
    getPaymentByOrderId: protectedProcedure
      .input(z.object({ orderId: z.number() }))
      .query(async ({ input }) => {
        return await getPaymentByOrderId(input.orderId);
      }),
  }),
});

export type AppRouter = typeof appRouter;
