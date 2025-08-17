import Image from "next/image";
import Link from "next/link";

export default function Item({image, title, slug}: {image: string, title: string, slug: string}) {
  return (
    <div className="bg-gray-700 w-64 rounded-lg relative flex gap-5">
      <Image src={image} alt={`${title} picture`} fill={true} className="w-16 h-16 mx-auto"/>
      <div className="p-4">
        <h4>{title}</h4>
        <Link key={title} href={slug} className="text-blue-500 hover:underline">
          View Details
        </Link>
      </div>
    </div>
    );
  }
