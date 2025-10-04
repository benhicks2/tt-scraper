"use client";
import React, { useEffect } from "react";
import { useRouter } from "next/navigation";

interface DetailPageWrapperProps {
  children: React.ReactNode;
}

export function DetailPageWrapper({ children }: DetailPageWrapperProps) {
  const router = useRouter();

  useEffect(() => {
    // Set navigation type when component mounts (user is on detail page)
    sessionStorage.setItem('navigation-type', 'detail-to-list');

    // Handle browser back button
    const handlePopState = () => {
      sessionStorage.setItem('navigation-type', 'detail-to-list');
    };

    window.addEventListener('popstate', handlePopState);

    return () => {
      window.removeEventListener('popstate', handlePopState);
    };
  }, []);

  return (
    <div>
      {/* Back button */}
      <div className="mb-6">
        <button
          onClick={() => {
            sessionStorage.setItem('navigation-type', 'detail-to-list');
            router.back();
          }}
          className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200"
        >
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Rubbers
        </button>
      </div>
      {children}
    </div>
  );
}
