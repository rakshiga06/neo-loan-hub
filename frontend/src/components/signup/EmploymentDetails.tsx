import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

interface EmploymentDetailsProps {
  formData: any;
  updateFormData: (data: any) => void;
}

const EmploymentDetails = ({ formData, updateFormData }: EmploymentDetailsProps) => {
  const handleChange = (field: string, value: any) => {
    updateFormData({ [field]: value });
  };

  const handleFileChange = (field: string, file: File | null) => {
    updateFormData({ [field]: file });
  };

  return (
    <div className="space-y-4 py-4">
      <div className="space-y-2">
        <Label htmlFor="employmentStatus">Employment Status *</Label>
        <Select value={formData.employmentStatus} onValueChange={(value) => handleChange("employmentStatus", value)}>
          <SelectTrigger>
            <SelectValue placeholder="Select employment status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="employed">Employed</SelectItem>
            <SelectItem value="self-employed">Self-employed</SelectItem>
            <SelectItem value="unemployed">Unemployed</SelectItem>
            <SelectItem value="student">Student</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="employerName">Employer Name & Address</Label>
        <Textarea
          id="employerName"
          value={formData.employerName}
          onChange={(e) => handleChange("employerName", e.target.value)}
          placeholder="Enter employer name and address"
          rows={2}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="jobTitle">Job Title / Position</Label>
        <Input
          id="jobTitle"
          value={formData.jobTitle}
          onChange={(e) => handleChange("jobTitle", e.target.value)}
          placeholder="Enter job title"
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="income">Monthly / Annual Income *</Label>
          <Input
            id="income"
            type="number"
            value={formData.income}
            onChange={(e) => handleChange("income", e.target.value)}
            placeholder="Enter income amount"
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="otherIncome">Other Income Sources</Label>
          <Input
            id="otherIncome"
            value={formData.otherIncome}
            onChange={(e) => handleChange("otherIncome", e.target.value)}
            placeholder="Enter other income (optional)"
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="incomeProof">Upload Income Proof *</Label>
        <Input
          id="incomeProof"
          type="file"
          onChange={(e) => handleFileChange("incomeProof", e.target.files?.[0] || null)}
          accept=".pdf,.jpg,.jpeg,.png"
        />
        <p className="text-xs text-muted-foreground">Accepted formats: PDF, JPG, PNG (Max 5MB)</p>
      </div>
    </div>
  );
};

export default EmploymentDetails;
