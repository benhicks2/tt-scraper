"use client";
import React from "react";
import { usePathname, useRouter, useSearchParams } from 'next/navigation'
import { ItemList, EquipmentItem } from "@/app/ui/components/item";
import SearchBar from "@/app/ui/components/searchbar";
import { SearchParamsContext } from "next/dist/shared/lib/hooks-client-context.shared-runtime";

export default function Page() {
  const [items, setItems] = React.useState<EquipmentItem[]>([]);
  const [page, setPage] = React.useState<number>(1);
  const [query, setQuery] = React.useState<string | undefined>(undefined);
  const [hasMore, setHasMore] = React.useState<boolean>(true);
  const [loading, setLoading] = React.useState<boolean>(false);
  const { replace } = useRouter();
  const searchParams = useSearchParams();
  const pathname = usePathname();

  React.useEffect(() => {
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
    var currPage = 1;
    while (currPage <= initialPage) {
      loadPage(currPage, thisQuery);
      currPage++;
    }
  }, [searchParams.get('query')]);

  async function loadPage(page: number, query?: string) {
    setLoading(true);
    const response = await fetch(`http://127.0.0.1:5000/rubbers?page=${page}${query ? `&name=${query}` : ''}`);
    const data = await response.json();
    if (response.status == 404) {
      setHasMore(false);
    }
    else {
      setItems((prevItems) => [...prevItems, ...data.items]);
      setPage(page);
    }
    setLoading(false);
  }

  async function loadMore() {
    const params = new URLSearchParams(searchParams);
    const newPage = page + 1;
    setPage(newPage);
    loadPage(newPage, query);
    params.set('page', newPage.toString());
    replace(`${pathname}?${params.toString()}`, { scroll: false });
  }

  return (
    <div>
      <h1 className="text-3xl font-bold">Table Tennis Rubbers</h1>
      <SearchBar
        placeholder="Search items..."
        className="mb-4"
      />
      <ItemList items={items} loading={loading}/>
      {hasMore && (<button disabled={loading} onClick={loadMore}>Load More</button>)}
    </div>
  );
}
