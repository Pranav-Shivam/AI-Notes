import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { LayoutDashboard, Shield } from "lucide-react";
import Image from "next/image";
import React from "react";
import UploadFilesDailog from "./UploadFilesDailog";

const SideBar = () => {
  return (
    <div className="shadow-md h-screen p-7">
      <Image src={"/logo.svg"} height={120} width={180} alt="logo" />
      <div className="mt-10">
        <UploadFilesDailog>
          <Button className="w-full">+ Upload File</Button>
        </UploadFilesDailog>

        <div className="flex items-center gap-3 mt-5 pd-3 hover:bg-slate-100 p-3 rounded-lg cursor-pointer">
          <LayoutDashboard />
          <h2>Dashboard</h2>
        </div>
        <div className="flex items-center gap-3 mt-1 pd-3 hover:bg-slate-100 p-3 rounded-lg cursor-pointer">
          <Shield />
          <h2>Upgarde</h2>
        </div>
      </div>
      <div className="absolute bottom-20 w-[80%] text-center">
        <Progress value={40} />
        <p className="text-lg mt-1">2 out of 5 Files uploaded</p>
        <p className="text-lg mt-1 text-slate-500">Upgrade to Pro</p>
      </div>
    </div>
  );
};

export default SideBar;
