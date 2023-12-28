import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

function Home() {
  const [auth_url, setAuth_url] = useState("");
  const [authCode, setAuthCode] = useState("");
  const navigate = useNavigate();
  const location = useLocation();

  const exchangeCodeForTokens = async (code) => {
    console.log("Code:", code);
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/exchange_code_for_tokens",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ auth_code: code }),
        }
      );

      const data = await response.json();
      localStorage.setItem("jwt_token", data.jwt_token);
      console.log("Response:", data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  let count = 0;
  useEffect(() => {
    const exchangeCode = async () => {
      console.log(count++);
      const currentUrl = location.pathname + location.search;
      const urlParams = new URLSearchParams(currentUrl.split("?")[1]);
      const code = urlParams.get("code");
      if (code) {
        setAuthCode(code);
        await exchangeCodeForTokens(code);
        navigate("/dashboard");
      }
    };

    exchangeCode();
  }, [navigate, location.pathname, location.search]);

  const handleAuthorization = () => {
    fetch("http://127.0.0.1:8000/auth/url")
      .then((response) => response.json())
      .then((data) => {
        setAuth_url(data.auth_url);
        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const redirectToAuth = () => {
    if (auth_url) {
      window.location.href = auth_url;
    } else {
      console.error("Authorization URL not available yet.");
    }
  };

  return (
    <>
      <h1>SemTrack</h1>
      <div>
        <h2>Authorize Access to Google Calendar</h2>
        <button onClick={handleAuthorization}>Authorize</button>
        {auth_url && (
          <button onClick={redirectToAuth}>Proceed to Authorization</button>
        )}
      </div>
    </>
  );
}

export default Home;
