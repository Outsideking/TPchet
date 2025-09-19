import axios from "axios";

export default function Home() {
  const handleBuy = async () => {
    const res = await axios.post("http://localhost:8000/payment/create-checkout-session");
    window.location.href = res.data.checkout_url;
  };

  return (
    <div className="p-10">
      <h1 className="text-3xl font-bold">TPchet API Service</h1>
      <button onClick={handleBuy} className="mt-4 px-4 py-2 bg-blue-600 text-white rounded">
        Buy Pro Plan
      </button>
    </div>
  )
    }
