import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/hooks/useAuth";
import { trpc } from "@/lib/trpc";
import { ArrowLeft, Mail, Calendar, Eye, Loader2 } from "lucide-react";
import { Link, useLocation } from "wouter";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";

export default function Newsletters() {
  const { user } = useAuth();
  const [, setLocation] = useLocation();
  const [selectedNewsletter, setSelectedNewsletter] = useState<any>(null);

  const { data: newsletters, isLoading, refetch } = trpc.newsletters.list.useQuery(undefined, {
    enabled: !!user,
  });

  const generateMutation = trpc.newsletters.generate.useMutation({
    onSuccess: () => {
      refetch();
    },
  });

  if (!user) {
    setLocation("/login?returnTo=/newsletters");
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-8">
        <div className="container">
          <Link href="/dashboard">
            <Button variant="ghost" className="text-white hover:bg-white/20 mb-4">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Dashboard
            </Button>
          </Link>
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div>
              <h1 className="text-3xl font-bold mb-2">Weekly Newsletters</h1>
              <p className="text-blue-100">AI-generated market insights delivered to your inbox</p>
            </div>
            <Button
              onClick={() => generateMutation.mutate()}
              disabled={generateMutation.isPending}
              className="mt-4 md:mt-0 bg-white text-blue-600 hover:bg-blue-50"
            >
              {generateMutation.isPending ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <Mail className="w-4 h-4 mr-2" />
                  Generate Newsletter
                </>
              )}
            </Button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container py-12">
        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
          </div>
        ) : newsletters && newsletters.length > 0 ? (
          <div className="grid gap-6">
            {newsletters.map((newsletter: any) => (
              <Card key={newsletter.id} className="glass-card hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-xl mb-2">{newsletter.subject}</CardTitle>
                      <CardDescription className="flex items-center gap-4">
                        <span className="flex items-center gap-1">
                          <Calendar className="w-4 h-4" />
                          {new Date(newsletter.sentAt).toLocaleDateString("en-ZA", {
                            year: "numeric",
                            month: "long",
                            day: "numeric",
                          })}
                        </span>
                        {newsletter.opened && (
                          <span className="text-green-600 flex items-center gap-1">
                            <Eye className="w-4 h-4" />
                            Opened
                          </span>
                        )}
                      </CardDescription>
                    </div>
                    <Button
                      variant="outline"
                      onClick={() => setSelectedNewsletter(newsletter)}
                    >
                      <Eye className="w-4 h-4 mr-2" />
                      View
                    </Button>
                  </div>
                </CardHeader>
              </Card>
            ))}
          </div>
        ) : (
          <Card className="glass-card">
            <CardContent className="py-12 text-center">
              <Mail className="w-16 h-16 mx-auto mb-4 text-gray-400" />
              <h3 className="text-xl font-semibold mb-2">No Newsletters Yet</h3>
              <p className="text-gray-600 dark:text-gray-400 mb-6">
                Click "Generate Newsletter" to create your first AI-powered market insights report
              </p>
              <Button
                onClick={() => generateMutation.mutate()}
                disabled={generateMutation.isPending}
              >
                {generateMutation.isPending ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Generating...
                  </>
                ) : (
                  <>
                    <Mail className="w-4 h-4 mr-2" />
                    Generate First Newsletter
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Newsletter Viewer Dialog */}
      <Dialog open={!!selectedNewsletter} onOpenChange={() => setSelectedNewsletter(null)}>
        <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{selectedNewsletter?.subject}</DialogTitle>
          </DialogHeader>
          <div
            className="prose dark:prose-invert max-w-none"
            dangerouslySetInnerHTML={{ __html: selectedNewsletter?.content || "" }}
          />
        </DialogContent>
      </Dialog>
    </div>
  );
}
