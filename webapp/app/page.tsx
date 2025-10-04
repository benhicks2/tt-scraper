"use client";
import SearchBar from "./ui/components/searchbar";
import { StringUtils } from "@/app/_lib/stringutils";
import React, { Suspense } from "react";

function HomeContent() {
  return (
    <main className="p-4">
      <h1 className="text-3xl font-bold">Table Tennis Equipment</h1>
      <SearchBar
        placeholder="Search items..."
        className="mb-4"
      />
      <p>Hello</p>
    </main>
  );
}

export default function Home() {
  return (
    <Suspense fallback={
      <main className="p-4">
        <h1 className="text-3xl font-bold">Table Tennis Equipment</h1>
        <div className="animate-pulse bg-gray-200 h-12 rounded mb-4"></div>
        <p>Loading...</p>
      </main>
    }>
      <HomeContent />
    </Suspense>
  );
}
