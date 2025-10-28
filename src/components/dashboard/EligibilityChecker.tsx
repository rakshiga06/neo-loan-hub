import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Calculator } from "lucide-react";
import { toast } from "sonner";

const EligibilityChecker = () => {
  const [formData, setFormData] = useState({
    loanAmount: "",
    interestRate: "",
    tenure: "",
    monthlyIncome: "",
  });
  const [result, setResult] = useState<any>(null);

  const calculateEligibility = () => {
    const { loanAmount, interestRate, tenure, monthlyIncome } = formData;

    if (!loanAmount || !interestRate || !tenure || !monthlyIncome) {
      toast.error("Please fill all fields");
      return;
    }

    const P = parseFloat(loanAmount);
    const r = parseFloat(interestRate) / 12 / 100;
    const n = parseFloat(tenure) * 12;
    const income = parseFloat(monthlyIncome);

    // EMI = [P x R x (1+R)^N]/[(1+R)^N-1]
    const emi = (P * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);

    // Max eligible amount (40% of income as EMI)
    const maxEligible = (income * 0.4 * (Math.pow(1 + r, n) - 1)) / (r * Math.pow(1 + r, n));

    // Recommended banks based on amount
    const banks = ["HDFC Bank", "ICICI Bank", "SBI", "Axis Bank", "Kotak Mahindra"];

    setResult({
      emi: emi.toFixed(2),
      maxEligible: maxEligible.toFixed(2),
      recommendedBanks: banks.slice(0, 3),
      totalPayment: (emi * n).toFixed(2),
      totalInterest: (emi * n - P).toFixed(2),
    });

    toast.success("Eligibility calculated successfully!");
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Loan Eligibility Checker</h1>
        <p className="text-muted-foreground">Calculate your loan eligibility and EMI</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calculator className="w-5 h-5" />
              Enter Details
            </CardTitle>
            <CardDescription>Fill in the loan details to check eligibility</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="loanAmount">Loan Amount (₹)</Label>
              <Input
                id="loanAmount"
                type="number"
                placeholder="e.g., 500000"
                value={formData.loanAmount}
                onChange={(e) => setFormData({ ...formData, loanAmount: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="interestRate">Interest Rate (% per annum)</Label>
              <Input
                id="interestRate"
                type="number"
                step="0.1"
                placeholder="e.g., 9.5"
                value={formData.interestRate}
                onChange={(e) => setFormData({ ...formData, interestRate: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="tenure">Loan Tenure (Years)</Label>
              <Input
                id="tenure"
                type="number"
                placeholder="e.g., 5"
                value={formData.tenure}
                onChange={(e) => setFormData({ ...formData, tenure: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="monthlyIncome">Monthly Income (₹)</Label>
              <Input
                id="monthlyIncome"
                type="number"
                placeholder="e.g., 50000"
                value={formData.monthlyIncome}
                onChange={(e) => setFormData({ ...formData, monthlyIncome: e.target.value })}
              />
            </div>
            <Button className="w-full bg-gradient-to-r from-primary to-accent" onClick={calculateEligibility}>
              Calculate Eligibility
            </Button>
          </CardContent>
        </Card>

        {result && (
          <Card className="border-accent">
            <CardHeader>
              <CardTitle className="text-accent">Results</CardTitle>
              <CardDescription>Your loan eligibility details</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="p-4 bg-secondary rounded-lg">
                <p className="text-sm text-muted-foreground">Monthly EMI</p>
                <p className="text-2xl font-bold text-primary">₹{result.emi}</p>
              </div>
              <div className="p-4 bg-secondary rounded-lg">
                <p className="text-sm text-muted-foreground">Maximum Eligible Amount</p>
                <p className="text-2xl font-bold text-accent">₹{result.maxEligible}</p>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="p-3 bg-secondary rounded-lg">
                  <p className="text-xs text-muted-foreground">Total Payment</p>
                  <p className="text-lg font-semibold">₹{result.totalPayment}</p>
                </div>
                <div className="p-3 bg-secondary rounded-lg">
                  <p className="text-xs text-muted-foreground">Total Interest</p>
                  <p className="text-lg font-semibold">₹{result.totalInterest}</p>
                </div>
              </div>
              <div className="space-y-2">
                <p className="text-sm font-semibold">Recommended Banks:</p>
                <ul className="space-y-1">
                  {result.recommendedBanks.map((bank: string) => (
                    <li key={bank} className="text-sm text-muted-foreground flex items-center gap-2">
                      <span className="w-2 h-2 bg-accent rounded-full"></span>
                      {bank}
                    </li>
                  ))}
                </ul>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default EligibilityChecker;
