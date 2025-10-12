"use client";
import React, { Suspense } from "react";
import { EquipmentPageContent } from "@/app/ui/components/EquipmentPageContent";
import { breadcrumbConfigs } from "@/app/ui/components/breadcrumb";

function RubbersPageContent() {
  return (
    <EquipmentPageContent
      equipmentType="rubbers"
      title="Table Tennis Rubbers"
      searchPlaceholder="Search rubbers..."
      breadcrumbItems={breadcrumbConfigs.rubbers}
    />
  );
}

export default function Page() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading rubbers...</p>
        </div>
      </div>
    }>
      <RubbersPageContent />
    </Suspense>
  );
}
