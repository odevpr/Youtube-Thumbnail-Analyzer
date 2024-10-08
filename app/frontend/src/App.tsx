import React from "react";
import ThumbnailUpload from "./components/ThumbnailUpload";

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <h1 className="text-4xl text-center font-bold mb-6">YouTube Thumbnail Analyzer</h1>
      <div className="max-w-md mx-auto bg-white rounded-xl shadow-lg p-6">
        <ThumbnailUpload />
      </div>
    </div>
  );
};

export default App;
