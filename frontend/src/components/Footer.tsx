import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-100 text-gray-600 py-8 border-t border-gray-200">
      <div className="container mx-auto px-4 text-center">
        <p>&copy; {new Date().getFullYear()} DocuGeniusAI. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;