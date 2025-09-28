"use client";
import { useSearchParams, usePathname, useRouter } from 'next/navigation';

type SearchBarProps = {
  placeholder: string,
  className: string
};

export default function SearchBar({
  placeholder = "Search...",
  className = "",
}: SearchBarProps) {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const { replace } = useRouter();

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const input = formData.get('query')?.toString().trim();
    const params = new URLSearchParams(searchParams);
    if (input) {
      params.set('query', input);
    }
    else {
      params.delete('query');
    }
    params.set('page', '1');
    replace(`${pathname}?${params.toString()}`);
  }

  return (
    <form className={`flex items-center ${className}`} onSubmit={handleSubmit}>
      <input
        name="query"
        type="text"
        placeholder={placeholder}
        defaultValue={searchParams.get('query')?.toString()}
        className="border rounded-l px-3 py-2 focus:outline-none"
        aria-label="Search"
      />
      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded-r hover:bg-blue-700"
      >
        Search
      </button>
    </form>
  );
}
