'use client';

import Image from 'next/image';
import { CartItem as CartItemType } from '@/types';
import { useCart } from '@/lib/cartContext';

interface Props {
  item: CartItemType;
}

export default function CartItemRow({ item }: Props) {
  const { updateItem, removeItem } = useCart();

  return (
    <div className="flex items-center gap-4 py-4 border-b border-gray-100 last:border-0">
      <div className="relative h-20 w-20 rounded-xl overflow-hidden bg-gray-50 shrink-0">
        {item.product.image_url ? (
          <Image
            src={item.product.image_url}
            alt={item.product.name}
            fill
            className="object-cover"
            sizes="80px"
          />
        ) : (
          <div className="h-full flex items-center justify-center text-3xl">🛒</div>
        )}
      </div>

      <div className="flex-1 min-w-0">
        <p className="font-semibold text-gray-800 truncate">{item.product.name}</p>
        <p className="text-sm text-green-700 font-medium">${item.product.price} each</p>
      </div>

      <div className="flex items-center gap-2">
        <button
          onClick={() => updateItem(item.id, item.quantity - 1)}
          className="h-8 w-8 rounded-full border border-gray-200 flex items-center justify-center hover:bg-gray-100 transition-colors font-bold text-gray-600"
        >
          −
        </button>
        <span className="w-8 text-center font-semibold text-gray-800">{item.quantity}</span>
        <button
          onClick={() => updateItem(item.id, item.quantity + 1)}
          className="h-8 w-8 rounded-full border border-gray-200 flex items-center justify-center hover:bg-gray-100 transition-colors font-bold text-gray-600"
        >
          +
        </button>
      </div>

      <div className="text-right shrink-0">
        <p className="font-bold text-gray-800">${(item.product.price * item.quantity).toFixed(2)}</p>
        <button
          onClick={() => removeItem(item.id)}
          className="text-xs text-red-400 hover:text-red-600 transition-colors mt-1"
        >
          Remove
        </button>
      </div>
    </div>
  );
}
