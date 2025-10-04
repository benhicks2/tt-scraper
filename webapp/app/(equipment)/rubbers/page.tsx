"use client";
import React, { useState, useEffect, useRef, Suspense } from "react";
import { usePathname, useRouter, useSearchParams } from 'next/navigation'
import { ItemList, EquipmentItem } from "@/app/ui/components/item";
import SearchBar from "@/app/ui/components/searchbar";

function RubbersPageContent() {
  const [items, setItems] = useState<EquipmentItem[]>([]);
  const [page, setPage] = useState<number>(1);
  const [query, setQuery] = useState<string | undefined>(undefined);
  const [hasMore, setHasMore] = useState<boolean>(true);
  const [loading, setLoading] = useState<boolean>(true);
  const { replace } = useRouter();
  const searchParams = useSearchParams();
  const pathname = usePathname();

  // Restore scroll position only when coming back from detail page
  // useEffect(() => {
  //   const navigationType = sessionStorage.getItem('navigation-type');
  //   const savedScrollPosition = sessionStorage.getItem('rubbers-scroll-position');

  //   if (navigationType === 'detail-to-list' && savedScrollPosition) {
  //     const scrollPosition = parseInt(savedScrollPosition, 10);
  //     setTimeout(() => {
  //       window.scrollTo(0, scrollPosition);
  //     }, 100);
  //   } else {
  //     // Reset scroll position for other navigation types
  //     window.scrollTo(0, 0);
  //   }

  //   // Clear the navigation type after handling
  //   sessionStorage.removeItem('navigation-type');
  // }, []);

  // // Save scroll position and navigation type when navigating to detail page
  // useEffect(() => {
  //   const handleLinkClick = (event: MouseEvent) => {
  //     const target = event.target as HTMLElement;
  //     const link = target.closest('a[href*="/rubbers/"]');

  //     if (link) {
  //       sessionStorage.setItem('rubbers-scroll-position', window.scrollY.toString());
  //       sessionStorage.setItem('navigation-type', 'list-to-detail');
  //     }
  //   };

  //   // Listen for clicks on detail page links
  //   document.addEventListener('click', handleLinkClick);

  //   return () => {
  //     document.removeEventListener('click', handleLinkClick);
  //   };
  // }, []);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const pageParam = params.get('page');
    const thisQuery = params.get('query') || undefined;
    setQuery(thisQuery);
    const initialPage = pageParam ? parseInt(pageParam, 10) : 1;
    if (isNaN(initialPage) || initialPage < 1) {
      setPage(1);
    } else {
      setPage(initialPage);
    }
    setItems([]);
    setHasMore(true);

    // Load all pages sequentially to avoid race conditions
    const loadAllPages = async () => {
      let currPage = 1;
      let allItems: EquipmentItem[] = [];

      while (currPage <= initialPage) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/rubbers?page=${currPage}${thisQuery ? `&name=${thisQuery}` : ''}`);
          const data = await response.json();
          if (response.status === 404) {
            setHasMore(false);
            break;
          } else {
            allItems = [...allItems, ...data.items];
            setPage(currPage);
          }
        } catch (error) {
          console.error('Error loading page:', error);
          break;
        }
        currPage++;
      }

      setItems(allItems);
      setLoading(false);
    };

    setLoading(true);
    loadAllPages();
  }, [searchParams.get('query')]);

  async function loadPage(page: number, query?: string, isInitialLoad: boolean = false) {
    setLoading(true);
    const response = await fetch(`http://127.0.0.1:5000/rubbers?page=${page}${query ? `&name=${query}` : ''}`);
    const data = await response.json();
    if (response.status == 404) {
      setHasMore(false);
    }
    else {
      if (isInitialLoad) {
        // For initial load, replace items instead of appending
        setItems(data.items);
      } else {
        // For load more, append to existing items
        setItems((prevItems: EquipmentItem[]) => [...prevItems, ...data.items]);
      }
      setPage(page);
    }
    setLoading(false);
  }

  async function loadMore() {
    const params = new URLSearchParams(searchParams);
    const newPage = page + 1;
    setPage(newPage);
    loadPage(newPage, query, false);
    params.set('page', newPage.toString());
    replace(`${pathname}?${params.toString()}`, { scroll: false });
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Material Design Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-medium text-gray-900 mb-6">
            Table Tennis Rubbers
          </h1>
          <SearchBar
            placeholder="Search rubbers..."
            className="max-w-md"
          />
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <ItemList items={items} loading={loading}/>

        {/* Load More Button with Material Design */}
        {hasMore && (
          <div className="flex justify-center mt-8">
            <button
              disabled={loading}
              onClick={loadMore}
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 ease-in-out transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-xl"
            >Load More
            </button>
          </div>
        )}
      </div>
    </div>
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
