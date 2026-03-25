import { useAuth } from "@/_core/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { APP_TITLE } from "@/const";
import { trpc } from "@/lib/trpc";
import { Users, CheckCircle, XCircle, Clock, LogOut, Shield } from "lucide-react";
import { toast } from "sonner";

export default function AdminDashboard() {
  const { user, logout } = useAuth();
  const { data: pendingProviders, refetch } = trpc.admin.getPendingProviders.useQuery();
  const approveMutation = trpc.admin.approveProvider.useMutation();
  const rejectMutation = trpc.admin.rejectProvider.useMutation();

  const handleLogout = () => {
    logout();
    window.location.href = "/";
  };

  const handleApprove = async (providerId: number) => {
    try {
      await approveMutation.mutateAsync({ providerId });
      toast.success("Provider approved successfully");
      refetch();
    } catch (error) {
      toast.error("Failed to approve provider");
    }
  };

  const handleReject = async (providerId: number) => {
    const reason = prompt("Enter rejection reason:");
    if (!reason) return;

    try {
      await rejectMutation.mutateAsync({ providerId, reason });
      toast.success("Provider rejected");
      refetch();
    } catch (error) {
      toast.error("Failed to reject provider");
    }
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
            <Badge variant="destructive">
              <Shield className="w-3 h-3 mr-1" />
              Admin
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
          <h1 className="text-3xl font-bold mb-2">Admin Dashboard</h1>
          <p className="text-muted-foreground">Manage provider applications and platform operations</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-yellow-100 flex items-center justify-center">
                  <Clock className="w-6 h-6 text-yellow-600" />
                </div>
                <div>
                  <CardTitle className="text-lg">{pendingProviders?.length || 0}</CardTitle>
                  <CardDescription>Pending Applications</CardDescription>
                </div>
              </div>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center">
                  <CheckCircle className="w-6 h-6 text-green-600" />
                </div>
                <div>
                  <CardTitle className="text-lg">0</CardTitle>
                  <CardDescription>Approved Providers</CardDescription>
                </div>
              </div>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
                  <Users className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <CardTitle className="text-lg">0</CardTitle>
                  <CardDescription>Total Customers</CardDescription>
                </div>
              </div>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center">
                  <XCircle className="w-6 h-6 text-purple-600" />
                </div>
                <div>
                  <CardTitle className="text-lg">0</CardTitle>
                  <CardDescription>Active Bookings</CardDescription>
                </div>
              </div>
            </CardHeader>
          </Card>
        </div>

        {/* Pending Provider Applications */}
        <Card>
          <CardHeader>
            <CardTitle>Pending Provider Applications</CardTitle>
            <CardDescription>Review and approve or reject provider applications</CardDescription>
          </CardHeader>
          <CardContent>
            {pendingProviders && pendingProviders.length > 0 ? (
              <div className="space-y-4">
                {pendingProviders.map((item) => {
                  const provider = item.profile;
                  const user = item.user;
                  
                  return (
                    <div key={provider?.id} className="border rounded-lg p-6">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <h3 className="font-semibold text-lg mb-1">{user?.name || "Unknown"}</h3>
                          <p className="text-sm text-muted-foreground">{user?.email}</p>
                        </div>
                        <Badge variant="secondary">
                          <Clock className="w-3 h-3 mr-1" />
                          Pending Review
                        </Badge>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                        <div>
                          <p className="text-sm font-medium mb-1">Phone</p>
                          <p className="text-sm text-muted-foreground">{provider?.phone || "N/A"}</p>
                        </div>
                        <div>
                          <p className="text-sm font-medium mb-1">Location</p>
                          <p className="text-sm text-muted-foreground">
                            {provider?.city}, {provider?.province || "N/A"}
                          </p>
                        </div>
                        <div>
                          <p className="text-sm font-medium mb-1">Background Check</p>
                          <Badge variant={
                            provider?.backgroundCheckStatus === 'completed' ? 'default' :
                            provider?.backgroundCheckStatus === 'in_progress' ? 'secondary' :
                            provider?.backgroundCheckStatus === 'failed' ? 'destructive' : 'outline'
                          }>
                            {provider?.backgroundCheckStatus || "not_started"}
                          </Badge>
                        </div>
                        <div>
                          <p className="text-sm font-medium mb-1">Insurance Verified</p>
                          <Badge variant={provider?.insuranceVerified ? 'default' : 'outline'}>
                            {provider?.insuranceVerified ? 'Yes' : 'No'}
                          </Badge>
                        </div>
                      </div>

                      {provider?.bio && (
                        <div className="mb-4">
                          <p className="text-sm font-medium mb-1">Bio</p>
                          <p className="text-sm text-muted-foreground">{provider.bio}</p>
                        </div>
                      )}

                      <div className="flex gap-2">
                        <Button 
                          size="sm" 
                          onClick={() => handleApprove(provider?.userId || 0)}
                          disabled={approveMutation.isPending}
                        >
                          <CheckCircle className="w-4 h-4 mr-2" />
                          Approve
                        </Button>
                        <Button 
                          size="sm" 
                          variant="destructive"
                          onClick={() => handleReject(provider?.userId || 0)}
                          disabled={rejectMutation.isPending}
                        >
                          <XCircle className="w-4 h-4 mr-2" />
                          Reject
                        </Button>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="text-center py-12">
                <div className="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-4">
                  <CheckCircle className="w-8 h-8 text-gray-400" />
                </div>
                <h3 className="font-semibold mb-2">No pending applications</h3>
                <p className="text-muted-foreground">
                  All provider applications have been reviewed
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
