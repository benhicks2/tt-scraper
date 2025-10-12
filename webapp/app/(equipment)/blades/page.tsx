"use client";
import React, { Suspense } from "react";
import { EquipmentPageContent } from "@/app/ui/components/EquipmentPageContent";
import { breadcrumbConfigs } from "@/app/ui/components/breadcrumb";

function BladesPageContent() {
  return (
    <EquipmentPageContent
      equipmentType="blades"
      title="Table Tennis Blades"
      searchPlaceholder="Search blades..."
      breadcrumbItems={breadcrumbConfigs.blades}
    />
  );
}

export default function Page() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading blades...</p>
        </div>
      </div>
    }>
      <BladesPageContent />
    </Suspense>
  );
}
