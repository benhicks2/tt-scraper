"use client";
import React from "react";
import Header from "./header";
import SideNav from "./sidenav";
import Footer from "./footer";

interface LayoutWrapperProps {
  children: React.ReactNode;
}

export default function LayoutWrapper({ children }: LayoutWrapperProps) {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header - Full width at top */}
      <Header />

      {/* Content area with sidebar */}
      <div className="flex flex-1">
        {/* Sidebar - Always visible */}
        <SideNav />

        {/* Main content area */}
        <main className="flex-1 flex flex-col">
          {children}
        </main>
      </div>

      {/* Footer - Sticky to bottom */}
      <Footer />
    </div>
  );
}
