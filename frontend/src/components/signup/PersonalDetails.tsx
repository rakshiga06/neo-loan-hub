import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { CalendarIcon } from "lucide-react";
import { format } from "date-fns";
import { cn } from "@/lib/utils";

interface PersonalDetailsProps {
  formData: any;
  updateFormData: (data: any) => void;
}

const PersonalDetails = ({ formData, updateFormData }: PersonalDetailsProps) => {

  // Update single field in formData
  const handleChange = (field: string, value: any) => {
    updateFormData({ ...formData, [field]: value });
  };

  // Save profile or register + save if token not found
  const handleProfileSave = async () => {
    try {
      // 1️⃣ Password validation
      if (formData.password && formData.password !== formData.confirmPassword) {
        alert("Passwords do not match");
        return;
      }

      // 2️⃣ Email validation
      if (!formData.email || !formData.email.includes("@")) {
        alert("Please enter a valid email address");
        return;
      }

      // 3️⃣ Contact number validation (digits only)
      if (!formData.contact || !/^\+?\d{10,15}$/.test(formData.contact)) {
        alert("Please enter a valid contact number");
        return;
      }

      // 4️⃣ Token from localStorage
      let token = localStorage.getItem("token");

      // 5️⃣ Register user if no token
      if (!token) {
        const regPayload = {
          full_name: formData.fullName || "",
          email: formData.email,
          contact_number: formData.contact || "",
          password: formData.password || "Passw0rd1!",
          date_of_birth: formData.dob ? formData.dob.slice(0, 10) : "",
          permanent_address: formData.address || "",
          gender: formData.gender ? formData.gender.charAt(0).toUpperCase() + formData.gender.slice(1) : "",
          marital_status: formData.maritalStatus ? formData.maritalStatus.charAt(0).toUpperCase() + formData.maritalStatus.slice(1) : "",
          nationality: formData.nationality || "",
           // ✅ Required by backend
        };

        const regRes = await fetch("http://localhost:5000/api/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(regPayload),
        });

        const regData = await regRes.json();
        if (!regRes.ok) {
          alert(regData.msg || "Signup failed");
          return;
        }

        token = regData.access_token;
        localStorage.setItem("token", token);
      }

      // 6️⃣ Profile update payload
      const payload = {
        full_name: formData.fullName || "",
        contact_number: formData.contact || "",
        permanent_address: formData.address || "",
        gender: formData.gender ? formData.gender.charAt(0).toUpperCase() + formData.gender.slice(1) : "",
        marital_status: formData.maritalStatus ? formData.maritalStatus.charAt(0).toUpperCase() + formData.maritalStatus.slice(1) : "",
        nationality: formData.nationality || "",
        date_of_birth: formData.dob ? formData.dob.slice(0, 10) : "",
        // ✅ always string
      };

      console.log("Token:", token);
      console.log("Payload:", payload);

      const res = await fetch("http://localhost:5000/api/users/profile", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.msg || "Failed to save profile");
        return;
      }

      alert("Profile saved successfully!");
    } catch (err) {
      console.error("Error saving profile:", err);
      alert("An unexpected error occurred.");
    }
  };

  return (
    <div className="space-y-4 py-4">
      {/* Full Name & DOB */}
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="fullName">Full Name *</Label>
          <Input
            id="fullName"
            value={formData.fullName}
            onChange={(e) => handleChange("fullName", e.target.value)}
            placeholder="Enter your full name"
          />
        </div>
        <div className="space-y-2">
          <Label>Date of Birth *</Label>
          <Popover>
            <PopoverTrigger asChild>
              <Button
                variant="outline"
                className={cn("w-full justify-start text-left font-normal", !formData.dob && "text-muted-foreground")}
              >
                <CalendarIcon className="mr-2 h-4 w-4" />
                {formData.dob ? format(new Date(formData.dob), "PPP") : "Pick a date"}
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-auto p-0" align="start">
              <Calendar
                mode="single"
                selected={formData.dob ? new Date(formData.dob) : undefined}
                onSelect={(date) => handleChange("dob", date?.toISOString())}
                disabled={(date) => date > new Date() || date < new Date("1900-01-01")}
                initialFocus
                className="pointer-events-auto"
              />
            </PopoverContent>
          </Popover>
        </div>
      </div>

      {/* Gender & Nationality */}
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="gender">Gender *</Label>
          <Select value={formData.gender} onValueChange={(value) => handleChange("gender", value)}>
            <SelectTrigger>
              <SelectValue placeholder="Select gender" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="male">Male</SelectItem>
              <SelectItem value="female">Female</SelectItem>
              <SelectItem value="other">Other</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div className="space-y-2">
          <Label htmlFor="nationality">Nationality *</Label>
          <Input
            id="nationality"
            value={formData.nationality}
            onChange={(e) => handleChange("nationality", e.target.value)}
            placeholder="Enter nationality"
          />
        </div>
      </div>

      {/* Marital Status & Contact */}
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="maritalStatus">Marital Status *</Label>
          <Select value={formData.maritalStatus} onValueChange={(value) => handleChange("maritalStatus", value)}>
            <SelectTrigger>
              <SelectValue placeholder="Select status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="single">Single</SelectItem>
              <SelectItem value="married">Married</SelectItem>
              <SelectItem value="divorced">Divorced</SelectItem>
              <SelectItem value="widowed">Widowed</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div className="space-y-2">
          <Label htmlFor="contact">Contact Number *</Label>
          <Input
            id="contact"
            type="tel"
            value={formData.contact}
            onChange={(e) => handleChange("contact", e.target.value)}
            placeholder="Enter contact number"
          />
        </div>
      </div>

      {/* Email & Password */}
      <div className="space-y-2">
        <Label htmlFor="email">Email Address *</Label>
        <Input
          id="email"
          type="email"
          value={formData.email}
          onChange={(e) => handleChange("email", e.target.value)}
          placeholder="Enter email address"
        />
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="password">Password *</Label>
          <Input
            id="password"
            type="password"
            value={formData.password}
            onChange={(e) => handleChange("password", e.target.value)}
            placeholder="Enter password"
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="confirmPassword">Confirm Password *</Label>
          <Input
            id="confirmPassword"
            type="password"
            value={formData.confirmPassword}
            onChange={(e) => handleChange("confirmPassword", e.target.value)}
            placeholder="Confirm password"
          />
        </div>
      </div>

      {/* Address */}
      <div className="space-y-2">
        <Label htmlFor="address">Permanent Address *</Label>
        <Textarea
          id="address"
          value={formData.address}
          onChange={(e) => handleChange("address", e.target.value)}
          placeholder="Enter permanent address"
          rows={3}
        />
      </div>

      {/* Subject */}
      <div className="space-y-2">
        <Label htmlFor="subject">Subject</Label>
        <Input
          id="subject"
          value={formData.subject || ""}
          onChange={(e) => handleChange("subject", e.target.value)}
          placeholder="Enter subject (optional)"
        />
      </div>

      <Button onClick={handleProfileSave}>Save Personal Details</Button>
    </div>
  );
};

export default PersonalDetails;
