import { useAuth } from "@/_core/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { trpc } from "@/lib/trpc";
import { getLoginUrl } from "@/const";
import { Link, useLocation } from "wouter";
import {
  BarChart3,
  BookOpen,
  DollarSign,
  Package,
  Plus,
  Sparkles,
  Users,
  TrendingUp,
  ShoppingCart,
} from "lucide-react";

export default function Admin() {
  const { user, loading, isAuthenticated } = useAuth();
  const [, setLocation] = useLocation();

  // Redirect if not admin
  if (!loading && (!isAuthenticated || user?.role !== "admin")) {
    window.location.href = getLoginUrl();
    return null;
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50/30">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/">
                <div className="flex items-center gap-2 cursor-pointer">
                  <Sparkles className="h-6 w-6 text-indigo-600" />
                  <span className="text-xl font-bold">AI Prompts Academy</span>
                </div>
              </Link>
              <span className="text-sm text-gray-500 border-l pl-4">Admin Panel</span>
            </div>
            <div className="flex items-center gap-4">
              <Link href="/courses">
                <Button variant="ghost">View Site</Button>
              </Link>
              <div className="text-sm text-gray-600">
                {user?.name}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Admin Dashboard</h1>
          <p className="text-gray-600">Manage your courses, bundles, and view analytics</p>
        </div>

        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-5 lg:w-auto lg:inline-grid">
            <TabsTrigger value="overview">
              <BarChart3 className="h-4 w-4 mr-2" />
              Overview
            </TabsTrigger>
            <TabsTrigger value="courses">
              <BookOpen className="h-4 w-4 mr-2" />
              Courses
            </TabsTrigger>
            <TabsTrigger value="bundles">
              <Package className="h-4 w-4 mr-2" />
              Bundles
            </TabsTrigger>
            <TabsTrigger value="sales">
              <ShoppingCart className="h-4 w-4 mr-2" />
              Sales
            </TabsTrigger>
            <TabsTrigger value="users">
              <Users className="h-4 w-4 mr-2" />
              Users
            </TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            <OverviewTab />
          </TabsContent>

          {/* Courses Tab */}
          <TabsContent value="courses" className="space-y-6">
            <CoursesTab />
          </TabsContent>

          {/* Bundles Tab */}
          <TabsContent value="bundles" className="space-y-6">
            <BundlesTab />
          </TabsContent>

          {/* Sales Tab */}
          <TabsContent value="sales" className="space-y-6">
            <SalesTab />
          </TabsContent>

          {/* Users Tab */}
          <TabsContent value="users" className="space-y-6">
            <UsersTab />
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}

function OverviewTab() {
  // TODO: Add tRPC queries for stats
  const stats = {
    totalCourses: 193,
    totalPrompts: 9352,
    totalRevenue: 0,
    totalUsers: 1,
    totalSales: 0,
  };

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Courses</CardTitle>
          <BookOpen className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.totalCourses}</div>
          <p className="text-xs text-muted-foreground">Across 14 categories</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Prompts</CardTitle>
          <Sparkles className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.totalPrompts.toLocaleString()}</div>
          <p className="text-xs text-muted-foreground">Expert AI prompts</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
          <DollarSign className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">R{stats.totalRevenue.toLocaleString()}</div>
          <p className="text-xs text-muted-foreground">From {stats.totalSales} sales</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Users</CardTitle>
          <Users className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.totalUsers}</div>
          <p className="text-xs text-muted-foreground">Registered users</p>
        </CardContent>
      </Card>

      <Card className="md:col-span-2 lg:col-span-4">
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>Common administrative tasks</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-3">
          <Button className="w-full" variant="outline">
            <Plus className="h-4 w-4 mr-2" />
            Add New Course
          </Button>
          <Button className="w-full" variant="outline">
            <Package className="h-4 w-4 mr-2" />
            Create Bundle
          </Button>
          <Button className="w-full" variant="outline">
            <TrendingUp className="h-4 w-4 mr-2" />
            View Analytics
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

function CoursesTab() {
  const { data: courses, isLoading } = trpc.courses.list.useQuery();

  if (isLoading) {
    return <div className="text-center py-12">Loading courses...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Manage Courses</h2>
          <p className="text-gray-600">View and edit all your courses</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Add Course
        </Button>
      </div>

      <div className="grid gap-4">
        {courses?.map((course) => (
          <Card key={course.id}>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="text-lg">{course.title}</CardTitle>
                  <CardDescription className="mt-1">{course.description}</CardDescription>
                  <div className="flex items-center gap-4 mt-2 text-sm text-gray-600">
                    <span className="flex items-center gap-1">
                      <BookOpen className="h-4 w-4" />
                      {course.promptCount} prompts
                    </span>
                    <span className="px-2 py-1 bg-indigo-100 text-indigo-700 rounded-full text-xs">
                      {course.category}
                    </span>
                    <span className="font-semibold text-green-600">
                      R{(course.price / 100).toFixed(2)}
                    </span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm">Edit</Button>
                  <Button variant="ghost" size="sm">View</Button>
                </div>
              </div>
            </CardHeader>
          </Card>
        ))}
      </div>
    </div>
  );
}

function BundlesTab() {
  const { data: bundles, isLoading } = trpc.bundles.list.useQuery();

  if (isLoading) {
    return <div className="text-center py-12">Loading bundles...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Manage Bundles</h2>
          <p className="text-gray-600">Create and manage course bundles</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Create Bundle
        </Button>
      </div>

      {bundles && bundles.length > 0 ? (
        <div className="grid gap-4">
          {bundles.map((bundle) => (
            <Card key={bundle.id}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-lg">{bundle.title}</CardTitle>
                    <CardDescription className="mt-1">{bundle.description}</CardDescription>
                    <div className="flex items-center gap-4 mt-2 text-sm text-gray-600">
                      <span className="px-2 py-1 bg-indigo-100 text-indigo-700 rounded-full text-xs">
                        {bundle.category}
                      </span>
                      <span className="font-semibold text-green-600">
                        R{(bundle.price / 100).toFixed(2)}
                      </span>
                      <span className="text-gray-500 line-through">
                        R{(bundle.originalPrice / 100).toFixed(2)}
                      </span>
                      <span className="text-red-600 font-semibold">
                        {bundle.discountPercent}% OFF
                      </span>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm">Edit</Button>
                    <Button variant="ghost" size="sm">View</Button>
                  </div>
                </div>
              </CardHeader>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardHeader>
            <CardTitle>No Bundles Yet</CardTitle>
            <CardDescription>
              Create your first bundle to offer discounted course packages to your customers
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Create Your First Bundle
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

function SalesTab() {
  // TODO: Add tRPC query for sales
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">Sales Overview</h2>
        <p className="text-gray-600">Track your revenue and sales performance</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>No Sales Yet</CardTitle>
          <CardDescription>
            Sales data will appear here once customers start purchasing courses
          </CardDescription>
        </CardHeader>
      </Card>
    </div>
  );
}

function UsersTab() {
  // TODO: Add tRPC query for users
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">User Management</h2>
        <p className="text-gray-600">View and manage registered users</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Registered Users</CardTitle>
          <CardDescription>1 user registered</CardDescription>
        </CardHeader>
      </Card>
    </div>
  );
}
