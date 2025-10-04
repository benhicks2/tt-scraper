"use client";
import React from 'react';
import { useSearchParams, usePathname, useRouter } from 'next/navigation';

type SearchBarProps = {
  placeholder: string,
  className: string
};

export default function SearchBar({
  placeholder = "Search...",
  className = "",
}: SearchBarProps) {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const { replace } = useRouter();

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const input = formData.get('query')?.toString().trim();
    const params = new URLSearchParams(searchParams);
    if (input) {
      params.set('query', input);
    }
    else {
      params.delete('query');
    }
    params.set('page', '1');
    replace(`${pathname}?${params.toString()}`);
  }

  return (
    <form className={`relative flex items-center ${className}`} onSubmit={handleSubmit}>
      <div className="relative flex-1">
      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
      <input
        name="query"
        type="text"
        placeholder={placeholder}
        defaultValue={searchParams.get('query')?.toString()}
        className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-700 text-gray-900 focus:outline-none focus:placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 ease-in-out"
        aria-label="Search"
      />
      </div>
      <button
      type="submit"
      className="ml-3 inline-flex items-center px-5 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200 ease-in-out transform hover:scale-105 active:scale-95 shadow-sm hover:shadow-md"
      >
        Search
      </button>
    </form>
  );
}
