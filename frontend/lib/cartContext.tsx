'use client';

import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { CartItem } from '@/types';
import { getCart, addToCart as apiAddToCart, updateCartItem as apiUpdateCartItem, deleteCartItem as apiDeleteCartItem } from '@/lib/api';
import { useAuth } from '@/lib/auth';

interface CartContextType {
  items: CartItem[];
  itemCount: number;
  isLoading: boolean;
  addToCart: (product_id: number, quantity?: number) => Promise<void>;
  updateItem: (id: number, quantity: number) => Promise<void>;
  removeItem: (id: number) => Promise<void>;
  refresh: () => Promise<void>;
}

const CartContext = createContext<CartContextType | null>(null);

export function CartProvider({ children }: { children: React.ReactNode }) {
  const { accessToken } = useAuth();
  const [items, setItems] = useState<CartItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const refresh = useCallback(async () => {
    if (!accessToken) { setItems([]); return; }
    setIsLoading(true);
    try {
      const data = await getCart(accessToken);
      setItems(data);
    } catch {
      setItems([]);
    } finally {
      setIsLoading(false);
    }
  }, [accessToken]);

  useEffect(() => { refresh(); }, [refresh]);

  async function addToCart(product_id: number, quantity = 1) {
    if (!accessToken) throw new Error('Not authenticated');
    await apiAddToCart(accessToken, product_id, quantity);
    await refresh();
  }

  async function updateItem(id: number, quantity: number) {
    if (!accessToken) return;
    if (quantity <= 0) {
      await apiDeleteCartItem(accessToken, id);
    } else {
      await apiUpdateCartItem(accessToken, id, quantity);
    }
    await refresh();
  }

  async function removeItem(id: number) {
    if (!accessToken) return;
    await apiDeleteCartItem(accessToken, id);
    await refresh();
  }

  const itemCount = items.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <CartContext.Provider value={{ items, itemCount, isLoading, addToCart, updateItem, removeItem, refresh }}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error('useCart must be used within CartProvider');
  return ctx;
}
