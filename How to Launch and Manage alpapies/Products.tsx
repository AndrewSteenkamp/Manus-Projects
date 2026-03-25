import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { formatPrice, calculateDiscount } from "@/const";
import { trpc } from "@/lib/trpc";
import { Link } from "wouter";
import { Search, SlidersHorizontal } from "lucide-react";

export default function Products() {
  const [selectedCategory, setSelectedCategory] = useState<number | undefined>();
  const [searchQuery, setSearchQuery] = useState("");

  const { data: products, isLoading } = trpc.products.list.useQuery({
    categoryId: selectedCategory,
  });
  const { data: categories } = trpc.categories.list.useQuery();

  // Filter products by search query on client side
  const filteredProducts = products?.filter((product) =>
    searchQuery
      ? product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        product.description?.toLowerCase().includes(searchQuery.toLowerCase())
      : true
  );

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container flex h-16 items-center justify-between">
          <Link href="/" className="font-bold text-xl">
            Alpapies
          </Link>
          <nav className="hidden md:flex items-center space-x-6">
            <Link href="/products" className="text-sm font-medium text-primary">
              Products
            </Link>
            <Link href="/compare" className="text-sm font-medium hover:text-primary transition-colors">
              Compare Prices
            </Link>
          </nav>
          <Button variant="outline" size="sm" asChild>
            <Link href="/">
              Home
            </Link>
          </Button>
        </div>
      </header>

      <div className="container py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold tracking-tight mb-2">All Products</h1>
          <p className="text-muted-foreground">
            Browse our complete collection of premium electronics
          </p>
        </div>

        {/* Filters */}
        <div className="flex flex-col md:flex-row gap-4 mb-8">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search products..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
          <Select
            value={selectedCategory?.toString() || "all"}
            onValueChange={(value) =>
              setSelectedCategory(value === "all" ? undefined : parseInt(value))
            }
          >
            <SelectTrigger className="w-full md:w-[200px]">
              <SlidersHorizontal className="h-4 w-4 mr-2" />
              <SelectValue placeholder="All Categories" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Categories</SelectItem>
              {categories?.map((category) => (
                <SelectItem key={category.id} value={category.id.toString()}>
                  {category.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Results Count */}
        <div className="mb-4 text-sm text-muted-foreground">
          {filteredProducts && (
            <span>
              Showing {filteredProducts.length} {filteredProducts.length === 1 ? "product" : "products"}
            </span>
          )}
        </div>

        {/* Products Grid */}
        {isLoading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
              <Card key={i} className="overflow-hidden">
                <div className="aspect-square bg-muted animate-pulse" />
                <CardContent className="p-4">
                  <div className="h-4 bg-muted rounded animate-pulse mb-2" />
                  <div className="h-3 bg-muted rounded animate-pulse w-2/3" />
                </CardContent>
              </Card>
            ))}
          </div>
        ) : filteredProducts && filteredProducts.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredProducts.map((product) => {
              const discount = calculateDiscount(product.price, product.compareAtPrice || 0);
              return (
                <Link key={product.id} href={`/product/${product.slug}`}>
                  <Card className="overflow-hidden hover:shadow-lg transition-shadow group">
                      <div className="aspect-square bg-muted relative overflow-hidden">
                        {product.imageUrl ? (
                          <img
                            src={product.imageUrl}
                            alt={product.name}
                            className="object-cover w-full h-full group-hover:scale-105 transition-transform"
                          />
                        ) : (
                          <div className="flex items-center justify-center h-full text-muted-foreground">
                            No Image
                          </div>
                        )}
                        {discount > 0 && (
                          <Badge className="absolute top-2 right-2 bg-destructive text-destructive-foreground">
                            -{discount}%
                          </Badge>
                        )}
                        {product.stock <= 10 && product.stock > 0 && (
                          <Badge className="absolute top-2 left-2 bg-warning text-warning-foreground">
                            Low Stock
                          </Badge>
                        )}
                        {product.stock === 0 && (
                          <Badge className="absolute top-2 left-2 bg-muted text-muted-foreground">
                            Out of Stock
                          </Badge>
                        )}
                      </div>
                      <CardContent className="p-4">
                        <h3 className="font-semibold line-clamp-2 mb-2 group-hover:text-primary transition-colors">
                          {product.name}
                        </h3>
                        {product.shortDescription && (
                          <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
                            {product.shortDescription}
                          </p>
                        )}
                        <div className="flex items-center gap-2">
                          <span className="text-lg font-bold text-primary">
                            {formatPrice(product.price)}
                          </span>
                          {product.compareAtPrice && product.compareAtPrice > product.price && (
                            <span className="text-sm text-muted-foreground line-through">
                              {formatPrice(product.compareAtPrice)}
                            </span>
                          )}
                        </div>
                      </CardContent>
                      <CardFooter className="p-4 pt-0">
                        <Button className="w-full" size="sm" disabled={product.stock === 0}>
                          {product.stock === 0 ? "Out of Stock" : "View Details"}
                        </Button>
                      </CardFooter>
                  </Card>
                </Link>
              );
            })}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-muted-foreground mb-4">No products found matching your criteria.</p>
            <Button
              variant="outline"
              onClick={() => {
                setSearchQuery("");
                setSelectedCategory(undefined);
              }}
            >
              Clear Filters
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
