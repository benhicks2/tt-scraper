"use client";
import React from "react";
import { useRouter } from 'next/navigation'
import { ItemList, EquipmentItem, ItemListLoading } from "@/app/ui/components/item";
import SearchBar from "@/app/ui/components/searchbar";
import { StringUtils } from "@/app/_lib/stringutils";

export default function Page() {
  const [items, setItems] = React.useState<EquipmentItem[]>([]);
  const [page, setPage] = React.useState<number>(1);
  const [hasMore, setHasMore] = React.useState<boolean>(true);
  const [loading, setLoading] = React.useState<boolean>(false);
  const router = useRouter();

  React.useEffect(() => {
      console.log("here");
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
        loadMore();
        currPage++;
      }
  }, []);

  // React.useEffect(() => {
  //   console.log("Here: ", items.length);
  //   if (items.length > 0) {
  //     sessionStorage.setItem("items", JSON.stringify(items));
  //     sessionStorage.setItem("cursor", cursor || "");
  //   }
  // }, [items]);

  async function loadMore() {
    setLoading(true);
    const newPage = page + 1;
    router.push(`?page=${newPage}`, { scroll: false });
    const response = await fetch(`http://127.0.0.1:5000/rubbers?page=${newPage}`);
    const data = await response.json();
    if (response.status == 404) {
      setHasMore(false);
    }
    else {
      setItems((prevItems) => [...prevItems, ...data.items]);
      setPage(newPage);
      if (data.next == "null") {
        setHasMore(false);
      }
    }
    setLoading(false);
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
