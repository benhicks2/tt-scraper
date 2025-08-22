import Item from "@/app/ui/components/item";
import SearchBar from "./ui/components/searchbar";
import { StringUtils } from "@/lib/stringutils";

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

async function loadMore() {

}

export default async function Home() {
  const data = await fetch("http://127.0.0.1:5000/rubbers");
  const equipment = await data.json();

  return (
    <main className="p-4">
      <h1 className="text-3xl font-bold">Table Tennis Equipment</h1>
      <SearchBar
        placeholder="Search items..."
        onSearch={(query) => console.log("Searching for:", query)}
        className="mb-4"
      />
      <div className="flex flex-wrap gap-4">
        {equipment['items'].map((item: EquipmentItem) => (
          <Item
            key={item._id}
            image={"/test.jpg"}
            title={StringUtils.truncate(item.name, 50)}
            price={item.entries[0].price}
            slug={`/rubbers/${item._id}`}
          />
        ))}
      </div>
      {/* <button onClick={loadMore}>Load More</button> */}
    </main>
  );
}
