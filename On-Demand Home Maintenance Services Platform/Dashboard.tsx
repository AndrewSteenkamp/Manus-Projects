import { useAuth } from "@/_core/hooks/useAuth";
import { Loader2 } from "lucide-react";
import { Redirect } from "wouter";
import CustomerDashboard from "./CustomerDashboard";
import ProviderDashboard from "./ProviderDashboard";
import AdminDashboard from "./AdminDashboard";

export default function Dashboard() {
  const { user, loading, isAuthenticated } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Redirect to="/" />;
  }

  // Route to appropriate dashboard based on user role
  if (user?.role === "admin") {
    return <AdminDashboard />;
  }

  if (user?.role === "provider") {
    return <ProviderDashboard />;
  }

  // Default to customer dashboard
  return <CustomerDashboard />;
}
