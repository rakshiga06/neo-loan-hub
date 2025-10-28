import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Building2, Shield, TrendingUp, Users } from "lucide-react";

const Index = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary via-primary to-accent py-24">
        <div className="container mx-auto px-4 text-center text-white">
          <div className="mb-8 flex justify-center">
            <div className="h-20 w-20 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
              <Building2 className="h-10 w-10" />
            </div>
          </div>
          <h1 className="mb-6 text-5xl font-bold">Welcome to LoanHub</h1>
          <p className="mb-8 text-xl text-white/90 max-w-2xl mx-auto">
            Your trusted partner for seamless loan management. Compare offers, check eligibility, and apply for loans from top banks in minutes.
          </p>
          <div className="flex gap-4 justify-center">
            <Button size="lg" variant="secondary" onClick={() => navigate("/signup")}>
              Get Started
            </Button>
            <Button size="lg" variant="outline" className="bg-white/10 border-white text-white hover:bg-white/20" onClick={() => navigate("/login")}>
              Login
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-secondary">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Why Choose LoanHub?</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-card p-6 rounded-lg shadow-md text-center">
              <div className="mb-4 flex justify-center">
                <div className="h-16 w-16 rounded-full bg-primary/10 flex items-center justify-center">
                  <Shield className="h-8 w-8 text-primary" />
                </div>
              </div>
              <h3 className="text-xl font-semibold mb-2">Secure & Trusted</h3>
              <p className="text-muted-foreground">Bank-level security with encrypted data protection for all your financial information.</p>
            </div>
            <div className="bg-card p-6 rounded-lg shadow-md text-center">
              <div className="mb-4 flex justify-center">
                <div className="h-16 w-16 rounded-full bg-accent/10 flex items-center justify-center">
                  <TrendingUp className="h-8 w-8 text-accent" />
                </div>
              </div>
              <h3 className="text-xl font-semibold mb-2">Best Rates</h3>
              <p className="text-muted-foreground">Compare loan offers from multiple banks to find the best interest rates and terms.</p>
            </div>
            <div className="bg-card p-6 rounded-lg shadow-md text-center">
              <div className="mb-4 flex justify-center">
                <div className="h-16 w-16 rounded-full bg-primary/10 flex items-center justify-center">
                  <Users className="h-8 w-8 text-primary" />
                </div>
              </div>
              <h3 className="text-xl font-semibold mb-2">Easy Management</h3>
              <p className="text-muted-foreground">Track all your loans in one place with our intuitive dashboard and tools.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Get Started?</h2>
          <p className="text-muted-foreground mb-8 max-w-2xl mx-auto">
            Join thousands of satisfied customers who have found their perfect loan through LoanHub. Start your application today!
          </p>
          <Button size="lg" className="bg-gradient-to-r from-primary to-accent" onClick={() => navigate("/signup")}>
            Create Your Account
          </Button>
        </div>
      </section>
    </div>
  );
};

export default Index;
