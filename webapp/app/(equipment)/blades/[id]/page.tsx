import { notFound } from 'next/navigation';
import { ItemDescription } from "@/app/ui/components/item";
import { DetailPageWrapper } from "./detail-page-wrapper";

export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/blades/${id}`);
  if (!response.ok) {
    notFound();
  }
  const data = await response.json();

  return (
    <DetailPageWrapper>
      <ItemDescription item={data} />
    </DetailPageWrapper>
  );
}
