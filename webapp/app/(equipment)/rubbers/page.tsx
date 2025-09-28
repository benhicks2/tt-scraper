"use client";
import React from "react";
import { useRouter } from 'next/navigation'
import { ItemList, EquipmentItem } from "@/app/ui/components/item";
import SearchBar from "@/app/ui/components/searchbar";

export default function Page() {
  const [items, setItems] = React.useState<EquipmentItem[]>([]);
  const [page, setPage] = React.useState<number>(1);
  const [hasMore, setHasMore] = React.useState<boolean>(true);
  const [loading, setLoading] = React.useState<boolean>(false);
  const router = useRouter();

  React.useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const pageParam = params.get('page');
    const initialPage = pageParam ? parseInt(pageParam, 10) : 1;
    if (isNaN(initialPage) || initialPage < 1) {
      setPage(1);
    } else {
      setPage(initialPage);
    }
    var currPage = 1;
    while (currPage <= initialPage) {
      loadPage(currPage);
      currPage++;
    }
  }, []);

  async function loadPage(page: number) {
    setLoading(true);
    const response = await fetch(`http://127.0.0.1:5000/rubbers?page=${page}`);
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
    const newPage = page + 1;
    setPage(newPage);
    loadPage(newPage);
    router.push(`?page=${newPage}`, { scroll: false });
  }

  return (
    <div>
      <h1 className="text-3xl font-bold">Table Tennis Rubbers</h1>
      <SearchBar
        placeholder="Search items..."
        onSearch={(query) => console.log("Searching for:", query)}
        className="mb-4"
      />
      <ItemList items={items} loading={loading}/>
      {hasMore && (<button disabled={loading} onClick={loadMore}>Load More</button>)}
    </div>
  );
}
