'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/lib/auth';
import { getOrder } from '@/lib/api';
import { Order } from '@/types';

export default function OrderDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { user, isLoading: authLoading, accessToken } = useAuth();
  const router = useRouter();
  const [order, setOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!authLoading && !user) router.push('/login');
  }, [authLoading, user, router]);

  useEffect(() => {
    if (!accessToken) return;
    getOrder(accessToken, Number(id))
      .then(setOrder)
      .catch(() => setError('Order not found'))
      .finally(() => setLoading(false));
  }, [accessToken, id]);

  if (authLoading || (!user && !authLoading)) return null;

  if (loading) {
    return <div className="max-w-3xl mx-auto px-4 py-12"><div className="animate-pulse bg-white rounded-2xl h-64" /></div>;
  }

  if (error || !order) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-12 text-center">
        <p className="text-red-600 mb-4">{error || 'Order not found'}</p>
        <Link href="/orders" className="text-green-700 hover:underline">← Back to orders</Link>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      <Link href="/orders" className="text-sm text-gray-500 hover:text-green-700 mb-6 inline-flex items-center gap-1 transition-colors">
        ← Back to orders
      </Link>

      <div className="mt-4 bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
        <div className="flex justify-between items-start mb-8">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Order #{order.id}</h1>
            <p className="text-sm text-gray-500 mt-1">
              Placed on {new Date(order.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
            </p>
          </div>
          <span className={`px-3 py-1 rounded-full text-sm font-medium capitalize ${
            order.status === 'completed' ? 'bg-green-100 text-green-700' :
            order.status === 'pending' ? 'bg-yellow-100 text-yellow-700' :
            'bg-gray-100 text-gray-600'
          }`}>
            {order.status}
          </span>
        </div>

        <h2 className="text-lg font-semibold text-gray-700 mb-4">Items</h2>
        <div className="space-y-3 mb-8">
          {order.items.map((item) => (
            <div key={item.id} className="flex justify-between items-center py-3 border-b border-gray-100 last:border-0">
              <div>
                <p className="font-medium text-gray-800">Product #{item.product_id}</p>
                <p className="text-sm text-gray-500">Qty: {item.quantity} × ${item.unit_price.toFixed(2)}</p>
              </div>
              <p className="font-semibold text-gray-800">${(item.quantity * item.unit_price).toFixed(2)}</p>
            </div>
          ))}
        </div>

        <div className="flex justify-between items-center pt-4 border-t border-gray-200">
          <span className="text-lg font-semibold text-gray-700">Total</span>
          <span className="text-2xl font-bold text-green-700">${order.total.toFixed(2)}</span>
        </div>
      </div>
    </div>
  );
}
