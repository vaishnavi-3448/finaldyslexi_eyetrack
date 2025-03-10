import { useState, useEffect } from 'react';
import io from 'socket.io-client';

function App() {
    const [status, setStatus] = useState('Not Tracking');
    const [gazeData, setGazeData] = useState([]);
    const [score, setScore] = useState(null);
    const [showPopup, setShowPopup] = useState(false);

  
    useEffect(() => {
        const socket = io("http://localhost:5000");

        socket.on("gaze-data", (data) => {
            setGazeData(prevData => [...prevData, data]); 
        });

        socket.on("final-score", (data) => {
            setScore(data.score);  
            setShowPopup(true);    
        });

        return () => socket.disconnect();
    }, []);

    const startTracking = async () => {
        const res = await fetch('http://localhost:5000/start-test');
        const data = await res.json();
        if (res.ok) {
            setStatus('Tracking Started');
            setScore(null);  
            setShowPopup(false);
            setGazeData([]);
        } else {
            alert(data.message);
        }
    };

    const stopTracking = async () => {
        const res = await fetch('http://localhost:5000/stop-test');
        const data = await res.json();
        if (res.ok) {
            setStatus('Tracking Stopped');
        } else {
            alert(data.message);
        }
    };

    return (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <h1>Gaze Tracking App</h1>
            <h2>Status: {status}</h2>
            <button onClick={startTracking}>Start Tracking</button>
            <button onClick={stopTracking} style={{ marginLeft: '10px' }}>Stop Tracking</button>

            <h3>Gaze Data:</h3>
            <ul>
                {gazeData.map((entry, index) => (
                    <li key={index}>
                        {new Date(entry.timestamp * 1000).toLocaleTimeString()} - {entry.gaze_focus}
                    </li>
                ))}
            </ul>

            {/* Score Popup */}
            {showPopup && (
                <div style={{
                    position: "fixed", 
                    top: "50%", left: "50%", 
                    transform: "translate(-50%, -50%)",
                    backgroundColor: "white",
                    padding: "20px", 
                    borderRadius: "10px", 
                    boxShadow: "0px 4px 10px rgba(0,0,0,0.3)",
                    textAlign: "center"
                }}>
                    <h2>Your Focus Score</h2>
                    <p style={{ fontSize: "24px", fontWeight: "bold" }}>{score} / 25</p>
                    <button onClick={() => setShowPopup(false)} 
                        style={{
                            padding: "10px 20px", 
                            backgroundColor: "#007BFF", 
                            color: "white", 
                            border: "none", 
                            borderRadius: "5px", 
                            cursor: "pointer"
                        }}>
                        Close
                    </button>
                </div>
            )}
        </div>
    );
}

export default App;
