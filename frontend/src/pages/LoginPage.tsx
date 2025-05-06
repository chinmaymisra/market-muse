import { useEffect } from "react";
import { LoginButton } from "../components/LoginButton";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const { user, loading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!loading && user) {
      // Delay ensures state has propagated
      setTimeout(() => navigate("/"), 50);
    }
  }, [user, loading, navigate]);

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-900 text-white">
      <div className="text-center">
        <h1 className="text-3xl font-bold mb-6">Login to MarketMuse</h1>
        <LoginButton />
      </div>
    </div>
  );
};

export default LoginPage;
