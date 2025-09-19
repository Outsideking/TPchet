import { useEffect, useState } from "react";
import axios from "axios";

export default function AdminDashboard() {
  const [payments, setPayments] = useState([]);
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const resPayments = await axios.get("https://yourdomain.com/api/admin/payments");
      setPayments(resPayments.data);

      const resUsers = await axios.get("https://yourdomain.com/api/admin/users");
      setUsers(resUsers.data);
    };
    fetchData();
  }, []);

  return (
    <div className="p-10">
      <h1 className="text-4xl font-bold mb-6">Admin Dashboard</h1>
      <h2 className="text-2xl font-bold mb-2">Payments</h2>
      <table className="min-w-full mb-8">
        <thead>
          <tr><th>User</th><th>Amount</th><th>Status</th><th>Date</th></tr>
        </thead>
        <tbody>{payments.map(p => (
          <tr key={p.id}><td>{p.user_email}</td><td>{p.amount} {p.currency}</td><td>{p.status}</td><td>{p.date}</td></tr>
        ))}</tbody>
      </table>
      <h2 className="text-2xl font-bold mb-2">Users & API Keys</h2>
      <ul>{users.map(u => <li key={u.id}>{u.email} - Keys: {u.api_keys.join(", ")}</li>)}</ul>
    </div>
  );
    }
