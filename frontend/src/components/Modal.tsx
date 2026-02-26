// src/components/Modal.tsx
import React, { useEffect } from 'react';

// Defina as props que o componente Modal espera
interface ModalProps {
  isOpen: boolean;           // Controla se a modal está aberta
  onClose: () => void;       // Função chamada ao fechar a modal (pode ser por botão, X ou fundo escuro)
  title?: string;            // Título opcional da modal
  children: React.ReactNode; // Conteúdo da modal (pode ser texto, outros componentes, etc.)
  footer?: React.ReactNode;  // Rodapé opcional da modal (para botões de ação)
}

const Modal: React.FC<ModalProps> = ({ isOpen, onClose, title, children, footer }) => {
  // Fecha a modal ao pressionar ESC
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleEsc);
    return () => window.removeEventListener('keydown', handleEsc);
  }, [onClose]);

  // Se não estiver aberta, não renderiza nada
  if (!isOpen) return null;

  return (
    // Fundo escuro (overlay)
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50 backdrop-blur-sm">
      {/* Conteúdo da modal */}
      <div className="bg-white rounded-xl shadow-xl w-full max-w-md max-h-[90vh] overflow-y-auto">
        {/* Cabeçalho */}
        {title && (
          <div className="border-b border-gray-200 px-6 py-4">
            <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          </div>
        )}
        {/* Corpo */}
        <div className="p-6">
          {children}
        </div>
        {/* Rodapé (botões) */}
        {footer && (
          <div className="border-t border-gray-200 px-6 py-4 bg-gray-50 rounded-b-xl flex justify-end space-x-3">
            {footer}
          </div>
        )}
        {/* Botão de fechar (X) */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-500 hover:text-gray-700 focus:outline-none"
          aria-label="Close"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default Modal;