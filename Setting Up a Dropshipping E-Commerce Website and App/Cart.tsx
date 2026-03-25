import { useState } from "react";
import { Link, useLocation } from "wouter";
import { trpc } from "@/lib/trpc";
import { useAuth } from "@/_core/hooks/useAuth";
import { getLoginUrl } from "@/const";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { 
  Shield, 
  ShoppingCart, 
  Trash2,
  Plus,
  Minus,
  ArrowLeft,
  ArrowRight
} from "lucide-react";

export default function Cart() {
  const [, setLocation] = useLocation();
  const { isAuthenticated } = useAuth();

  const { data: cartItems, isLoading } = trpc.cart.items.useQuery(undefined, {
    enabled: isAuthenticated,
  });

  const utils = trpc.useUtils();

  const updateQuantityMutation = trpc.cart.updateQuantity.useMutation({
    onSuccess: () => {
      utils.cart.items.invalidate();
      toast.success("Cart updated");
    },
    onError: (error) => {
      toast.error(`Error: ${error.message}`);
    },
  });

  const removeItemMutation = trpc.cart.remove.useMutation({
    onSuccess: () => {
      utils.cart.items.invalidate();
      toast.success("Item removed from cart");
    },
    onError: (error) => {
      toast.error(`Error: ${error.message}`);
    },
  });

  const clearCartMutation = trpc.cart.clear.useMutation({
    onSuccess: () => {
      utils.cart.items.invalidate();
      toast.success("Cart cleared");
    },
    onError: (error) => {
      toast.error(`Error: ${error.message}`);
    },
  });

  if (!isAuthenticated) {
    setLocation(getLoginUrl());
    return null;
  }

  const handleUpdateQuantity = (cartItemId: number, newQuantity: number) => {
    if (newQuantity < 1) return;
    updateQuantityMutation.mutate({ id: cartItemId, quantity: newQuantity });
  };

  const handleRemoveItem = (cartItemId: number) => {
    removeItemMutation.mutate({ id: cartItemId });
  };

  const handleClearCart = () => {
    if (confirm("Are you sure you want to clear your cart?")) {
      clearCartMutation.mutate();
    }
  };

  const subtotal = cartItems?.reduce((sum, item) => {
    if (!item.product) return sum;
    return sum + parseFloat(item.product.price) * item.quantity;
  }, 0) || 0;

  const shipping = subtotal > 50 ? 0 : 5.99;
  const total = subtotal + shipping;

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container flex h-16 items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
              <Shield className="w-6 h-6 text-primary-foreground" />
            </div>
            <span className="text-xl font-bold">Alpapies</span>
          </Link>
          
          <div className="flex items-center gap-4">
            <Button variant="outline" onClick={() => setLocation("/account")}>Account</Button>
          </div>
        </div>
      </header>

      <div className="container py-8">
        {/* Back Button */}
        <Button variant="ghost" size="sm" className="mb-6 flex items-center gap-2" onClick={() => setLocation("/products")}>
          <ArrowLeft className="w-4 h-4" /> Continue Shopping
        </Button>

        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold tracking-tight mb-2">Shopping Cart</h1>
          <p className="text-muted-foreground">
            {cartItems?.length || 0} {cartItems?.length === 1 ? "item" : "items"} in your cart
          </p>
        </div>

        {isLoading ? (
          <div className="text-center py-12">
            <p className="text-muted-foreground">Loading cart...</p>
          </div>
        ) : !cartItems || cartItems.length === 0 ? (
          <Card>
            <CardContent className="p-12 text-center">
              <ShoppingCart className="w-16 h-16 mx-auto mb-4 text-muted-foreground" />
              <h2 className="text-2xl font-bold mb-2">Your cart is empty</h2>
              <p className="text-muted-foreground mb-6">
                Add some products to get started!
              </p>
              <Button size="lg" onClick={() => setLocation("/products")}>Browse Products</Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid lg:grid-cols-3 gap-8">
            {/* Cart Items */}
            <div className="lg:col-span-2 space-y-4">
              {cartItems.map((item) => {
                if (!item.product) return null;
                return (
                <Card key={item.id}>
                  <CardContent className="p-6">
                    <div className="flex gap-6">
                      {/* Product Image */}
                      <div className="w-24 h-24 rounded-lg bg-muted flex-shrink-0" />

                      {/* Product Info */}
                      <div className="flex-1">
                        <div className="flex justify-between items-start mb-2">
                          <div>
                            <h3 
                              className="font-semibold hover:text-primary transition-colors cursor-pointer"
                              onClick={() => item.product && setLocation(`/product/${item.product.id}`)}
                            >
                              {item.product.name}
                            </h3>
                            <p className="text-sm text-muted-foreground">
                              {item.product.category}
                            </p>
                          </div>
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleRemoveItem(item.id)}
                            disabled={removeItemMutation.isPending}
                          >
                            <Trash2 className="w-4 h-4 text-destructive" />
                          </Button>
                        </div>

                        <div className="flex items-center justify-between mt-4">
                          {/* Quantity Controls */}
                          <div className="flex items-center gap-2">
                            <Button
                              variant="outline"
                              size="icon"
                              className="h-8 w-8"
                              onClick={() => handleUpdateQuantity(item.id, item.quantity - 1)}
                              disabled={item.quantity <= 1 || updateQuantityMutation.isPending}
                            >
                              <Minus className="w-4 h-4" />
                            </Button>
                            <span className="w-12 text-center font-medium">{item.quantity}</span>
                            <Button
                              variant="outline"
                              size="icon"
                              className="h-8 w-8"
                              onClick={() => handleUpdateQuantity(item.id, item.quantity + 1)}
                              disabled={updateQuantityMutation.isPending}
                            >
                              <Plus className="w-4 h-4" />
                            </Button>
                          </div>

                          {/* Price */}
                          <div className="text-right">
                            <p className="font-bold text-lg">
                              ${(parseFloat(item.product.price) * item.quantity).toFixed(2)}
                            </p>
                            <p className="text-sm text-muted-foreground">
                              ${item.product.price} each
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
              })}

              {/* Clear Cart Button */}
              <Button
                variant="outline"
                className="w-full"
                onClick={handleClearCart}
                disabled={clearCartMutation.isPending}
              >
                <Trash2 className="w-4 h-4 mr-2" />
                Clear Cart
              </Button>
            </div>

            {/* Order Summary */}
            <div className="lg:col-span-1">
              <Card className="sticky top-24">
                <CardContent className="p-6">
                  <h2 className="text-xl font-bold mb-6">Order Summary</h2>

                  <div className="space-y-4 mb-6">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Subtotal</span>
                      <span className="font-medium">${subtotal.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Shipping</span>
                      <span className="font-medium">
                        {shipping === 0 ? (
                          <Badge variant="secondary">FREE</Badge>
                        ) : (
                          `$${shipping.toFixed(2)}`
                        )}
                      </span>
                    </div>
                    {shipping > 0 && (
                      <p className="text-sm text-muted-foreground">
                        Add ${(50 - subtotal).toFixed(2)} more for free shipping
                      </p>
                    )}
                    <div className="border-t pt-4">
                      <div className="flex justify-between items-center">
                        <span className="text-lg font-bold">Total</span>
                        <span className="text-2xl font-bold">${total.toFixed(2)}</span>
                      </div>
                    </div>
                  </div>

                  <Button size="lg" className="w-full mb-4" disabled>
                    <ArrowRight className="w-5 h-5 mr-2" />
                    Proceed to Checkout
                  </Button>
                  <p className="text-xs text-center text-muted-foreground">
                    Payment integration coming soon
                  </p>

                  <div className="mt-6 pt-6 border-t space-y-3">
                    <div className="flex items-center gap-3 text-sm">
                      <Shield className="w-5 h-5 text-primary" />
                      <span>Secure checkout</span>
                    </div>
                    <div className="flex items-center gap-3 text-sm">
                      <ShoppingCart className="w-5 h-5 text-primary" />
                      <span>30-day money-back guarantee</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
