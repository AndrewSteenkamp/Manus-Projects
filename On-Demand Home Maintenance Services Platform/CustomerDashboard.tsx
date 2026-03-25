import { useAuth } from "@/_core/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { APP_TITLE } from "@/const";
import { trpc } from "@/lib/trpc";
import { Plus, MapPin, Clock, DollarSign, MessageSquare, LogOut } from "lucide-react";
import { Link } from "wouter";

export default function CustomerDashboard() {
  const { user, logout } = useAuth();
  const { data: requests, isLoading } = trpc.requests.getMy.useQuery();

  const handleLogout = () => {
    logout();
    window.location.href = "/";
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-white font-bold">
              SHS
            </div>
            <span className="font-semibold text-lg">{APP_TITLE}</span>
          </div>
          
          <div className="flex items-center gap-4">
            <span className="text-sm text-muted-foreground">{user?.name || user?.email}</span>
            <Button variant="ghost" size="sm" onClick={handleLogout}>
              <LogOut className="w-4 h-4 mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      <div className="container py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Welcome back, {user?.name?.split(' ')[0] || 'Customer'}!</h1>
          <p className="text-muted-foreground">Manage your service requests and bookings</p>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Link href="/requests/new">
            <Card className="hover:shadow-lg transition-shadow cursor-pointer">
              <CardHeader>
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                    <Plus className="w-6 h-6 text-primary" />
                  </div>
                  <div>
                    <CardTitle className="text-lg">New Request</CardTitle>
                    <CardDescription>Post a service request</CardDescription>
                  </div>
                </div>
              </CardHeader>
            </Card>
          </Link>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
                  <Clock className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <CardTitle className="text-lg">{requests?.length || 0}</CardTitle>
                  <CardDescription>Active Requests</CardDescription>
                </div>
              </div>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center">
                  <MessageSquare className="w-6 h-6 text-green-600" />
                </div>
                <div>
                  <CardTitle className="text-lg">0</CardTitle>
                  <CardDescription>Unread Messages</CardDescription>
                </div>
              </div>
            </CardHeader>
          </Card>
        </div>

        {/* Service Requests */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>My Service Requests</CardTitle>
                <CardDescription>Track and manage your service requests</CardDescription>
              </div>
              <Button asChild>
                <Link href="/requests/new">
                  <Plus className="w-4 h-4 mr-2" />
                  New Request
                </Link>
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="text-center py-8 text-muted-foreground">Loading...</div>
            ) : requests && requests.length > 0 ? (
              <div className="space-y-4">
                {requests.map((request) => (
                  <div key={request.id} className="border rounded-lg p-4 hover:bg-gray-50 transition-colors">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <h3 className="font-semibold">{request.title}</h3>
                          <Badge variant={
                            request.status === 'open' ? 'default' :
                            request.status === 'quoted' ? 'secondary' :
                            request.status === 'accepted' ? 'default' : 'outline'
                          }>
                            {request.status}
                          </Badge>
                        </div>
                        <p className="text-sm text-muted-foreground mb-3 line-clamp-2">
                          {request.description}
                        </p>
                        <div className="flex items-center gap-4 text-sm text-muted-foreground">
                          <div className="flex items-center gap-1">
                            <MapPin className="w-4 h-4" />
                            {request.city}
                          </div>
                          <div className="flex items-center gap-1">
                            <Clock className="w-4 h-4" />
                            {new Date(request.createdAt).toLocaleDateString()}
                          </div>
                        </div>
                      </div>
                      <Button variant="outline" size="sm" asChild>
                        <Link href={`/requests/${request.id}`}>View Details</Link>
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <div className="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-4">
                  <Plus className="w-8 h-8 text-gray-400" />
                </div>
                <h3 className="font-semibold mb-2">No service requests yet</h3>
                <p className="text-muted-foreground mb-4">
                  Post your first service request to get started
                </p>
                <Button asChild>
                  <Link href="/requests/new">Create Service Request</Link>
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Become a Provider CTA */}
        <Card className="mt-8 bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
          <CardHeader>
            <CardTitle>Are you a service provider?</CardTitle>
            <CardDescription>
              Join our network of verified professionals and start receiving job requests
            </CardDescription>
            <div className="pt-4">
              <Button variant="default" asChild>
                <Link href="/provider/apply">Become a Provider</Link>
              </Button>
            </div>
          </CardHeader>
        </Card>
      </div>
    </div>
  );
}
