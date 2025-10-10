"use client";
import React, { useEffect } from "react";
import { useRouter } from "next/navigation";

interface DetailPageWrapperProps {
  children: React.ReactNode;
}

export function DetailPageWrapper({ children }: DetailPageWrapperProps) {
  const router = useRouter();

  // useEffect(() => {
  //   // Set navigation type when component mounts (user is on detail page)
  //   sessionStorage.setItem('navigation-type', 'detail-to-list');

  //   // Handle browser back button
  //   const handlePopState = () => {
  //     sessionStorage.setItem('navigation-type', 'detail-to-list');
  //   };

  //   window.addEventListener('popstate', handlePopState);

  //   return () => {
  //     window.removeEventListener('popstate', handlePopState);
  //   };
  // }, []);

  return (
    <div>
      {children}
    </div>
  );
}
