import React, { useEffect } from "react";
import { LoginButton } from "../components/LoginButton";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  // If already logged in, redirect away from login page
  useEffect(() => {
    if (user) {
      navigate("/");
    }
  }, [user, navigate]);

  return (
    <div className="flex justify-center items-center w-screen h-screen bg-gray-900 text-white">
      <div className="text-center">
        <h1 className="text-3xl font-bold mb-6">Login to MarketMuse</h1>
        <LoginButton />
      </div>
    </div>
  );
};

export default LoginPage;
