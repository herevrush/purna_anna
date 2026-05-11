import { Product, Category, CartItem, Order } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function apiFetch<T>(
  path: string,
  options: RequestInit = {},
  token?: string | null
): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}${path}`, { ...options, headers });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `API error ${res.status}`);
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

// Products
export const getProducts = (params?: { category_id?: number; skip?: number; limit?: number }) => {
  const qs = new URLSearchParams();
  if (params?.category_id) qs.set('category_id', String(params.category_id));
  if (params?.skip) qs.set('skip', String(params.skip));
  if (params?.limit) qs.set('limit', String(params.limit));
  const query = qs.toString() ? `?${qs}` : '';
  return apiFetch<Product[]>(`/api/v1/products/${query}`);
};

export const getProduct = (id: number) => apiFetch<Product>(`/api/v1/products/${id}`);

// Categories
export const getCategories = () => apiFetch<Category[]>('/api/v1/categories/');

// Cart
export const getCart = (token: string) => apiFetch<CartItem[]>('/api/v1/cart/', {}, token);

export const addToCart = (token: string, product_id: number, quantity: number) =>
  apiFetch<CartItem>('/api/v1/cart/items', { method: 'POST', body: JSON.stringify({ product_id, quantity }) }, token);

export const updateCartItem = (token: string, id: number, quantity: number) =>
  apiFetch<CartItem>(`/api/v1/cart/items/${id}`, { method: 'PUT', body: JSON.stringify({ quantity }) }, token);

export const deleteCartItem = (token: string, id: number) =>
  apiFetch<void>(`/api/v1/cart/items/${id}`, { method: 'DELETE' }, token);

// Orders
export const createOrder = (token: string) =>
  apiFetch<Order>('/api/v1/orders/', { method: 'POST' }, token);

export const getOrders = (token: string) => apiFetch<Order[]>('/api/v1/orders/', {}, token);

export const getOrder = (token: string, id: number) => apiFetch<Order>(`/api/v1/orders/${id}`, {}, token);
