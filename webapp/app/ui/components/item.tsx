import Image from "next/image";
import Link from "next/link";

export default function Item({image, title, price, slug}: {image: string, title: string, price: string, slug: string}) {
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
