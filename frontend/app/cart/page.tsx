'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/lib/auth';
import { useCart } from '@/lib/cartContext';
import CartItemRow from '@/components/CartItem';
import { createOrder } from '@/lib/api';

export default function CartPage() {
  const { user, isLoading: authLoading, accessToken } = useAuth();
  const { items, isLoading, refresh } = useCart();
  const router = useRouter();
  const [checkingOut, setCheckingOut] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
    }
  }, [authLoading, user, router]);

  if (authLoading || (!user && !authLoading)) return null;

  const total = items.reduce((sum, item) => sum + item.product.price * item.quantity, 0);

  async function handleCheckout() {
    if (!accessToken) return;
    setError('');
    setCheckingOut(true);
    try {
      const order = await createOrder(accessToken);
      await refresh();
      router.push(`/orders/${order.id}`);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Checkout failed');
    } finally {
      setCheckingOut(false);
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Your Cart</h1>

      {isLoading && (
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-24 bg-white rounded-2xl animate-pulse" />
          ))}
        </div>
      )}

      {!isLoading && items.length === 0 && (
        <div className="text-center py-20">
          <p className="text-5xl mb-4">🧺</p>
          <p className="text-xl font-semibold text-gray-600 mb-2">Your cart is empty</p>
          <p className="text-gray-400 mb-8">Add some fresh groceries to get started</p>
          <Link
            href="/products"
            className="inline-block bg-green-600 hover:bg-green-700 text-white font-semibold px-8 py-3 rounded-xl transition-colors"
          >
            Shop Now
          </Link>
        </div>
      )}

      {!isLoading && items.length > 0 && (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <div className="divide-y divide-gray-100">
            {items.map((item) => (
              <CartItemRow key={item.id} item={item} />
            ))}
          </div>

          <div className="mt-6 pt-6 border-t border-gray-100">
            <div className="flex justify-between items-center mb-6">
              <span className="text-lg font-semibold text-gray-700">Total</span>
              <span className="text-2xl font-bold text-green-700">${total.toFixed(2)}</span>
            </div>

            {error && (
              <p className="text-sm text-red-600 mb-4">{error}</p>
            )}

            <button
              onClick={handleCheckout}
              disabled={checkingOut}
              className="w-full py-3 bg-green-600 hover:bg-green-700 text-white font-bold rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-lg"
            >
              {checkingOut ? 'Placing Order…' : 'Checkout'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
