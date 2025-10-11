
import { BreadcrumbSkeleton } from "@/app/ui/components/breadcrumb";

export default function DetailsLoading() {
  return (
      <div className="bg-gray-50">
        {/* Header Section Skeleton */}
        <div className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            {/* Breadcrumb Navigation Skeleton */}
            <div className="mb-4">
              <BreadcrumbSkeleton />
            </div>

            {/* Product name skeleton */}
            <div className="animate-pulse">
              <div className="h-8 bg-gray-200 rounded w-3/4 mb-4 skeleton-shimmer"></div>
              <div className="flex items-center space-x-4">
                <div className="h-6 bg-gray-200 rounded-full w-32 skeleton-shimmer"></div>
                <div className="h-4 bg-gray-200 rounded w-24 skeleton-shimmer"></div>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content Skeleton */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Price Comparison Section Skeleton */}
          <div className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden mb-8">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="animate-pulse">
                <div className="h-6 bg-gray-200 rounded w-1/3 mb-2 skeleton-shimmer"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2 skeleton-shimmer"></div>
              </div>
            </div>

            <div className="divide-y divide-gray-200">
              {/* Store listing skeletons */}
              {Array.from({ length: 4 }).map((_, index) => (
                <div key={index} className="p-6">
                  <div className="animate-pulse">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3">
                          <div className="w-10 h-10 bg-gray-200 rounded-lg skeleton-shimmer"></div>
                          <div className="flex-1 min-w-0">
                            <div className="h-5 bg-gray-200 rounded w-1/3 mb-2 skeleton-shimmer"></div>
                            <div className="h-4 bg-gray-200 rounded w-1/4 skeleton-shimmer"></div>
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center space-x-4">
                        <div className="text-right">
                          <div className="h-8 bg-gray-200 rounded w-16 mb-1 skeleton-shimmer"></div>
                          {index === 0 && (
                            <div className="h-3 bg-gray-200 rounded w-20 skeleton-shimmer"></div>
                          )}
                        </div>
                        <div className="h-10 bg-gray-200 rounded w-24 skeleton-shimmer"></div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
  );
}
