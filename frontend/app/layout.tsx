export default function RootLayout({ children }: any) {
  return (
    <html>
      <body className="bg-gray-50 text-gray-900">
        <div className="min-h-screen">
          <nav className="bg-white shadow-sm p-4">
            <div className="max-w-6xl mx-auto font-semibold">
              LLM Eval Dashboard
            </div>
          </nav>

          {children}
        </div>
      </body>
    </html>
  );
}