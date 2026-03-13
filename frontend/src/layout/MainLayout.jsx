import { Outlet } from "react-router-dom";

function MainLayout() {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <header className="bg-white shadow p-4">
        <h1 className="text-xl font-semibold text-blue-900">Nyay Saar</h1>
      </header>

      {/* Page Content */}
      <main className="p-6">
        <Outlet />
      </main>
    </div>
  );
}

export default MainLayout;
