import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "sonner";
import { FileText } from "lucide-react";

const LoanApplication = () => {
  const [formData, setFormData] = useState({
    bank: "",
    loanType: "",
    amount: "",
    tenure: "",
    purpose: "",
    documents: null,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.bank || !formData.loanType || !formData.amount) {
      toast.error("Please fill all required fields");
      return;
    }
    toast.success("Loan application submitted successfully!");
    setFormData({
      bank: "",
      loanType: "",
      amount: "",
      tenure: "",
      purpose: "",
      documents: null,
    });
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Apply for Loan</h1>
        <p className="text-muted-foreground">Submit a new loan application</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="w-5 h-5" />
            Loan Application Form
          </CardTitle>
          <CardDescription>Fill in the details to apply for a loan</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="bank">Select Bank *</Label>
                <Select value={formData.bank} onValueChange={(value) => setFormData({ ...formData, bank: value })}>
                  <SelectTrigger>
                    <SelectValue placeholder="Choose a bank" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="hdfc">HDFC Bank</SelectItem>
                    <SelectItem value="icici">ICICI Bank</SelectItem>
                    <SelectItem value="sbi">State Bank of India</SelectItem>
                    <SelectItem value="axis">Axis Bank</SelectItem>
                    <SelectItem value="kotak">Kotak Mahindra Bank</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="loanType">Loan Type *</Label>
                <Select value={formData.loanType} onValueChange={(value) => setFormData({ ...formData, loanType: value })}>
                  <SelectTrigger>
                    <SelectValue placeholder="Choose loan type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="personal">Personal Loan</SelectItem>
                    <SelectItem value="home">Home Loan</SelectItem>
                    <SelectItem value="car">Car Loan</SelectItem>
                    <SelectItem value="education">Education Loan</SelectItem>
                    <SelectItem value="business">Business Loan</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="amount">Loan Amount (₹) *</Label>
                <Input
                  id="amount"
                  type="number"
                  placeholder="Enter loan amount"
                  value={formData.amount}
                  onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="tenure">Tenure (Months) *</Label>
                <Input
                  id="tenure"
                  type="number"
                  placeholder="Enter tenure in months"
                  value={formData.tenure}
                  onChange={(e) => setFormData({ ...formData, tenure: e.target.value })}
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="purpose">Purpose of Loan</Label>
              <Textarea
                id="purpose"
                placeholder="Describe the purpose of the loan"
                value={formData.purpose}
                onChange={(e) => setFormData({ ...formData, purpose: e.target.value })}
                rows={3}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="documents">Upload Additional Documents</Label>
              <Input
                id="documents"
                type="file"
                onChange={(e) => setFormData({ ...formData, documents: e.target.files?.[0] as any })}
                accept=".pdf,.jpg,.jpeg,.png"
                multiple
              />
              <p className="text-xs text-muted-foreground">Upload any additional supporting documents</p>
            </div>

            <div className="bg-secondary p-4 rounded-lg">
              <h4 className="font-semibold mb-2">Pre-filled Information</h4>
              <p className="text-sm text-muted-foreground">Your personal, financial, and employment details from registration will be automatically included with this application.</p>
            </div>

            <Button type="submit" className="w-full bg-gradient-to-r from-primary to-accent">
              Submit Application
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default LoanApplication;
