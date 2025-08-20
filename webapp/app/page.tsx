import Item from "@/app/ui/components/item";
import SearchBar from "./ui/components/searchbar";

export default function Home() {
  return (
    <main className="p-4">
      <h1 className="text-3xl font-bold">Table Tennis Equipment</h1>
      <SearchBar
        placeholder="Search items..."
        onSearch={(query) => console.log("Searching for:", query)}
        className="mb-4"
      />
      <Item
        image="/test.jpg"
        title="Sample Item"
        slug="/rubbers"
      />
    </main>
  );
}
