import React, { useEffect, useState } from "react";
import axios from "../api/axios";

const TeamViewer = () => {
  const [team, setTeam] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTeam = async () => {
      try {
        const response = await axios.get("/team/current");
        setTeam(response.data);
      } catch (err) {
        console.error("Failed to fetch team:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchTeam();
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h2>Current Team</h2>
      <ul>
        {team.map((player, idx) => (
          <li key={idx}>
            Player ID: {player.player_id}, Captain:{" "}
            {player.is_captain ? "Yes" : "No"}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TeamViewer;
