import PlanCard from "../components/PlanCard";
import axios from "axios";

export default function Home() {
  const handleBuy = async (plan) => {
    const res = await axios.post("https://yourdomain.com/payment/create-checkout-session", { plan });
    window.location.href = res.data.checkout_url;
  };

  return (
    <div className="p-10">
      <h1 className="text-4xl font-bold mb-6">TPchet API Service</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <PlanCard title="Starter" price="$10/month" onBuy={() => handleBuy("starter")} />
        <PlanCard title="Pro" price="$30/month" onBuy={() => handleBuy("pro")} />
        <PlanCard title="Enterprise" price="$100/month" onBuy={() => handleBuy("enterprise")} />
      </div>
    </div>
  );
    }
