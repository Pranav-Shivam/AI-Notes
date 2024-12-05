import React from "react";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

const UploadFilesDailog = ({ children }) => {
  return (
    <Dialog>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle className="text-xl font-bold ml-2">Upload a File</DialogTitle>
          <DialogDescription asChild>
            <div className="flex flex-col gap-3 rounded-md border border-slate-200 p-3">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-slate-700 "> Select a File to Upload </h2>
                <input type="file" />
              </div>
              <div className="mt-2">
                <label htmlFor="FileName" className="text-sm font-semibold text-slate-700"> File Name * </label>
                <Input type="text" id="FileName" className="w-full shadow-sm border-slate-200" />
              </div>
            </div>
          </DialogDescription>
        </DialogHeader>
        <DialogFooter className="sm:justify-end">
          <DialogClose asChild>
            <Button variant="destructive"> Cancel </Button>
          </DialogClose>
          <Button> Upload </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default UploadFilesDailog;
