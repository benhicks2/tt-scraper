"use client";
import { useState, useEffect } from "react";
import { usePathname, useRouter, useSearchParams } from 'next/navigation';
import { EquipmentItem } from "@/app/ui/components/item";

interface UseEquipmentPageProps {
  equipmentType: 'rubbers' | 'blades';
}

export function useEquipmentPage({ equipmentType }: UseEquipmentPageProps) {
  const [items, setItems] = useState<EquipmentItem[]>([]);
  const [page, setPage] = useState<number>(1);
  const [query, setQuery] = useState<string | undefined>(undefined);
  const [hasMore, setHasMore] = useState<boolean>(true);
  const [loading, setLoading] = useState<boolean>(true);
  const { replace } = useRouter();
  const searchParams = useSearchParams();
  const pathname = usePathname();

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
          const response = await fetch(`http://127.0.0.1:5000/${equipmentType}?page=${currPage}${thisQuery ? `&name=${thisQuery}` : ''}`);
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
  }, [equipmentType]);

  async function loadPage(page: number, query?: string, isInitialLoad: boolean = false) {
    setLoading(true);
    const response = await fetch(`http://127.0.0.1:5000/${equipmentType}?page=${page}${query ? `&name=${query}` : ''}`);
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

  return {
    items,
    page,
    query,
    hasMore,
    loading,
    loadMore
  };
}
