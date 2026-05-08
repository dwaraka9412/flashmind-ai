import "./App.css";
import axios from "axios";
import { useState } from "react";

import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

function App() {

  const [files, setFiles] = useState([]);
  const [message, setMessage] = useState("");
  const [duplicates, setDuplicates] = useState([]);
  const [stats, setStats] = useState(null);
  const [plotData, setPlotData] = useState([]);
  const [cleanedFlashcards, setCleanedFlashcards] = useState([]);
  const [hallucinations, setHallucinations] = useState([]);

  const handleUpload = async () => {

    if (files.length === 0) {
      alert("Please select files");
      return;
    }

    const formData = new FormData();

    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i], files[i].name);
    }

    try {

      const response = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData
      );

      setMessage(response.data.message);
      setDuplicates(response.data.duplicates);
      setStats(response.data);
      setPlotData(response.data.plot_data);
      setHallucinations(response.data.hallucinations);
      setCleanedFlashcards(response.data.cleaned_flashcards);

      console.log(response.data);

    } catch (error) {

      console.log(error);
      setMessage("Upload Failed");
    }
  };

  const downloadCleanedFile = () => {

    const text = cleanedFlashcards.join("\n");

    const blob = new Blob(
      [text],
      { type: "text/plain" }
    );

    const link = document.createElement("a");

    link.href = URL.createObjectURL(blob);

    link.download = "cleaned_flashcards.txt";

    link.click();
  };

  return (

    <div className="app">

      <div className="navbar">
        <h1>FLASHMIND AI</h1>
      </div>

      <div className="hero">

        <h2>AI Flashcard De-Duplicator</h2>

        <p>
          Upload multiple TXT files and let AI
          detect duplicate flashcards intelligently.
        </p>

        <input
          type="file"
          multiple
          onChange={(e) => setFiles(e.target.files)}
        />

        <br /><br />

        <button
          className="btn"
          onClick={handleUpload}
        >
          Analyze Flashcards
        </button>

        <h3>{message}</h3>

        {
          cleanedFlashcards.length > 0 && (

            <button
              className="btn"
              onClick={downloadCleanedFile}
            >
              Download Cleaned Flashcards
            </button>

          )
        }

      </div>

      {
        stats && (

          <div className="dashboard">

            <div className="stat-card">
              <h2>{stats.total_flashcards}</h2>
              <p>Total Flashcards</p>
            </div>

            <div className="stat-card">
              <h2>{stats.duplicate_count}</h2>
              <p>Duplicates Found</p>
            </div>

            <div className="stat-card">
              <h2>{stats.unique_flashcards}</h2>
              <p>Unique Flashcards</p>
            </div>

            <div className="stat-card">
              <h2>{stats.average_similarity}%</h2>
              <p>Average Similarity</p>
            </div>

          </div>

        )
      }

      {
        plotData.length > 0 && (

          <div className="chart-container">

            <h2>Semantic Flashcard Clustering</h2>

            <ResponsiveContainer width="100%" height={400}>

              <ScatterChart>

                <CartesianGrid />

                <XAxis
                  type="number"
                  dataKey="x"
                />

                <YAxis
                  type="number"
                  dataKey="y"
                />

                <Tooltip
                  cursor={{ strokeDasharray: "3 3" }}
                  formatter={(value, name, props) => [
                    props.payload.name
                  ]}
                />

                <Scatter
                  data={plotData}
                  fill="#00ffff"
                />

              </ScatterChart>

            </ResponsiveContainer>

          </div>

        )
      }

      {
          hallucinations.length > 0  && (

          <div className="hallucination-box">

            <h2>AI Hallucination Detection</h2>
            <p>
  Total Hallucinations:
  {hallucinations.length}
</p>

            {
              hallucinations.map((item, index) => (

                <div
                  className="warning-card"
                  key={index}
                >

                  <p>
                    ⚠ {item.flashcard}
                  </p>

                  <p>
                    {item.warning}
                  </p>
                  

                </div>

              ))
            }

          </div>

        )
      }

      <div className="results">

        <h2>Duplicate Flashcards</h2>

        {
          duplicates.map((item, index) => (

            <div className="card" key={index}>

              <p>
                <strong>Flashcard 1:</strong>
                <br />
                {item.flashcard1}
              </p>

              <p>
                <strong>Flashcard 2:</strong>
                <br />
                {item.flashcard2}
              </p>

              <p>
                <strong>Similarity:</strong>{" "}
                {(item.score * 100).toFixed(2)}%
              </p>

            </div>

          ))
        }

      </div>

    </div>
  );
}

export default App;