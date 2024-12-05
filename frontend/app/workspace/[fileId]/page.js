"use client";
import React, { useEffect, useState } from "react";
import WorkspaceHeader from "./_components/WorkspaceHeader";
import { useParams } from "next/navigation";
import FileViewer from "./_components/FileViewer";
import TextEditor from "./_components/TextEditor";
import documentsApi from "@/app/api/clients/documentsApi";

const Workspace = () => {
  const { fileId } = useParams();
  const [documentData, setDocumentData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDocument = async () => {
      if (!fileId) return;

      try {
        setLoading(true);
        const response = await documentsApi.getDocumentById(fileId);
        setDocumentData(response);
      } catch (err) {
        console.error('Error fetching document:', err);
        setError(err.message || 'Failed to load document');
      } finally {
        setLoading(false);
      }
    };

    fetchDocument();
  }, [fileId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen text-red-500">
        Error: {error}
      </div>
    );
  }

  return (
    <div className="overflow-hidden h-screen">
      <WorkspaceHeader />
      <div className="grid grid-cols-2 gap-5 h-[calc(100vh-64px)]">
        <div>
          <TextEditor />
        </div>
        <div className="overflow-y-auto">
          {documentData && <FileViewer fileUrl={documentData.url} />}
        </div>
      </div>
    </div>
  );
};

export default Workspace;
