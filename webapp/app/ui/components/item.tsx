"use client";
import React from "react";
import Image from "next/image";
import Link from "next/link";
import { StringUtils } from "@/app/_lib/stringutils";
import Breadcrumb, { breadcrumbConfigs } from "@/app/ui/components/breadcrumb";

export type EquipmentItem = {
  _id: string;
  name: string;
  all_time_low_price: string;
  entries: Array<{
    url: string;
    price: string;
    last_updated: string;
  }>;
};

export function Item({image, title, price, slug}: {image: string, title: string, price: string, slug: string}) {
  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      window.location.href = slug;
    }
  };

  return (
    <Link
      href={slug}
      className="block bg-white rounded-lg shadow-md hover:bg-gray-50 hover:shadow-lg transition-all duration-200 border border-gray-200 overflow-hidden focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
      tabIndex={0}
      aria-label={`View details for ${title}`}
      onKeyDown={handleKeyDown}
    >
      {/* Card Image Placeholder - TODO: Add image */}
      {/* <div className="h-48 bg-gradient-to-br from-blue-50 to-blue-100 flex items-center justify-center">
        <div className="w-16 h-16 bg-blue-200 rounded-full flex items-center justify-center">
          <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>
      </div> */}

      {/* Card Content */}
      <div className="p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-2 line-clamp-2">
          {title}
        </h3>
        <p className="text-2xl font-bold text-blue-600 mb-4">
          {price}
        </p>
        <div className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600">
          View Details
          <svg className="ml-2 -mr-1 w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </div>
      </div>
    </Link>
  );
}

export function ItemList({ items, loading, numLoadingItems, equipmentType }: { items: EquipmentItem[], loading: boolean, numLoadingItems?: number, equipmentType: 'rubbers' | 'blades' }) {
  const getEmptyStateMessage = (type: 'rubbers' | 'blades') => {
    return type === 'rubbers' ? 'No rubbers found' : 'No blades found';
  };

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {items.map((item) => (
        <Item
          key={item._id}
          image={"/test.jpg"}
          title={StringUtils.truncate(item.name, 50)}
          price={item.entries[0].price}
          slug={`/${equipmentType}/${item._id}`}
        />
      ))}
      {!loading && items.length === 0 ? (
        <div className="col-span-full flex flex-col items-center justify-center py-12">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">{getEmptyStateMessage(equipmentType)}</h3>
          <p className="text-gray-500">Try adjusting your search criteria</p>
        </div>
      ) : (
        loading ? (
          ItemListLoading({ numItems: numLoadingItems || 10 })
        ) : ""
      )}
    </div>
  );
}

export function ItemDescription({ item }: { item: EquipmentItem }) {
  // Extract domain name from URL
  const getDomainName = (url: string) => {
    try {
      const domain = new URL(url).hostname;
      return domain.replace('www.', '');
    } catch {
      return url;
    }
  };

  // Format date
  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    } catch {
      return dateString;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header Section */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          {/* Breadcrumb Navigation */}
          <div className="mb-4">
            <Breadcrumb items={breadcrumbConfigs.rubberDetails(item.name, item._id)} />
          </div>

          <h1 className="text-3xl font-medium text-gray-900 mb-2">{item.name}</h1>
          <div className="flex items-center space-x-4">
            <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
              Best Price: {item.all_time_low_price}
            </div>
            <div className="text-gray-500 text-sm">
              {item.entries.length} store{item.entries.length !== 1 ? 's' : ''} available
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Price Comparison Section */}
        <div className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden mb-8">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Available at {item.entries.length} stores</h2>
            <p className="text-gray-600 mt-1">Compare prices and find the best deal</p>
          </div>

          <div className="divide-y divide-gray-200">
            {item.entries.map((entry, index) => (
              <div key={entry.url} className="p-6 hover:bg-gray-50 transition-colors duration-200">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3">
                      <div className="flex-shrink-0">
                        <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                          <span className="text-blue-600 font-semibold text-sm">
                            {index + 1}
                          </span>
                        </div>
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="text-lg font-medium text-gray-900 truncate">
                          {getDomainName(entry.url)}
                        </h3>
                        <p className="text-sm text-gray-500">
                          Last updated: {formatDate(entry.last_updated)}
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center space-x-4">
                    <div className="text-right">
                      <div className="text-2xl font-bold text-gray-900">
                        {entry.price}
                      </div>
                      {index === 0 && (
                        <div className="text-xs text-green-600 font-medium">
                          Best Price
                        </div>
                      )}
                    </div>

                    <a
                      href={entry.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200 ease-in-out transform hover:scale-105 active:scale-95 shadow-sm hover:shadow-md"
                    >
                      Visit Store
                      <svg className="ml-2 -mr-1 w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                      </svg>
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Price History Section - TODO*/}
        {/* <div className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Price History</h2>
            <p className="text-gray-600 mt-1">Track price changes over time</p>
          </div>

          <div className="p-6">
            <div className="space-y-4">
              {item.entries.map((entry, index) => (
                <div key={`${entry.url}-${index}`} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                      <span className="text-gray-600 text-sm font-medium">
                        {index + 1}
                      </span>
                    </div>
                    <div>
                      <p className="font-medium text-gray-900">{getDomainName(entry.url)}</p>
                      <p className="text-sm text-gray-500">{formatDate(entry.last_updated)}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-lg font-semibold text-gray-900">{entry.price}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div> */}
      </div>
    </div>
  );
}

function LoadingItem() {
  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden animate-pulse">
      {/* Image placeholder */}
      {/* <div className="h-48 bg-gray-200"></div> */}

      {/* Content placeholder */}
      <div className="p-6">
        <div className="h-6 bg-gray-200 rounded mb-2"></div>
        <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
        <div className="h-10 bg-gray-200 rounded w-1/2"></div>
      </div>
    </div>
  );
}

export function ItemListLoading({ numItems = 10 }: { numItems?: number }) {
  return (
    Array.from({ length: numItems }).map((_, index) => (
      <LoadingItem key={index} />
    ))
  );
}
