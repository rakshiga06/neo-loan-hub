import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

interface FinancialDetailsProps {
  formData: any;
  updateFormData: (data: any) => void;
}

const FinancialDetails = ({ formData, updateFormData }: FinancialDetailsProps) => {
  const handleChange = (field: string, value: any) => {
    updateFormData({ [field]: value });
  };

  return (
    <div className="space-y-4 py-4">
      <div className="space-y-2">
        <Label htmlFor="existingLoans">Existing Loans / Liabilities</Label>
        <Input
          id="existingLoans"
          value={formData.existingLoans}
          onChange={(e) => handleChange("existingLoans", e.target.value)}
          placeholder="Enter existing loans or liabilities"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="monthlyEMI">Monthly EMI / Debt Obligations</Label>
        <Input
          id="monthlyEMI"
          type="number"
          value={formData.monthlyEMI}
          onChange={(e) => handleChange("monthlyEMI", e.target.value)}
          placeholder="Enter monthly EMI amount"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="assets">Assets Owned</Label>
        <Textarea
          id="assets"
          value={formData.assets}
          onChange={(e) => handleChange("assets", e.target.value)}
          placeholder="List your assets (property, vehicles, etc.)"
          rows={3}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="bankDetails">Bank Account Details *</Label>
        <Textarea
          id="bankDetails"
          value={formData.bankDetails}
          onChange={(e) => handleChange("bankDetails", e.target.value)}
          placeholder="Enter bank name, account number, IFSC code"
          rows={3}
        />
      </div>
    </div>
  );
};

export default FinancialDetails;
