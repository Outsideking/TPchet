import { useEffect, useState } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart, Bar } from "recharts";

export default function Admin() {
  const [translations, setTranslations] = useState([]);
  const [payments, setPayments] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/admin/translations").then(res => setTranslations(res.data));
    axios.get("http://localhost:8000/admin/payments").then(res => setPayments(res.data));
  }, []);

  return (
    <div className="p-10">
      <h1 className="text-3xl font-bold">Admin Dashboard</h1>

      <h2 className="mt-6 text-xl">Translations Over Time</h2>
      <LineChart width={800} height={300} data={translations}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="count" stroke="#8884d8" />
      </LineChart>

      <h2 className="mt-6 text-xl">Payments</h2>
      <BarChart width={800} height={300} data={payments}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="amount" fill="#82ca9d" />
      </BarChart>
    </div>
  )
            }
