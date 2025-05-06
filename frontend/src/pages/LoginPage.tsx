import { LoginButton } from "../components/LoginButton";

const LoginPage = () => {
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
