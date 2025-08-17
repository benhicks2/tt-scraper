export default function SideNav() {
  return (
    <nav className="bg-gray-800 text-white p-4 fixed h-full left-0 top-0 w-48">
      <h2 className="text-xl font-bold">My Application Sidebar</h2>
      <ul className="mt-4 space-y-2">
        <li>
          <a href="#" className="hover:underline">
            Home
          </a>
        </li>
        <li>
          <a href="/rubbers" className="hover:underline">
            Rubbers
          </a>
        </li>
        <li>
          <a href="/blades" className="hover:underline">
            Blades
          </a>
        </li>
      </ul>
    </nav>
    );
  }
