
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Progress } from "@/components/ui/progress";
import { toast } from "sonner";
import PersonalDetails from "@/components/signup/PersonalDetails";
import FinancialDetails from "@/components/signup/FinancialDetails";
import EmploymentDetails from "@/components/signup/EmploymentDetails";
import KYCDocuments from "@/components/signup/KYCDocuments";
import { Building2 } from "lucide-react";

const Signup = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    // Personal
    fullName: "",
    dob: "",
    gender: "",
    nationality: "",
    maritalStatus: "",
    contact: "",
    email: "",
    password: "",
    confirmPassword: "",
    address: "",
    
    // Financial
    existingLoans: "",
    monthlyEMI: "",
    assets: "",
    bankDetails: "",
    // Employment
    employmentStatus: "",
    employerName: "",
    jobTitle: "",
    income: "",
    otherIncome: "",
    incomeProof: null,
    // KYC
    govId: null,
    addressProof: null,
    panCard: null,
    photo: null,
    otherDocs: null,
  });

  const [completedSections, setCompletedSections] = useState<string[]>([]);

  const updateFormData = (section: string, data: any) => {
    setFormData({ ...formData, ...data });
    if (!completedSections.includes(section)) {
      setCompletedSections([...completedSections, section]);
    }
  };

  const progress = (completedSections.length / 4) * 100;

  const handleSubmit = async () => {
    if (completedSections.length < 4) {
      toast.error("Please complete all sections");
      return;
    }
  
    try {
      const response = await fetch("/api/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...formData,
          // ensure it's a string
        })
      });
  
      if (!response.ok) {
        const error = await response.json();
        toast.error(error.msg || "Something went wrong");
        return;
      }
  
      toast.success("Registration successful! Please login.");
      navigate("/login");
    } catch (err) {
      toast.error("Network error, please try again");
    }
  };
  

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <Card className="w-full max-w-3xl shadow-lg">
        <CardHeader className="text-center space-y-4">
          <div className="flex justify-center">
            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center">
              <Building2 className="w-6 h-6 text-white" />
            </div>
          </div>
          <CardTitle className="text-3xl font-bold">Create Your Account</CardTitle>
          <CardDescription>Complete all sections to register for loan services</CardDescription>
          <div className="space-y-2">
            <Progress value={progress} className="h-2" />
            <p className="text-sm text-muted-foreground">{completedSections.length} of 4 sections completed</p>
          </div>
        </CardHeader>
        <CardContent>
          <Accordion type="single" collapsible className="space-y-4">
            <AccordionItem value="personal" className="border rounded-lg px-4">
              <AccordionTrigger className="hover:no-underline">
                <span className="flex items-center gap-2">
                  Personal Details
                  {completedSections.includes("personal") && <span className="text-accent">✓</span>}
                </span>
              </AccordionTrigger>
              <AccordionContent>
                <PersonalDetails formData={formData} updateFormData={(data) => updateFormData("personal", data)} />
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="financial" className="border rounded-lg px-4">
              <AccordionTrigger className="hover:no-underline">
                <span className="flex items-center gap-2">
                  Financial Details
                  {completedSections.includes("financial") && <span className="text-accent">✓</span>}
                </span>
              </AccordionTrigger>
              <AccordionContent>
                <FinancialDetails formData={formData} updateFormData={(data) => updateFormData("financial", data)} />
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="employment" className="border rounded-lg px-4">
              <AccordionTrigger className="hover:no-underline">
                <span className="flex items-center gap-2">
                  Employment Details
                  {completedSections.includes("employment") && <span className="text-accent">✓</span>}
                </span>
              </AccordionTrigger>
              <AccordionContent>
                <EmploymentDetails formData={formData} updateFormData={(data) => updateFormData("employment", data)} />
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="kyc" className="border rounded-lg px-4">
              <AccordionTrigger className="hover:no-underline">
                <span className="flex items-center gap-2">
                  KYC / Document Uploads
                  {completedSections.includes("kyc") && <span className="text-accent">✓</span>}
                </span>
              </AccordionTrigger>
              <AccordionContent>
                <KYCDocuments formData={formData} updateFormData={(data) => updateFormData("kyc", data)} />
              </AccordionContent>
            </AccordionItem>
          </Accordion>

          <div className="mt-6 flex gap-4">
            <Button variant="outline" className="flex-1" onClick={() => navigate("/login")}>
              Already have an account?
            </Button>
            <Button className="flex-1 bg-gradient-to-r from-primary to-accent" onClick={handleSubmit}>
              Submit & Register
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Signup;
