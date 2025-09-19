import { useEffect, useState } from "react";
import axios from "axios";

export default function Dashboard() {
  const [apiKeys, setApiKeys] = useState([]);
  const [usage, setUsage] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const resKeys = await axios.get("https://yourdomain.com/api/user/apikeys");
      setApiKeys(resKeys.data);

      const resUsage = await axios.get("https://yourdomain.com/api/user/usage");
      setUsage(resUsage.data);
    };
    fetchData();
  }, []);

  return (
    <div className="p-10">
      <h1 className="text-3xl font-bold mb-4">Your API Keys</h1>
      <ul>{apiKeys.map((key) => <li key={key.id}>{key.key}</li>)}</ul>
      <h2 className="text-2xl font-bold mt-8 mb-4">Usage History</h2>
      <ul>{usage.map((u) => <li key={u.id}>{u.date} - {u.calls} calls</li>)}</ul>
    </div>
  );
}
