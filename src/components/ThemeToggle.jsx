import React, { useEffect, useState } from "react";

export default function ThemeToggle() {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [isDark]);

  return (
    <button
      onClick={() => setIsDark(!isDark)}
      className="fixed top-4 right-4 p-2 rounded bg-gray-200 dark:bg-gray-700 text-sm text-gray-800 dark:text-white"
    >
      {isDark ? "☀️ Light" : "🌙 Dark"}
    </button>
  );
}
