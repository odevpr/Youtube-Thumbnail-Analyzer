import React, { useState } from "react";
import axios from "axios";

interface Feedback {
  score: number;
  comment: string;
}

const ThumbnailUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setFile(event.target.files ? event.target.files[0] : null);
    setFeedback(null); // Reset feedback on file change
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!file) {
      setError("Please upload a file first.");
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post<Feedback>("http://localhost:8000/analyze-thumbnail/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setFeedback(response.data);
    } catch (error: any) {
      setError("Error analyzing the thumbnail. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="thumbnail" className="block text-sm font-medium text-gray-700">
            Upload YouTube Thumbnail
          </label>
          <input
            type="file"
            accept="image/*"
            id="thumbnail"
            onChange={handleFileChange}
            className="mt-1 block w-full text-sm text-gray-900 border-gray-300 rounded-lg shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-600 transition"
        >
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>

      {error && <p className="mt-4 text-red-500">{error}</p>}

      {feedback && (
        <div className="mt-6 p-4 bg-gray-100 rounded-lg shadow-inner">
          <h2 className="text-lg font-bold mb-2">Analysis Result:</h2>
          <p><strong>Score:</strong> {feedback.score}/10</p>
          <p><strong>Comment:</strong> {feedback.comment}</p>
        </div>
      )}
    </div>
  );
};

export default ThumbnailUpload;
