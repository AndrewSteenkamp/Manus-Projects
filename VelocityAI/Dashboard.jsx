import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Plus, Play, Eye, CheckCircle, XCircle, Clock, Loader2 } from 'lucide-react';

const API_BASE = '/api';

const Dashboard = () => {
  const [clients, setClients] = useState([]);
  const [projects, setProjects] = useState([]);
  const [ads, setAds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedClient, setSelectedClient] = useState(null);
  const [newProject, setNewProject] = useState({
    product_name: '',
    product_url: '',
    product_description: '',
    category: ''
  });
  const [newClient, setNewClient] = useState({
    name: '',
    email: '',
    shopify_store_url: ''
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [clientsRes, projectsRes, adsRes] = await Promise.all([
        fetch(`${API_BASE}/clients`),
        fetch(`${API_BASE}/projects`),
        fetch(`${API_BASE}/ads`)
      ]);

      const clientsData = await clientsRes.json();
      const projectsData = await projectsRes.json();
      const adsData = await adsRes.json();

      setClients(clientsData);
      setProjects(projectsData);
      setAds(adsData);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const createClient = async () => {
    try {
      const response = await fetch(`${API_BASE}/clients`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newClient),
      });

      if (response.ok) {
        const client = await response.json();
        setClients([...clients, client]);
        setNewClient({ name: '', email: '', shopify_store_url: '' });
      }
    } catch (error) {
      console.error('Error creating client:', error);
    }
  };

  const createProject = async () => {
    if (!selectedClient) return;

    try {
      const response = await fetch(`${API_BASE}/projects`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...newProject,
          client_id: selectedClient.id
        }),
      });

      if (response.ok) {
        const project = await response.json();
        setProjects([...projects, project]);
        setNewProject({ product_name: '', product_url: '', product_description: '', category: '' });
      }
    } catch (error) {
      console.error('Error creating project:', error);
    }
  };

  const startAdGeneration = async (projectId) => {
    try {
      const response = await fetch(`${API_BASE}/projects/${projectId}/start-generation`, {
        method: 'POST',
      });

      if (response.ok) {
        fetchData(); // Refresh data
      }
    } catch (error) {
      console.error('Error starting ad generation:', error);
    }
  };

  const approveAd = async (adId) => {
    try {
      const response = await fetch(`${API_BASE}/ads/${adId}/approve`, {
        method: 'POST',
      });

      if (response.ok) {
        fetchData(); // Refresh data
      }
    } catch (error) {
      console.error('Error approving ad:', error);
    }
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { color: 'bg-yellow-100 text-yellow-800', icon: Clock },
      in_progress: { color: 'bg-blue-100 text-blue-800', icon: Loader2 },
      completed: { color: 'bg-green-100 text-green-800', icon: CheckCircle },
      pending_review: { color: 'bg-orange-100 text-orange-800', icon: Eye },
      approved: { color: 'bg-green-100 text-green-800', icon: CheckCircle },
      rejected: { color: 'bg-red-100 text-red-800', icon: XCircle },
    };

    const config = statusConfig[status] || statusConfig.pending;
    const Icon = config.icon;

    return (
      <Badge className={`${config.color} flex items-center gap-1`}>
        <Icon className="w-3 h-3" />
        {status.replace('_', ' ')}
      </Badge>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Loader2 className="w-8 h-8 animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">UGC Ads Agency Dashboard</h1>
          <p className="text-gray-600 mt-2">Manage your clients, projects, and AI-generated ads</p>
        </div>

        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="clients">Clients</TabsTrigger>
            <TabsTrigger value="projects">Projects</TabsTrigger>
            <TabsTrigger value="ads">Ads</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Clients</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{clients.length}</div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Active Projects</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {projects.filter(p => p.status === 'in_progress').length}
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Generated Ads</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{ads.length}</div>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Recent Activity</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {projects.slice(0, 5).map((project) => (
                    <div key={project.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div>
                        <h4 className="font-medium">{project.product_name}</h4>
                        <p className="text-sm text-gray-600">
                          Client: {clients.find(c => c.id === project.client_id)?.name || 'Unknown'}
                        </p>
                      </div>
                      {getStatusBadge(project.status)}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="clients" className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold">Clients</h2>
              <Dialog>
                <DialogTrigger asChild>
                  <Button>
                    <Plus className="w-4 h-4 mr-2" />
                    Add Client
                  </Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Add New Client</DialogTitle>
                    <DialogDescription>
                      Create a new client account to start managing their projects.
                    </DialogDescription>
                  </DialogHeader>
                  <div className="space-y-4">
                    <div>
                      <Label htmlFor="name">Name</Label>
                      <Input
                        id="name"
                        value={newClient.name}
                        onChange={(e) => setNewClient({ ...newClient, name: e.target.value })}
                        placeholder="Client name"
                      />
                    </div>
                    <div>
                      <Label htmlFor="email">Email</Label>
                      <Input
                        id="email"
                        type="email"
                        value={newClient.email}
                        onChange={(e) => setNewClient({ ...newClient, email: e.target.value })}
                        placeholder="client@example.com"
                      />
                    </div>
                    <div>
                      <Label htmlFor="shopify_url">Shopify Store URL</Label>
                      <Input
                        id="shopify_url"
                        value={newClient.shopify_store_url}
                        onChange={(e) => setNewClient({ ...newClient, shopify_store_url: e.target.value })}
                        placeholder="https://store.myshopify.com"
                      />
                    </div>
                    <Button onClick={createClient} className="w-full">
                      Create Client
                    </Button>
                  </div>
                </DialogContent>
              </Dialog>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {clients.map((client) => (
                <Card key={client.id} className="cursor-pointer hover:shadow-lg transition-shadow"
                      onClick={() => setSelectedClient(client)}>
                  <CardHeader>
                    <CardTitle>{client.name}</CardTitle>
                    <CardDescription>{client.email}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-600">
                      Projects: {projects.filter(p => p.client_id === client.id).length}
                    </p>
                    {client.shopify_store_url && (
                      <p className="text-sm text-blue-600 truncate">
                        {client.shopify_store_url}
                      </p>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="projects" className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold">Projects</h2>
              <Dialog>
                <DialogTrigger asChild>
                  <Button disabled={!selectedClient}>
                    <Plus className="w-4 h-4 mr-2" />
                    Add Project
                  </Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Add New Project</DialogTitle>
                    <DialogDescription>
                      Create a new project for {selectedClient?.name || 'a client'}.
                    </DialogDescription>
                  </DialogHeader>
                  <div className="space-y-4">
                    <div>
                      <Label htmlFor="product_name">Product Name</Label>
                      <Input
                        id="product_name"
                        value={newProject.product_name}
                        onChange={(e) => setNewProject({ ...newProject, product_name: e.target.value })}
                        placeholder="iPhone 15 Pro Max"
                      />
                    </div>
                    <div>
                      <Label htmlFor="category">Product Category</Label>
                      <select
                        id="category"
                        value={newProject.category || ''}
                        onChange={(e) => setNewProject({ ...newProject, category: e.target.value })}
                        className="w-full p-2 border border-gray-300 rounded-md"
                      >
                        <option value="">Auto-detect category</option>
                        <option value="electronics">Electronics</option>
                        <option value="beauty">Beauty & Cosmetics</option>
                        <option value="supplements">Health & Supplements</option>
                        <option value="outdoor">Outdoor & Sports</option>
                        <option value="fashion">Fashion & Accessories</option>
                        <option value="home">Home & Garden</option>
                        <option value="fitness">Fitness & Wellness</option>
                      </select>
                    </div>
                    <div>
                      <Label htmlFor="product_url">Product URL</Label>
                      <Input
                        id="product_url"
                        value={newProject.product_url}
                        onChange={(e) => setNewProject({ ...newProject, product_url: e.target.value })}
                        placeholder="https://store.com/product/iphone-15-pro-max"
                      />
                    </div>
                    <div>
                      <Label htmlFor="product_description">Product Description</Label>
                      <Textarea
                        id="product_description"
                        value={newProject.product_description}
                        onChange={(e) => setNewProject({ ...newProject, product_description: e.target.value })}
                        placeholder="Brief description of the product and its key features..."
                      />
                    </div>
                    <Button onClick={createProject} className="w-full">
                      Create Project
                    </Button>
                  </div>
                </DialogContent>
              </Dialog>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {projects.map((project) => (
                <Card key={project.id}>
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle>{project.product_name}</CardTitle>
                        <CardDescription>
                          {clients.find(c => c.id === project.client_id)?.name || 'Unknown Client'}
                        </CardDescription>
                      </div>
                      {getStatusBadge(project.status)}
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-600 mb-4">
                      {project.product_description || 'No description provided'}
                    </p>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-500">
                        Ads: {ads.filter(a => a.project_id === project.id).length}
                      </span>
                      {project.status === 'pending' && (
                        <Button
                          size="sm"
                          onClick={() => startAdGeneration(project.id)}
                        >
                          <Play className="w-4 h-4 mr-2" />
                          Start Generation
                        </Button>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="ads" className="space-y-6">
            <h2 className="text-2xl font-bold">Generated Ads</h2>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
              {ads.map((ad) => {
                const project = projects.find(p => p.id === ad.project_id);
                const client = clients.find(c => c.id === project?.client_id);
                
                return (
                  <Card key={ad.id}>
                    <CardHeader>
                      <div className="flex justify-between items-start">
                        <div>
                          <CardTitle className="text-lg">{project?.product_name || 'Unknown Product'}</CardTitle>
                          <CardDescription>{client?.name || 'Unknown Client'}</CardDescription>
                        </div>
                        {getStatusBadge(ad.status)}
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        <div>
                          <Label className="text-sm font-medium">Script:</Label>
                          <p className="text-sm text-gray-600 mt-1 line-clamp-3">
                            {ad.script}
                          </p>
                        </div>
                        
                        {ad.video_url && (
                          <div>
                            <Label className="text-sm font-medium">Video:</Label>
                            <div className="mt-2 bg-gray-100 rounded-lg p-4 text-center">
                              <Play className="w-8 h-8 mx-auto text-gray-400 mb-2" />
                              <p className="text-sm text-gray-600">Video Ready</p>
                            </div>
                          </div>
                        )}
                        
                        <div className="flex gap-2">
                          {ad.status === 'pending_review' && (
                            <Button
                              size="sm"
                              onClick={() => approveAd(ad.id)}
                              className="flex-1"
                            >
                              <CheckCircle className="w-4 h-4 mr-2" />
                              Approve
                            </Button>
                          )}
                          <Button size="sm" variant="outline" className="flex-1">
                            <Eye className="w-4 h-4 mr-2" />
                            View
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default Dashboard;

