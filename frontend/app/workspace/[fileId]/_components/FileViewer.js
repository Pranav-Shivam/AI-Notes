import React from "react";

const FileViewer = ({ fileUrl }) => {
    // console.log("Printing ......",fileUrl);
  return (
    <div className="h-[90vh] bg-gray-100">
      <iframe
        src={fileUrl+"#toolbar=0"}
        width="100%"
        height="100%"
        title="File Viewer"
        style={{ border: "none" }}
        className="h-[90vh]"
      />
    </div>
  );
};

export default FileViewer;
