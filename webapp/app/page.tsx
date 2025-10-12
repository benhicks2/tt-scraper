"use client";
import React, { useState, Suspense } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

function HomeContent() {
  const [selectedEquipment, setSelectedEquipment] = useState<'rubbers' | 'blades'>('rubbers');
  const [searchQuery, setSearchQuery] = useState('');
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/${selectedEquipment}?query=${encodeURIComponent(searchQuery.trim())}`);
    } else {
      router.push(`/${selectedEquipment}`);
    }
  };

  const equipmentTypes = [
    {
      id: 'rubbers' as const,
      name: 'Rubbers',
      icon: (
        <svg className="w-16 h-16" viewBox="0 0 48 48">
          <rect x="0" y="0" width="32" height="32" rx="1" fill="#000000" />
          <rect x="8" y="8" width="32" height="32" rx="1" fill="#ff0000" />
        </svg>
      ),
      color: 'blue'
    },
    {
      id: 'blades' as const,
      name: 'Blades',
      icon: (
        <svg className="w-16 h-16" viewBox="0 0 48 48">
          <rect x="30" y="14" width="8" height="17" rx="1" transform="rotate(35)" fill="#987654 " />
          <ellipse cx="28" cy="19" rx="16" ry="16" fill="#987654 " />
        </svg>
      ),
      color: 'green'
    }
  ];

  return (
    <div className="bg-gray-50">
      {/* Hero Section */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Table Tennis Equipment Tracker
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Find and compare table tennis rubbers and blades from various retailers.
            </p>
          </div>
        </div>
      </div>

      {/* Navigation Cards Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">
          Browse Equipment Categories
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {equipmentTypes.map((type) => (
            <Link
              key={type.id}
              href={`/${type.id}`}
              className="group block bg-white rounded-lg shadow-md hover:shadow-lg transition-all duration-200 border border-gray-200 overflow-hidden transform hover:scale-105"
            >
              <div className="p-8">
                <div className={`inline-flex items-center justify-center w-16 h-16 mb-4`}>
                  <span className={`text-${type.color}-600`}>
                    {type.icon}
                  </span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {type.name}
                </h3>
                <div className={`inline-flex items-center text-${type.color}-600 font-medium group-hover:text-${type.color}-700 transition-colors duration-200`}>
                  Browse {type.name}
                  <svg className="ml-2 w-4 h-4 transform group-hover:translate-x-1 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

export default function Home() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    }>
      <HomeContent />
    </Suspense>
  );
}
