  id: int("id").autoincrement().primaryKey(),
  title: varchar("title", { length: 255 }).notNull(),
  slug: varchar("slug", { length: 255 }).notNull().unique(),
  description: text("description"),
  category: varchar("category", { length: 100 }).notNull(),
  price: int("price").notNull().default(1700), // in cents (default $17)
  pdfUrl: varchar("pdf_url", { length: 500 }).notNull(),
  coverImage: text("cover_image"),
  promptCount: int("prompt_count").notNull().default(300),
  isActive: int("is_active").notNull().default(1),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().onUpdateNow().notNull(),
});

export type Product = typeof products.$inferSelect;
export type InsertProduct = typeof products.$inferInsert;

/**
 * Leads table - email captures from landing pages