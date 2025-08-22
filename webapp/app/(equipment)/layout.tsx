import SearchBar from "@/app/ui/components/searchbar";

export default function EquipmentLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

  return (
    <main className="p-4">
      <h1 className="text-3xl font-bold">Table Tennis Equipment</h1>
      <SearchBar
        placeholder="Search items..."
        onSearch={(query) => console.log("Searching for:", query)}
        className="mb-4"
      />
      {children}
    </main>
  )
}