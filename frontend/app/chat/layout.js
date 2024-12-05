export default function ChatLayout({ children }) {
    return (
      <div className="h-screen flex flex-col">
        <main className="flex-1 overflow-hidden">
          {children}
        </main>
      </div>
    );
  }