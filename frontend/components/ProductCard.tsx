'use client';

import Link from 'next/link';
import Image from 'next/image';
import { Product } from '@/types';
import { useAuth } from '@/lib/auth';
import { useCart } from '@/lib/cartContext';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

interface Props {
  product: Product;
}

export default function ProductCard({ product }: Props) {
  const { accessToken } = useAuth();
  const { addToCart } = useCart();
  const router = useRouter();
  const [adding, setAdding] = useState(false);
  const [added, setAdded] = useState(false);

  async function handleAdd() {
    if (!accessToken) { router.push('/login'); return; }
    setAdding(true);
    try {
      await addToCart(product.id);
      setAdded(true);
      setTimeout(() => setAdded(false), 2000);
    } catch {
      // silently fail
    } finally {
      setAdding(false);
    }
  }

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow flex flex-col">
      <Link href={`/products/${product.id}`} className="block">
        <div className="relative h-48 bg-gray-50">
          {product.image_url ? (
            <Image
              src={product.image_url}
              alt={product.name}
              fill
              className="object-cover"
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            />
          ) : (
            <div className="h-full flex items-center justify-center text-5xl">🛒</div>
          )}
        </div>
        <div className="p-4 flex-1">
          <h3 className="font-semibold text-gray-800 line-clamp-2 mb-1">{product.name}</h3>
          {product.description && (
            <p className="text-sm text-gray-500 line-clamp-2 mb-2">{product.description}</p>
          )}
          <p className="text-lg font-bold text-green-700">${product.price}</p>
        </div>
      </Link>
      <div className="px-4 pb-4">
        <button
          onClick={handleAdd}
          disabled={adding || product.stock_quantity === 0}
          className="w-full py-2 rounded-xl text-sm font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed bg-green-600 hover:bg-green-700 text-white"
        >
          {product.stock_quantity === 0 ? 'Out of Stock' : added ? '✓ Added!' : adding ? 'Adding…' : 'Add to Cart'}
        </button>
      </div>
    </div>
  );
}
