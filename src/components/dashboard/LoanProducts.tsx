import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Building, TrendingDown, Calendar, FileText } from "lucide-react";
import { toast } from "sonner";

const mockLoans = [
  {
    id: 1,
    bank: "HDFC Bank",
    type: "Personal Loan",
    interestRate: 10.5,
    processingFee: "2%",
    tenure: "12-60 months",
    minAmount: 50000,
    maxAmount: 2500000,
  },
  {
    id: 2,
    bank: "ICICI Bank",
    type: "Home Loan",
    interestRate: 8.5,
    processingFee: "0.5%",
    tenure: "60-360 months",
    minAmount: 500000,
    maxAmount: 10000000,
  },
  {
    id: 3,
    bank: "SBI",
    type: "Education Loan",
    interestRate: 9.0,
    processingFee: "1%",
    tenure: "36-120 months",
    minAmount: 100000,
    maxAmount: 2000000,
  },
  {
    id: 4,
    bank: "Axis Bank",
    type: "Car Loan",
    interestRate: 9.25,
    processingFee: "1.5%",
    tenure: "12-84 months",
    minAmount: 100000,
    maxAmount: 5000000,
  },
  {
    id: 5,
    bank: "Kotak Mahindra",
    type: "Business Loan",
    interestRate: 11.0,
    processingFee: "2.5%",
    tenure: "12-48 months",
    minAmount: 200000,
    maxAmount: 5000000,
  },
];

const LoanProducts = () => {
  const [filters, setFilters] = useState({
    minRate: "",
    maxRate: "",
    bank: "",
  });

  const filteredLoans = mockLoans.filter((loan) => {
    if (filters.minRate && loan.interestRate < parseFloat(filters.minRate)) return false;
    if (filters.maxRate && loan.interestRate > parseFloat(filters.maxRate)) return false;
    if (filters.bank && !loan.bank.toLowerCase().includes(filters.bank.toLowerCase())) return false;
    return true;
  });

  const handleApply = (loan: any) => {
    toast.success(`Application initiated for ${loan.bank} ${loan.type}`);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Loan Products</h1>
        <p className="text-muted-foreground">Browse and compare loan offers from various banks</p>
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle>Filter Loans</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label htmlFor="minRate">Min Interest Rate (%)</Label>
              <Input
                id="minRate"
                type="number"
                step="0.1"
                placeholder="e.g., 8"
                value={filters.minRate}
                onChange={(e) => setFilters({ ...filters, minRate: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="maxRate">Max Interest Rate (%)</Label>
              <Input
                id="maxRate"
                type="number"
                step="0.1"
                placeholder="e.g., 12"
                value={filters.maxRate}
                onChange={(e) => setFilters({ ...filters, maxRate: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="bank">Bank Name</Label>
              <Input
                id="bank"
                placeholder="Search by bank name"
                value={filters.bank}
                onChange={(e) => setFilters({ ...filters, bank: e.target.value })}
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Loan Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredLoans.map((loan) => (
          <Card key={loan.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                    <Building className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <CardTitle className="text-lg">{loan.bank}</CardTitle>
                    <CardDescription>{loan.type}</CardDescription>
                  </div>
                </div>
                <Badge variant="secondary">{loan.interestRate}%</Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground flex items-center gap-1">
                    <TrendingDown className="w-4 h-4" />
                    Interest Rate
                  </span>
                  <span className="font-semibold">{loan.interestRate}% p.a.</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground flex items-center gap-1">
                    <FileText className="w-4 h-4" />
                    Processing Fee
                  </span>
                  <span className="font-semibold">{loan.processingFee}</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground flex items-center gap-1">
                    <Calendar className="w-4 h-4" />
                    Tenure
                  </span>
                  <span className="font-semibold">{loan.tenure}</span>
                </div>
              </div>
              <div className="pt-2 border-t">
                <p className="text-xs text-muted-foreground mb-1">Loan Amount Range</p>
                <p className="text-sm font-semibold">
                  ₹{loan.minAmount.toLocaleString()} - ₹{loan.maxAmount.toLocaleString()}
                </p>
              </div>
              <Button className="w-full bg-gradient-to-r from-primary to-accent" onClick={() => handleApply(loan)}>
                Apply Now
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default LoanProducts;
