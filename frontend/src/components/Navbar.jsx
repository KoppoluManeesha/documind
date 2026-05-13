import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-white border-b border-gray-100 py-4 px-8 flex justify-between items-center">
      <div className="text-xl font-bold text-blue-600">DocuMind AI</div>
      <div className="flex gap-6">
        <Link to="/" className="text-gray-600 hover:text-blue-500">Home</Link>
        <Link to="/history" className="text-gray-600 hover:text-blue-500">History</Link>
      </div>
    </nav>
  );
};

export default Navbar;