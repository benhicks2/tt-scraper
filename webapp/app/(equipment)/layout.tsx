import SearchBar from "@/app/ui/components/searchbar";

export default function EquipmentLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

  return (
    <main className="p-4">
      {children}
    </main>
  )
}