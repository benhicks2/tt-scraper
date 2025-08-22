"use client";
import Item from "@/app/ui/components/item";
import SearchBar from "./ui/components/searchbar";
import { StringUtils } from "@/lib/stringutils";
import React from "react";

type EquipmentItem = {
  _id: string;
  name: string;
  all_time_low_price: string;
  entries: Array<{
    url: string;
    price: string;
    last_updated: string;
  }>;
};

export default function Home() {
  const [items, setItems] = React.useState<EquipmentItem[]>([]);
  const [cursor, setCursor] = React.useState<string | null>(null);
  const [hasMore, setHasMore] = React.useState<boolean>(true);

  React.useEffect(() => {
    loadMore();
  }, []);

  async function loadMore() {
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
  }

  return (
    <main className="p-4">
      <h1 className="text-3xl font-bold">Table Tennis Equipment</h1>
      <SearchBar
        placeholder="Search items..."
        onSearch={(query) => console.log("Searching for:", query)}
        className="mb-4"
      />
      <div className="flex flex-wrap gap-4">
        {items.map((item: EquipmentItem) => (
          <Item
            key={item._id}
            image={"/test.jpg"}
            title={StringUtils.truncate(item.name, 50)}
            price={item.entries[0].price}
            slug={`/rubbers/${item._id}`}
          />
        ))}
      </div>
      {hasMore && (<button onClick={loadMore}>Load More</button>)}
    </main>
  );
}
