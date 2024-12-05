import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import Image from "next/image";
import React from "react";
import UploadFilesDailog from "@/app/dashboard/_components/UploadFilesDailog";
import { Paperclip, Send, SendHorizonal } from "lucide-react";

const SearchArea = () => {
  return (
    <div>
      <div className="p-5 flex items-center relative">
        <div className="relative w-full flex items-center">
          {/* Paperclip Button */}
          <UploadFilesDailog>
            <Button variant="ghost" className="absolute top-1/2 left-2 -translate-y-1/2 p-0 border-none shadow-none h-8 w-8" asChild>
              <Paperclip />
            </Button>
          </UploadFilesDailog>

          {/* Textarea with Send Button inside */}
          <div className="relative w-full">
            <Textarea className="pr-14 pl-14" />
            <Button
              variant="ghost"
              className="absolute top-1/2 right-2 -translate-y-1/2 p-0 border-none shadow-none h-8 w-8" asChild
            >
              <SendHorizonal />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SearchArea;
