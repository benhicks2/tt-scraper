"use client";
import React from "react";
import Link from "next/link";

interface BreadcrumbItem {
  label: string;
  href?: string;
  current?: boolean;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
  className?: string;
}

export default function Breadcrumb({ items, className = "" }: BreadcrumbProps) {
  return (
    <nav className={`flex items-center space-x-1 text-sm text-gray-500 ${className}`} aria-label="Breadcrumb">
      <ol className="flex items-center space-x-1">
        {items.map((item, index) => (
          <li key={index} className="flex items-center">
            {index > 0 && (
              <svg className="h-4 w-4 text-gray-400 mx-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            )}
            {item.current ? (
              <span className="text-gray-900 font-medium" aria-current="page">
                {item.label}
              </span>
            ) : item.href ? (
              <Link
                href={item.href}
                className="text-gray-500 hover:text-gray-700 transition-colors duration-200"
              >
                {item.label}
              </Link>
            ) : (
              <span className="text-gray-500">{item.label}</span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}

// Predefined breadcrumb configurations
export const breadcrumbConfigs = {
  home: [{ label: "Home", href: "/", current: true }],
  rubbers: [
    { label: "Home", href: "/" },
    { label: "Rubbers", current: true }
  ],
  rubberDetails: (rubberName: string, rubberId: string) => [
    { label: "Home", href: "/" },
    { label: "Rubbers", href: "/rubbers" },
    { label: rubberName, current: true }
  ]
};
