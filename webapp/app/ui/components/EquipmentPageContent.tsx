"use client";
import React from "react";
import { ItemList } from "@/app/ui/components/item";
import SearchBar from "@/app/ui/components/searchbar";
import Breadcrumb from "@/app/ui/components/breadcrumb";
import { useEquipmentPage } from "@/app/ui/hooks/useEquipmentPage";

interface EquipmentPageContentProps {
  equipmentType: 'rubbers' | 'blades';
  title: string;
  searchPlaceholder: string;
  breadcrumbItems: Array<{ label: string; href?: string; current?: boolean }>;
}

export function EquipmentPageContent({
  equipmentType,
  title,
  searchPlaceholder,
  breadcrumbItems
}: EquipmentPageContentProps) {
  const { items, page, hasMore, loading, loadMore } = useEquipmentPage({ equipmentType });

  return (
    <div className="bg-gray-50">
      {/* Material Design Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          {/* Breadcrumb Navigation */}
          <div className="mb-4">
            <Breadcrumb items={breadcrumbItems} />
          </div>

          <h1 className="text-3xl font-medium text-gray-900 mb-6">
            {title}
          </h1>
          <SearchBar
            placeholder={searchPlaceholder}
            className="max-w-md"
          />
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <ItemList items={items} loading={loading} numLoadingItems={page * 10} equipmentType={equipmentType} />

        {/* Load More Button with Material Design */}
        {hasMore && (
          <div className="flex justify-center mt-8">
            <button
              disabled={loading}
              onClick={loadMore}
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 ease-in-out transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-xl"
            >Load More
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
