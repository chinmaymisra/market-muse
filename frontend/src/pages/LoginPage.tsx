import { useEffect } from "react";
import { LoginButton } from "../components/LoginButton";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import logo from "../assets/marketmuse_highres.png"; // App logo

const LoginPage = () => {
  const { user, loading } = useAuth();         // Auth context
  const navigate = useNavigate();              // Router navigation

  // Redirect to main app if already logged in
  useEffect(() => {
    if (!loading && user) {
      navigate("/");
    }
  }, [user, loading, navigate]);

  // Render the login screen
  return (
    <div className="flex items-center justify-center w-screen h-screen bg-gray-900 text-white px-4">
      <div className="flex flex-col items-center gap-6 text-center max-w-md">
        <img
          src={logo}
          alt="MarketMuse Logo"
          className="w-24 h-24 mb-4 rounded-full shadow-lg"
        />
        <h1 className="text-3xl font-bold">Login to MarketMuse</h1>
        <p className="text-gray-400">Your personal trading assistant</p>
        <LoginButton />
      </div>
    </div>
  );
};

export default LoginPage;
