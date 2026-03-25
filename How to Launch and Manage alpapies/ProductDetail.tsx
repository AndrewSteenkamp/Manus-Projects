import { useState } from "react";
import { useAuth } from "@/_core/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { formatPrice, calculateDiscount, getLoginUrl } from "@/const";
import { trpc } from "@/lib/trpc";
import { Link, useRoute, useLocation } from "wouter";
import { ShoppingCart, Truck, Shield, ArrowLeft, Plus, Minus } from "lucide-react";
import { toast } from "sonner";

export default function ProductDetail() {
  const [, params] = useRoute("/product/:slug");
  const [, setLocation] = useLocation();
  const { isAuthenticated } = useAuth();
  const [quantity, setQuantity] = useState(1);

  const { data: product, isLoading } = trpc.products.getBySlug.useQuery(params?.slug || "");
  const addToCartMutation = trpc.cart.add.useMutation({
    onSuccess: () => {
      toast.success("Added to cart!");
      setLocation("/cart");
    },
    onError: (error) => {
      toast.error(error.message || "Failed to add to cart");
    },
  });

  const handleAddToCart = () => {
    if (!isAuthenticated) {
      window.location.href = getLoginUrl();
      return;
    }

    if (product) {
      addToCartMutation.mutate({
        productId: product.id,
        quantity,
      });
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background">
        <header className="border-b">
          <div className="container flex h-16 items-center">
            <Link href="/products" className="flex items-center text-sm hover:text-primary">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Products
            </Link>
          </div>
        </header>
        <div className="container py-8">
          <div className="grid md:grid-cols-2 gap-8">
            <div className="aspect-square bg-muted animate-pulse rounded-lg" />
            <div className="space-y-4">
              <div className="h-8 bg-muted animate-pulse rounded" />
              <div className="h-4 bg-muted animate-pulse rounded w-2/3" />
              <div className="h-20 bg-muted animate-pulse rounded" />
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Product Not Found</h1>
          <Button asChild>
            <Link href="/products">
              Browse Products
            </Link>
          </Button>
        </div>
      </div>
    );
  }

  const discount = calculateDiscount(product.price, product.compareAtPrice || 0);
  const isOutOfStock = product.stock === 0;
  const isLowStock = product.stock <= 10 && product.stock > 0;

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container flex h-16 items-center justify-between">
          <Link href="/products" className="flex items-center text-sm hover:text-primary">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Products
          </Link>
          <Button variant="outline" size="sm" asChild>
            <Link href="/">
              Home
            </Link>
          </Button>
        </div>
      </header>

      <div className="container py-8">
        <div className="grid md:grid-cols-2 gap-8 lg:gap-12">
          {/* Product Image */}
          <div className="space-y-4">
            <div className="aspect-square bg-muted rounded-lg overflow-hidden relative">
              {product.imageUrl ? (
                <img
                  src={product.imageUrl}
                  alt={product.name}
                  className="object-cover w-full h-full"
                />
              ) : (
                <div className="flex items-center justify-center h-full text-muted-foreground">
                  No Image Available
                </div>
              )}
              {discount > 0 && (
                <Badge className="absolute top-4 right-4 bg-destructive text-destructive-foreground text-lg px-3 py-1">
                  -{discount}% OFF
                </Badge>
              )}
            </div>
          </div>

          {/* Product Info */}
          <div className="space-y-6">
            <div>
              <h1 className="text-3xl font-bold tracking-tight mb-2">{product.name}</h1>
              {product.sku && (
                <p className="text-sm text-muted-foreground">SKU: {product.sku}</p>
              )}
            </div>

            {/* Price */}
            <div className="flex items-baseline gap-3">
              <span className="text-4xl font-bold text-primary">
                {formatPrice(product.price)}
              </span>
              {product.compareAtPrice && product.compareAtPrice > product.price && (
                <span className="text-xl text-muted-foreground line-through">
                  {formatPrice(product.compareAtPrice)}
                </span>
              )}
            </div>

            {/* Stock Status */}
            <div>
              {isOutOfStock ? (
                <Badge variant="secondary" className="bg-muted text-muted-foreground">
                  Out of Stock
                </Badge>
              ) : isLowStock ? (
                <Badge variant="secondary" className="bg-warning/10 text-warning-foreground">
                  Only {product.stock} left in stock!
                </Badge>
              ) : (
                <Badge variant="secondary" className="bg-green-100 text-green-800">
                  In Stock
                </Badge>
              )}
            </div>

            {/* Description */}
            {product.description && (
              <div>
                <h2 className="font-semibold mb-2">Description</h2>
                <p className="text-muted-foreground leading-relaxed">{product.description}</p>
              </div>
            )}

            {/* Quantity Selector */}
            {!isOutOfStock && (
              <div className="flex items-center gap-4">
                <span className="font-semibold">Quantity:</span>
                <div className="flex items-center border rounded-lg">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    disabled={quantity <= 1}
                  >
                    <Minus className="h-4 w-4" />
                  </Button>
                  <span className="px-6 font-semibold">{quantity}</span>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => setQuantity(Math.min(product.stock, quantity + 1))}
                    disabled={quantity >= product.stock}
                  >
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            )}

            {/* Add to Cart Button */}
            <div className="space-y-3">
              <Button
                size="lg"
                className="w-full"
                onClick={handleAddToCart}
                disabled={isOutOfStock || addToCartMutation.isPending}
              >
                <ShoppingCart className="h-5 w-5 mr-2" />
                {isOutOfStock ? "Out of Stock" : "Add to Cart"}
              </Button>
              {!isAuthenticated && (
                <p className="text-sm text-muted-foreground text-center">
                  Please sign in to add items to cart
                </p>
              )}
            </div>

            {/* Features */}
            <div className="grid grid-cols-1 gap-4 pt-6 border-t">
              <div className="flex items-start gap-3">
                <div className="bg-primary/10 p-2 rounded-lg">
                  <Truck className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <h3 className="font-semibold text-sm">Fast Worldwide Shipping</h3>
                  <p className="text-sm text-muted-foreground">
                    Quick delivery via ZQ Dropshipping
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-primary/10 p-2 rounded-lg">
                  <Shield className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <h3 className="font-semibold text-sm">Secure Checkout</h3>
                  <p className="text-sm text-muted-foreground">
                    Your payment information is protected
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Product Details */}
        {(product.weight || product.dimensions) && (
          <Card className="mt-12">
            <CardContent className="p-6">
              <h2 className="text-xl font-bold mb-4">Product Specifications</h2>
              <div className="grid md:grid-cols-2 gap-4">
                {product.weight && (
                  <div>
                    <span className="font-semibold">Weight:</span>{" "}
                    <span className="text-muted-foreground">{product.weight}g</span>
                  </div>
                )}
                {product.dimensions && (
                  <div>
                    <span className="font-semibold">Dimensions:</span>{" "}
                    <span className="text-muted-foreground">{product.dimensions}</span>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
