import { LoginButton } from "../components/LoginButton"; // ✅ make sure path is correct

const LoginPage = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white">
      <h1 className="text-3xl font-bold mb-6">Login to MarketMuse</h1>
      <LoginButton />
    </div>
  );
};

export default LoginPage;
