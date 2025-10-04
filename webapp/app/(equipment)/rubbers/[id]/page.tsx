import { ItemDescription } from "@/app/ui/components/item";
import { DetailPageWrapper } from "./detail-page-wrapper";

export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const response = await fetch(`http://127.0.0.1:5000/rubbers/${id}`);
  if (!response.ok) {
    throw new Error("Failed to fetch rubber item");
  }
  const data = await response.json();

  return (
    <DetailPageWrapper>
      <ItemDescription item={data} />
    </DetailPageWrapper>
  );
}
