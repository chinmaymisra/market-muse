import { useEffect } from "react";
import { LoginButton } from "../components/LoginButton";
import { useAuth } from "../context/AuthContext";
import { useNavigate, Navigate } from "react-router-dom";

const LoginPage = () => {
  const { user, loading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!loading && user) {
      navigate("/");
    }
  }, [user, loading, navigate]);

  if (!loading && user) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="flex items-center justify-center w-screen h-screen bg-gray-900 text-white px-4">
      <div className="flex flex-col items-center gap-6 text-center max-w-md">
        <h1 className="text-3xl font-bold">Login to MarketMuse</h1>
        <p className="text-gray-400">Your AI-powered trading assistant</p>
        <LoginButton />
      </div>
    </div>
  );
};

export default LoginPage;
