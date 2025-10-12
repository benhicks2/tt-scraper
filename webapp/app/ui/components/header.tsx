"use client";
import React from "react";
import Link from "next/link";

export default function Header() {

  return (
    <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-40">
      <div className="flex items-center justify-between px-4 sm:px-6 lg:px-8 h-16">
        {/* Left side - Logo/Brand */}
        <div className="flex items-center">
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-xl font-semibold text-gray-900">TT Scraper</span>
          </Link>
        </div>
      </div>
    </header>
  );
}
