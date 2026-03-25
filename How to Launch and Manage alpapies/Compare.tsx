import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { formatPrice, calculateDiscount } from "@/const";
import { trpc } from "@/lib/trpc";
import { Link } from "wouter";
import { Search, X, ArrowLeft, Check, Minus } from "lucide-react";

export default function Compare() {
  const [selectedProducts, setSelectedProducts] = useState<number[]>([]);
  const [searchQuery, setSearchQuery] = useState("");

  const { data: allProducts } = trpc.products.list.useQuery({});
  const { data: compareProducts } = trpc.products.getByIds.useQuery(
    selectedProducts,
    { enabled: selectedProducts.length > 0 }
  );

  const filteredProducts = allProducts?.filter((product) =>
    searchQuery
      ? product.name.toLowerCase().includes(searchQuery.toLowerCase())
      : true
  );

  const toggleProduct = (productId: number) => {
    if (selectedProducts.includes(productId)) {
      setSelectedProducts(selectedProducts.filter((id) => id !== productId));
    } else if (selectedProducts.length < 4) {
      setSelectedProducts([...selectedProducts, productId]);
    }
  };

  const features = [
    { key: "price", label: "Price" },
    { key: "compareAtPrice", label: "Original Price" },
    { key: "discount", label: "Discount" },
    { key: "stock", label: "Availability" },
    { key: "sku", label: "SKU" },
    { key: "weight", label: "Weight" },
    { key: "dimensions", label: "Dimensions" },
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container flex h-16 items-center justify-between">
          <Link href="/">
            <a className="flex items-center text-sm hover:text-primary">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Home
            </a>
          </Link>
          <Button variant="outline" size="sm" asChild>
            <Link href="/products">
              <a>Browse Products</a>
            </Link>
          </Button>
        </div>
      </header>

      <div className="container py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold tracking-tight mb-2">Compare Products</h1>
          <p className="text-muted-foreground">
            Select up to 4 products to compare their features and prices side by side
          </p>
        </div>

        {/* Search and Select */}
        {selectedProducts.length < 4 && (
          <Card className="mb-8">
            <CardContent className="p-6">
              <div className="relative mb-4">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search products to compare..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>

              {searchQuery && filteredProducts && filteredProducts.length > 0 && (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 max-h-96 overflow-y-auto">
                  {filteredProducts.slice(0, 12).map((product) => {
                    const isSelected = selectedProducts.includes(product.id);
                    return (
                      <Card
                        key={product.id}
                        className={`cursor-pointer transition-all ${
                          isSelected ? "ring-2 ring-primary" : "hover:shadow-md"
                        }`}
                        onClick={() => toggleProduct(product.id)}
                      >
                        <CardContent className="p-4">
                          <div className="aspect-square bg-muted rounded mb-2 relative overflow-hidden">
                            {product.imageUrl ? (
                              <img
                                src={product.imageUrl}
                                alt={product.name}
                                className="object-cover w-full h-full"
                              />
                            ) : (
                              <div className="flex items-center justify-center h-full text-muted-foreground text-xs">
                                No Image
                              </div>
                            )}
                            {isSelected && (
                              <div className="absolute inset-0 bg-primary/20 flex items-center justify-center">
                                <Check className="h-8 w-8 text-primary" />
                              </div>
                            )}
                          </div>
                          <h3 className="font-semibold text-sm line-clamp-2 mb-1">
                            {product.name}
                          </h3>
                          <p className="text-primary font-bold text-sm">
                            {formatPrice(product.price)}
                          </p>
                        </CardContent>
                      </Card>
                    );
                  })}
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Comparison Table */}
        {compareProducts && compareProducts.length > 0 ? (
          <div className="overflow-x-auto">
            <div className="min-w-max">
              {/* Product Cards */}
              <div className="grid gap-4 mb-8" style={{ gridTemplateColumns: `repeat(${compareProducts.length}, minmax(250px, 1fr))` }}>
                {compareProducts.map((product) => (
                  <Card key={product.id} className="relative">
                    <Button
                      variant="ghost"
                      size="icon"
                      className="absolute top-2 right-2 z-10"
                      onClick={() => toggleProduct(product.id)}
                    >
                      <X className="h-4 w-4" />
                    </Button>
                    <CardContent className="p-4">
                      <div className="aspect-square bg-muted rounded mb-4 overflow-hidden">
                        {product.imageUrl ? (
                          <img
                            src={product.imageUrl}
                            alt={product.name}
                            className="object-cover w-full h-full"
                          />
                        ) : (
                          <div className="flex items-center justify-center h-full text-muted-foreground">
                            No Image
                          </div>
                        )}
                      </div>
                      <h3 className="font-bold mb-2 line-clamp-2">{product.name}</h3>
                      <Button size="sm" className="w-full" asChild>
                        <Link href={`/product/${product.slug}`}>
                          <a>View Details</a>
                        </Link>
                      </Button>
                    </CardContent>
                  </Card>
                ))}
              </div>

              {/* Comparison Features */}
              <Card>
                <CardContent className="p-0">
                  <table className="w-full">
                    <tbody>
                      {features.map((feature, index) => (
                        <tr
                          key={feature.key}
                          className={index % 2 === 0 ? "bg-muted/30" : ""}
                        >
                          <td className="p-4 font-semibold border-r sticky left-0 bg-background">
                            {feature.label}
                          </td>
                          {compareProducts.map((product) => {
                            let value: React.ReactNode = <Minus className="h-4 w-4 text-muted-foreground" />;

                            if (feature.key === "price") {
                              value = (
                                <span className="text-primary font-bold text-lg">
                                  {formatPrice(product.price)}
                                </span>
                              );
                            } else if (feature.key === "compareAtPrice") {
                              value = product.compareAtPrice ? (
                                <span className="text-muted-foreground line-through">
                                  {formatPrice(product.compareAtPrice)}
                                </span>
                              ) : (
                                <Minus className="h-4 w-4 text-muted-foreground" />
                              );
                            } else if (feature.key === "discount") {
                              const discount = calculateDiscount(
                                product.price,
                                product.compareAtPrice || 0
                              );
                              value = discount > 0 ? (
                                <Badge className="bg-destructive text-destructive-foreground">
                                  -{discount}%
                                </Badge>
                              ) : (
                                <Minus className="h-4 w-4 text-muted-foreground" />
                              );
                            } else if (feature.key === "stock") {
                              value =
                                product.stock > 0 ? (
                                  <Badge variant="secondary" className="bg-green-100 text-green-800">
                                    In Stock ({product.stock})
                                  </Badge>
                                ) : (
                                  <Badge variant="secondary" className="bg-muted text-muted-foreground">
                                    Out of Stock
                                  </Badge>
                                );
                            } else if (feature.key === "weight") {
                              value = product.weight ? `${product.weight}g` : <Minus className="h-4 w-4 text-muted-foreground" />;
                            } else {
                              const val = product[feature.key as keyof typeof product];
                              value = val ? String(val) : <Minus className="h-4 w-4 text-muted-foreground" />;
                            }

                            return (
                              <td key={product.id} className="p-4 text-center">
                                {value}
                              </td>
                            );
                          })}
                        </tr>
                      ))}

                      {/* Description Row */}
                      <tr>
                        <td className="p-4 font-semibold border-r sticky left-0 bg-background">
                          Description
                        </td>
                        {compareProducts.map((product) => (
                          <td key={product.id} className="p-4">
                            <p className="text-sm text-muted-foreground line-clamp-3">
                              {product.shortDescription || product.description || "No description available"}
                            </p>
                          </td>
                        ))}
                      </tr>
                    </tbody>
                  </table>
                </CardContent>
              </Card>
            </div>
          </div>
        ) : (
          <Card>
            <CardContent className="p-12 text-center">
              <Search className="h-16 w-16 mx-auto mb-4 text-muted-foreground" />
              <h2 className="text-xl font-semibold mb-2">No Products Selected</h2>
              <p className="text-muted-foreground mb-6">
                Search and select products above to start comparing
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
