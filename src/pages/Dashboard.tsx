import { useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import EligibilityChecker from "@/components/dashboard/EligibilityChecker";
import LoanProducts from "@/components/dashboard/LoanProducts";
import LoanApplication from "@/components/dashboard/LoanApplication";
import LoanHistory from "@/components/dashboard/LoanHistory";
import Profile from "@/components/dashboard/Profile";

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState("eligibility");

  const renderContent = () => {
    switch (activeTab) {
      case "eligibility":
        return <EligibilityChecker />;
      case "products":
        return <LoanProducts />;
      case "application":
        return <LoanApplication />;
      case "history":
        return <LoanHistory />;
      case "profile":
        return <Profile />;
      default:
        return <EligibilityChecker />;
    }
  };

  return (
    <DashboardLayout activeTab={activeTab} setActiveTab={setActiveTab}>
      {renderContent()}
    </DashboardLayout>
  );
};

export default Dashboard;
