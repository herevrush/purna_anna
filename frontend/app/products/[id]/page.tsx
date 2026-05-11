'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import { Product } from '@/types';
import { getProduct } from '@/lib/api';
import { useAuth } from '@/lib/auth';
import { useCart } from '@/lib/cartContext';

export default function ProductDetailPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const { accessToken } = useAuth();
  const { addToCart } = useCart();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [adding, setAdding] = useState(false);
  const [added, setAdded] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    getProduct(Number(id))
      .then(setProduct)
      .catch(() => setError('Product not found'))
      .finally(() => setLoading(false));
  }, [id]);

  async function handleAdd() {
    if (!accessToken) { router.push('/login'); return; }
    setAdding(true);
    try {
      await addToCart(product!.id, quantity);
      setAdded(true);
      setTimeout(() => setAdded(false), 3000);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to add to cart');
    } finally {
      setAdding(false);
    }
  }

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="animate-pulse bg-white rounded-2xl h-96" />
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12 text-center">
        <p className="text-red-600 mb-4">{error || 'Product not found'}</p>
        <Link href="/products" className="text-green-700 hover:underline">← Back to products</Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <Link href="/products" className="text-sm text-gray-500 hover:text-green-700 mb-6 inline-flex items-center gap-1 transition-colors">
        ← Back to products
      </Link>

      <div className="mt-4 bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <div className="flex flex-col md:flex-row">
          <div className="relative h-64 md:h-auto md:w-96 bg-gray-50 shrink-0">
            {product.image_url ? (
              <Image
                src={product.image_url}
                alt={product.name}
                fill
                className="object-cover"
                sizes="(max-width: 768px) 100vw, 384px"
              />
            ) : (
              <div className="h-64 md:h-full flex items-center justify-center text-8xl">🛒</div>
            )}
          </div>

          <div className="p-8 flex flex-col">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">{product.name}</h1>
            {product.description && (
              <p className="text-gray-600 mb-6 leading-relaxed">{product.description}</p>
            )}

            <p className="text-4xl font-bold text-green-700 mb-6">${product.price.toFixed(2)}</p>

            {product.stock_quantity === 0 ? (
              <p className="text-red-500 font-medium">Out of Stock</p>
            ) : (
              <>
                <p className="text-sm text-gray-500 mb-4">{product.stock_quantity} in stock</p>
                <div className="flex items-center gap-3 mb-6">
                  <label className="text-sm font-medium text-gray-700">Qty:</label>
                  <div className="flex items-center border border-gray-200 rounded-xl overflow-hidden">
                    <button
                      onClick={() => setQuantity(Math.max(1, quantity - 1))}
                      className="px-3 py-2 hover:bg-gray-100 transition-colors font-bold text-gray-600"
                    >
                      −
                    </button>
                    <span className="px-4 py-2 font-semibold text-gray-800 min-w-[3rem] text-center">{quantity}</span>
                    <button
                      onClick={() => setQuantity(Math.min(product.stock_quantity, quantity + 1))}
                      className="px-3 py-2 hover:bg-gray-100 transition-colors font-bold text-gray-600"
                    >
                      +
                    </button>
                  </div>
                </div>

                {error && (
                  <p className="text-sm text-red-600 mb-3">{error}</p>
                )}

                <button
                  onClick={handleAdd}
                  disabled={adding}
                  className="px-8 py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {added ? '✓ Added to Cart!' : adding ? 'Adding…' : 'Add to Cart'}
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
