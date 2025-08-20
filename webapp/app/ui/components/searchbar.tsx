
type SearchBarProps = {
  placeholder: string,
  onSearch: (query: string) => void,
  className: string
};

export default function SearchBar({
  placeholder = "Search...",
  onSearch,
  className = "",
}: SearchBarProps) {
  return (
    <form className={`flex items-center ${className}`}>
      <input
        type="text"
        placeholder={placeholder}
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
