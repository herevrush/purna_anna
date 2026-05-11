'use client';

import { useEffect, useState } from 'react';
import { Product, Category } from '@/types';
import { getProducts, getCategories } from '@/lib/api';
import ProductCard from '@/components/ProductCard';
import CategorySidebar from '@/components/CategorySidebar';

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<number | undefined>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    getCategories()
      .then(setCategories)
      .catch(() => {});
  }, []);

  useEffect(() => {
    setLoading(true);
    setError('');
    getProducts({ category_id: selectedCategory, limit: 50 })
      .then(setProducts)
      .catch(() => setError('Failed to load products'))
      .finally(() => setLoading(false));
  }, [selectedCategory]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex gap-8">
        <CategorySidebar
          categories={categories}
          selectedId={selectedCategory}
          onSelect={setSelectedCategory}
        />

        <div className="flex-1">
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold text-gray-800">
              {selectedCategory
                ? categories.find((c) => c.id === selectedCategory)?.name ?? 'Products'
                : 'All Products'}
            </h1>
            {!loading && (
              <span className="text-sm text-gray-500">{products.length} items</span>
            )}
          </div>

          {loading && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
              {Array.from({ length: 8 }).map((_, i) => (
                <div key={i} className="bg-white rounded-2xl shadow-sm border border-gray-100 h-72 animate-pulse" />
              ))}
            </div>
          )}

          {error && (
            <div className="p-6 text-center text-red-600 bg-red-50 rounded-2xl">{error}</div>
          )}

          {!loading && !error && products.length === 0 && (
            <div className="p-12 text-center text-gray-400">
              <p className="text-4xl mb-3">🧺</p>
              <p className="text-lg font-medium">No products found</p>
            </div>
          )}

          {!loading && !error && products.length > 0 && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
              {products.map((p) => (
                <ProductCard key={p.id} product={p} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
