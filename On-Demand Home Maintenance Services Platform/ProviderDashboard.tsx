import { useAuth } from "@/_core/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { APP_TITLE } from "@/const";
import { trpc } from "@/lib/trpc";
import { Briefcase, DollarSign, Star, TrendingUp, LogOut, CheckCircle2 } from "lucide-react";
import { Link } from "wouter";

export default function ProviderDashboard() {
  const { user, logout } = useAuth();
  const { data: profile } = trpc.profile.get.useQuery();
  const { data: openRequests } = trpc.requests.getOpen.useQuery();
  const { data: myQuotes } = trpc.quotes.getMy.useQuery();
  const { data: myBookings } = trpc.bookings.getMyProvider.useQuery();

  const handleLogout = () => {
    logout();
    window.location.href = "/";
  };

  const providerProfile = profile?.providerProfile;
  const averageRating = providerProfile?.averageRating ? (providerProfile.averageRating / 100).toFixed(2) : "N/A";
  const tierLabel = providerProfile?.tier === "probationary" ? "Probationary (20%)" :
                    providerProfile?.tier === "verified" ? "Verified (18%)" :
                    providerProfile?.tier === "premium" ? "Premium (15%)" : "N/A";

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
            <Badge variant={providerProfile?.verificationStatus === "approved" ? "default" : "secondary"}>
              {providerProfile?.verificationStatus === "approved" ? (
                <><CheckCircle2 className="w-3 h-3 mr-1" /> Verified</>
              ) : (
                providerProfile?.verificationStatus || "Pending"
              )}
            </Badge>
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
          <h1 className="text-3xl font-bold mb-2">Provider Dashboard</h1>
          <p className="text-muted-foreground">Manage your quotes, bookings, and profile</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
                  <Briefcase className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <CardTitle className="text-lg">{providerProfile?.totalJobs || 0}</CardTitle>
                  <CardDescription>Total Jobs</CardDescription>
                </div>
              </div>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-yellow-100 flex items-center justify-center">
                  <Star className="w-6 h-6 text-yellow-600" />
                </div>
                <div>
                  <CardTitle className="text-lg">{averageRating}</CardTitle>
                  <CardDescription>Average Rating</CardDescription>
                </div>
              </div>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-green-600" />
                </div>
                <div>
                  <CardTitle className="text-lg">{tierLabel}</CardTitle>
                  <CardDescription>Provider Tier</CardDescription>
                </div>
              </div>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center">
                  <DollarSign className="w-6 h-6 text-purple-600" />
                </div>
                <div>
                  <CardTitle className="text-lg">{myBookings?.length || 0}</CardTitle>
                  <CardDescription>Active Bookings</CardDescription>
                </div>
              </div>
            </CardHeader>
          </Card>
        </div>

        {/* Verification Status Banner */}
        {providerProfile?.verificationStatus !== "approved" && (
          <Card className="mb-8 bg-yellow-50 border-yellow-200">
            <CardHeader>
              <CardTitle>Verification Pending</CardTitle>
              <CardDescription>
                Your provider application is under review. You'll be notified once your account is verified and you can start bidding on jobs.
              </CardDescription>
            </CardHeader>
          </Card>
        )}

        {/* Open Service Requests */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Available Service Requests</CardTitle>
                <CardDescription>Browse and bid on open service requests</CardDescription>
              </div>
              <Button variant="outline" asChild>
                <Link href="/requests/browse">View All</Link>
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {openRequests && openRequests.length > 0 ? (
              <div className="space-y-4">
                {openRequests.slice(0, 5).map((request) => (
                  <div key={request.id} className="border rounded-lg p-4 hover:bg-gray-50 transition-colors">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <h3 className="font-semibold">{request.title}</h3>
                          <Badge variant={request.urgency === "high" ? "destructive" : "secondary"}>
                            {request.urgency}
                          </Badge>
                        </div>
                        <p className="text-sm text-muted-foreground mb-3 line-clamp-2">
                          {request.description}
                        </p>
                        <div className="text-sm text-muted-foreground">
                          {request.city} • Posted {new Date(request.createdAt).toLocaleDateString()}
                        </div>
                      </div>
                      <Button size="sm" asChild>
                        <Link href={`/requests/${request.id}`}>Submit Quote</Link>
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                No open service requests available at the moment
              </div>
            )}
          </CardContent>
        </Card>

        {/* My Quotes */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>My Quotes</CardTitle>
                <CardDescription>Track your submitted quotes</CardDescription>
              </div>
              <Button variant="outline" asChild>
                <Link href="/quotes">View All</Link>
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {myQuotes && myQuotes.length > 0 ? (
              <div className="space-y-4">
                {myQuotes.slice(0, 5).map((quote) => (
                  <div key={quote.id} className="border rounded-lg p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <Badge variant={
                            quote.status === 'accepted' ? 'default' :
                            quote.status === 'pending' ? 'secondary' :
                            quote.status === 'rejected' ? 'destructive' : 'outline'
                          }>
                            {quote.status}
                          </Badge>
                        </div>
                        <div className="text-sm text-muted-foreground">
                          Quote Amount: R{(quote.amount / 100).toFixed(2)}
                        </div>
                        <div className="text-sm text-muted-foreground">
                          Submitted {new Date(quote.createdAt).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                No quotes submitted yet
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
