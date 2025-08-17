import Item from "@/app/ui/components/item";

export default function Home() {
  return (
    <main className="p-4">
      <h1 className="text-3xl font-bold">Welcome to My Application</h1>
      <p className="mt-2">This is the home page content.</p>
      <Item
        image="/test.jpg"
        title="Sample Item"
        slug="/rubbers"
      />
    </main>
  );
}
