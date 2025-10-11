"use client";
import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function SideNav() {
  const pathname = usePathname();

  const navigationItems = [
    {
      name: 'Home',
      href: '/',
    },
    {
      name: 'Rubbers',
      href: '/rubbers',
    },
    {
      name: 'Blades',
      href: '/blades',
    }
  ];

  return (
    <nav className="sidebar w-64 bg-white shadow-sm border-r border-gray-200 flex-shrink-0">
      <div className="flex flex-col h-full">

          {/* Navigation Items */}
          <div className="flex-1 px-4 py-6">
            <ul className="space-y-2">
              {navigationItems.map((item) => {
                const isActive = pathname === item.href;
                return (
                  <li key={item.name}>
                    <Link
                      href={item.href}
                      className={`flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                        isActive
                          ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700'
                          : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                      }`}
                    >
                      <span>{item.name}</span>
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        </div>
      </nav>
  );
}
