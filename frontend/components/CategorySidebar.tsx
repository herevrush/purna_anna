'use client';

import { Category } from '@/types';

interface Props {
  categories: Category[];
  selectedId?: number;
  onSelect: (id?: number) => void;
}

export default function CategorySidebar({ categories, selectedId, onSelect }: Props) {
  return (
    <aside className="w-56 shrink-0">
      <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Categories</h2>
      <ul className="space-y-1">
        <li>
          <button
            onClick={() => onSelect(undefined)}
            className={`w-full text-left px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              selectedId === undefined
                ? 'bg-green-100 text-green-800'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            All Products
          </button>
        </li>
        {categories.map((cat) => (
          <li key={cat.id}>
            <button
              onClick={() => onSelect(cat.id)}
              className={`w-full text-left px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedId === cat.id
                  ? 'bg-green-100 text-green-800'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              {cat.name}
            </button>
          </li>
        ))}
      </ul>
    </aside>
  );
}
