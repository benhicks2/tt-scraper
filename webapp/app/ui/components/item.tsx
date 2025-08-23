"use client";
import Image from "next/image";
import Link from "next/link";
import { StringUtils } from "@/app/_lib/stringutils";

export type EquipmentItem = {
  _id: string;
  name: string;
  all_time_low_price: string;
  entries: Array<{
    url: string;
    price: string;
    last_updated: string;
  }>;
};

export function Item({image, title, price, slug}: {image: string, title: string, price: string, slug: string}) {
  return (
    <div className="bg-gray-700 w-64 min-h-40 rounded-lg relative flex gap-5 justify-end flex-col">
      {/* <Image src={image} alt={`${title} picture`} fill className="mx-auto"/> */}
      <div className="p-4">
        <h4>{title}</h4>
        <p className="text-lg font-bold">${price}</p>
        <Link key={title} href={slug} className="text-blue-500 hover:underline">
          View Details
        </Link>
      </div>
    </div>
  );
}

export function ItemList({ items, loading }: { items: EquipmentItem[], loading: boolean }) {
  return (
    <div className="flex flex-wrap gap-4">
      {items.map((item) => (
        <Item
          key={item._id}
          image={"/test.jpg"}
          title={StringUtils.truncate(item.name, 50)}
          price={item.entries[0].price}
          slug={`/rubbers/${item._id}`}
        />
      ))}
      {loading && ItemListLoading()}
    </div>
  );
}

export function ItemDescription({ item }: { item: EquipmentItem }) {
  return (
    <div>
      <h2>{item.name}</h2>
      <p>All Time Low Price: ${item.all_time_low_price}</p>
      <h3>Price History:</h3>
      <ul>
        {item.entries.map((entry) => (
          <li key={entry.url}>
            {entry.last_updated}: ${entry.price}
          </li>
        ))}
      </ul>
    </div>
  );
}

function LoadingItem() {
  return (
    <div className="bg-gray-700 w-64 min-h-40 rounded-lg relative flex gap-5 justify-end flex-col">
      <div className="p-4 flex gap-1 flex-col">
        <h4 className="animate-pulse bg-gray-600 h-4 w-3/4 rounded"></h4>
        <p className="animate-pulse bg-gray-600 h-4 w-1/4 rounded"></p>
        <button className="animate-pulse bg-gray-600 h-4 w-1/2 rounded"></button>
      </div>
    </div>
  );
}

export function ItemListLoading() {
  return (
    Array.from({ length: 10 }).map((_, index) => (
      <LoadingItem key={index} />
    ))
  );
}
