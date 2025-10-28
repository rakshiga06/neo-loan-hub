import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { FileText, Download, DollarSign } from "lucide-react";
import { toast } from "sonner";

const mockLoanHistory = [
  {
    id: "LN001234",
    bank: "HDFC Bank",
    type: "Personal Loan",
    amount: 500000,
    emi: 11000,
    status: "Active",
    remainingTenure: "24 months",
    disbursedDate: "2024-01-15",
  },
  {
    id: "LN001189",
    bank: "SBI",
    type: "Home Loan",
    amount: 3500000,
    emi: 32000,
    status: "Active",
    remainingTenure: "180 months",
    disbursedDate: "2023-06-20",
  },
  {
    id: "LN000987",
    bank: "ICICI Bank",
    type: "Car Loan",
    amount: 800000,
    emi: 0,
    status: "Completed",
    remainingTenure: "0 months",
    disbursedDate: "2020-03-10",
  },
  {
    id: "LN001456",
    bank: "Axis Bank",
    type: "Education Loan",
    amount: 1200000,
    emi: 0,
    status: "Pending",
    remainingTenure: "-",
    disbursedDate: "-",
  },
];

const LoanHistory = () => {
  const handleViewDetails = (id: string) => {
    toast.info(`Viewing details for loan ${id}`);
  };

  const handleDownloadStatement = (id: string) => {
    toast.success(`Downloading statement for loan ${id}`);
  };

  const handlePreclose = (id: string) => {
    toast.info(`Pre-closure request initiated for loan ${id}`);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "Active":
        return "bg-accent";
      case "Completed":
        return "bg-primary";
      case "Pending":
        return "bg-yellow-500";
      default:
        return "bg-gray-500";
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Loan History & Management</h1>
        <p className="text-muted-foreground">View and manage your loan applications</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">Active Loans</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">2</p>
            <p className="text-xs text-muted-foreground mt-1">Currently running</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">Total EMI</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">₹43,000</p>
            <p className="text-xs text-muted-foreground mt-1">Per month</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">Completed Loans</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">1</p>
            <p className="text-xs text-muted-foreground mt-1">Successfully closed</p>
          </CardContent>
        </Card>
      </div>

      {/* Loan History Table */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="w-5 h-5" />
            All Loans
          </CardTitle>
          <CardDescription>Complete history of your loan applications</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Loan ID</TableHead>
                <TableHead>Bank</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Amount</TableHead>
                <TableHead>EMI</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Remaining</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {mockLoanHistory.map((loan) => (
                <TableRow key={loan.id}>
                  <TableCell className="font-medium">{loan.id}</TableCell>
                  <TableCell>{loan.bank}</TableCell>
                  <TableCell>{loan.type}</TableCell>
                  <TableCell>₹{loan.amount.toLocaleString()}</TableCell>
                  <TableCell>{loan.emi > 0 ? `₹${loan.emi.toLocaleString()}` : "-"}</TableCell>
                  <TableCell>
                    <Badge className={getStatusColor(loan.status)}>{loan.status}</Badge>
                  </TableCell>
                  <TableCell>{loan.remainingTenure}</TableCell>
                  <TableCell>
                    <div className="flex gap-1">
                      <Button variant="ghost" size="sm" onClick={() => handleViewDetails(loan.id)}>
                        <FileText className="w-4 h-4" />
                      </Button>
                      {loan.status !== "Pending" && (
                        <Button variant="ghost" size="sm" onClick={() => handleDownloadStatement(loan.id)}>
                          <Download className="w-4 h-4" />
                        </Button>
                      )}
                      {loan.status === "Active" && (
                        <Button variant="ghost" size="sm" onClick={() => handlePreclose(loan.id)}>
                          <DollarSign className="w-4 h-4" />
                        </Button>
                      )}
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};

export default LoanHistory;
