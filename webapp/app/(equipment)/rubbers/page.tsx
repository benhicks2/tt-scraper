"use client";
import { ItemList, EquipmentItem, ItemListLoading } from "@/app/ui/components/item";
import SearchBar from "@/app/ui/components/searchbar";
import { StringUtils } from "@/app/_lib/stringutils";
import React from "react";

export default function Page() {
  const [items, setItems] = React.useState<EquipmentItem[]>([]);
  const [cursor, setCursor] = React.useState<string | null>(null);
  const [hasMore, setHasMore] = React.useState<boolean>(true);
  const [loading, setLoading] = React.useState<boolean>(false);

  React.useEffect(() => {
    loadMore();
  }, []);

  async function loadMore() {
    setLoading(true);
    const response = await fetch(`http://127.0.0.1:5000/rubbers${cursor ? `?cursor=${cursor}` : ''}`);
    const data = await response.json();
    if (response.status == 404) {
      setHasMore(false);
      setCursor(null);
    }
    else {
      setItems((prevItems) => [...prevItems, ...data.items]);
      if (data.next == "null") {
        setHasMore(false);
        setCursor(null);
      }
      else {
        setCursor(data.next);
      }
    }
    setLoading(false);
  }

  return (
    <div>
      <ItemList items={items} loading={loading}/>
      {hasMore && (<button disabled={loading} onClick={loadMore}>Load More</button>)}
    </div>
  );
}
