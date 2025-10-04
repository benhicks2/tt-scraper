"use client";
import React from "react";
import Header from "./header";
import SideNav from "./sidenav";

interface LayoutWrapperProps {
  children: React.ReactNode;
}

export default function LayoutWrapper({ children }: LayoutWrapperProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header - Full width at top */}
      <Header />

      {/* Content area with sidebar */}
      <div className="flex">
        {/* Sidebar - Always visible */}
        <SideNav />

        {/* Main content area */}
        <main className="flex-1">
          {children}
        </main>
      </div>
    </div>
  );
}
