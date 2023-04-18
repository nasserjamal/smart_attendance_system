import React from "react";
import axios from "axios";

const Settings = () => {
  const sendRequest = async () => {
    console.log("Now sending the request")
    try {
      const response = await axios.get("http://192.168.20.42:5000/react/reset", {
        params: {
          data: "yUTF56",
        },
      });

      if (response.data.success) {
        console.log("Success")
        window.location.reload();
      } else {
        console.log("Request was not successful. Response:", response.data);
      }
    } catch (error) {
      console.error("Error sending GET request:", error);
    }
  };

  const handleSystemReset = () => {
    const confirmReset = window.confirm(
      "Are you sure you want to reset the system?"
    );

    if (confirmReset) {
      sendRequest();
    }
  };

  return (
    <>
      <button onClick={handleSystemReset}>System reset</button>
    </>
  );
};

export default Settings;
