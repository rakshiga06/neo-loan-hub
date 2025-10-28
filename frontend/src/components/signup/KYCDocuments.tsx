import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface KYCDocumentsProps {
  formData: any;
  updateFormData: (data: any) => void;
}

const KYCDocuments = ({ formData, updateFormData }: KYCDocumentsProps) => {
  const handleFileChange = (field: string, file: File | null) => {
    updateFormData({ [field]: file });
  };

  return (
    <div className="space-y-4 py-4">
      <div className="space-y-2">
        <Label htmlFor="govId">Government ID Proof *</Label>
        <Input
          id="govId"
          type="file"
          onChange={(e) => handleFileChange("govId", e.target.files?.[0] || null)}
          accept=".pdf,.jpg,.jpeg,.png"
        />
        <p className="text-xs text-muted-foreground">Aadhar, Passport, Voter ID, Driving License</p>
      </div>

      <div className="space-y-2">
        <Label htmlFor="addressProof">Address Proof *</Label>
        <Input
          id="addressProof"
          type="file"
          onChange={(e) => handleFileChange("addressProof", e.target.files?.[0] || null)}
          accept=".pdf,.jpg,.jpeg,.png"
        />
        <p className="text-xs text-muted-foreground">Utility bill, Bank statement, Rent agreement</p>
      </div>

      <div className="space-y-2">
        <Label htmlFor="panCard">PAN Card / Tax ID *</Label>
        <Input
          id="panCard"
          type="file"
          onChange={(e) => handleFileChange("panCard", e.target.files?.[0] || null)}
          accept=".pdf,.jpg,.jpeg,.png"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="photo">Recent Photograph *</Label>
        <Input
          id="photo"
          type="file"
          onChange={(e) => handleFileChange("photo", e.target.files?.[0] || null)}
          accept=".jpg,.jpeg,.png"
        />
        <p className="text-xs text-muted-foreground">Passport size photo</p>
      </div>

      <div className="space-y-2">
        <Label htmlFor="otherDocs">Other Documents (Optional)</Label>
        <Input
          id="otherDocs"
          type="file"
          onChange={(e) => handleFileChange("otherDocs", e.target.files?.[0] || null)}
          accept=".pdf,.jpg,.jpeg,.png"
          multiple
        />
        <p className="text-xs text-muted-foreground">Any additional supporting documents</p>
      </div>
    </div>
  );
};

export default KYCDocuments;
