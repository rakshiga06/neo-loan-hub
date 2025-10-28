import { ReactNode } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Building2, Calculator, ShoppingCart, FileText, History, User, LogOut } from "lucide-react";

interface DashboardLayoutProps {
  children: ReactNode;
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const DashboardLayout = ({ children, activeTab, setActiveTab }: DashboardLayoutProps) => {
  const navigate = useNavigate();

  const navItems = [
    { id: "eligibility", label: "Eligibility Checker", icon: Calculator },
    { id: "products", label: "Loan Products", icon: ShoppingCart },
    { id: "application", label: "Apply for Loan", icon: FileText },
    { id: "history", label: "Loan History", icon: History },
    { id: "profile", label: "Profile & Settings", icon: User },
  ];

  return (
    <div className="min-h-screen bg-background flex">
      {/* Sidebar */}
      <aside className="w-64 border-r bg-card flex flex-col">
        <div className="p-6 flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center">
            <Building2 className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-lg">LoanHub</h1>
            <p className="text-xs text-muted-foreground">Loan Management</p>
          </div>
        </div>
        <Separator />
        <nav className="flex-1 p-4 space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <Button
                key={item.id}
                variant={isActive ? "secondary" : "ghost"}
                className={`w-full justify-start ${isActive ? "bg-primary/10 text-primary" : ""}`}
                onClick={() => setActiveTab(item.id)}
              >
                <Icon className="w-4 h-4 mr-3" />
                {item.label}
              </Button>
            );
          })}
        </nav>
        <Separator />
        <div className="p-4">
          <Button variant="outline" className="w-full" onClick={() => navigate("/login")}>
            <LogOut className="w-4 h-4 mr-2" />
            Logout
          </Button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <div className="p-8">{children}</div>
      </main>
    </div>
  );
};

export default DashboardLayout;
