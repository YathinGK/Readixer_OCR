import React from "react";
import FeatureSection from "../components/FeatureSection";
import ThemeToggle from "../components/ThemeToggle"; // make sure the path is correct

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-slate-100 dark:from-gray-900 dark:to-gray-800 text-gray-800 dark:text-gray-100 flex flex-col justify-between">
      {/* Theme Toggle */}
      <ThemeToggle />

      {/* Hero Section */}
      <div className="w-full py-16 px-6 text-center bg-white dark:bg-gray-900 font-[Cambria]">
        <div className="animate-fade-in">
          <h1
            className="text-6xl md:text-7xl font-extrabold text-violet-700 drop-shadow-sm tracking-wide"
            style={{ fontFamily: "'Orbitron', sans-serif" }}
          >
            READIXER
          </h1>
          <p className="mt-4 text-gray-600 dark:text-gray-300 text-lg md:text-xl tracking-wide font-normal">
            One Upload. Two Smart Tools. Infinite Simplicity.
          </p>
        </div>
      </div>

      {/* Feature Section */}
      <FeatureSection />

      {/* Footer */}
      <footer className="bg-gray-100 dark:bg-gray-800 text-center py-6 mt-auto text-sm text-gray-500 dark:text-gray-300 font-[Cambria]">
        Built with ❤️ by{" "}
        <a
          href="https://www.linkedin.com/in/developer1"
          className="text-blue-500 hover:underline ml-1 font-bold"
          target="_blank"
          rel="noopener noreferrer"
        >
          YATHIN G KUMMAR
        </a>
        ,{" "}
        <a
          href="https://www.linkedin.com/in/developer2"
          className="text-blue-500 hover:underline ml-1 font-bold"
          target="_blank"
          rel="noopener noreferrer"
        >
          ANANYA R BHAT
        </a>
        ,{" "}
        <a
          href="https://www.linkedin.com/in/developer3"
          className="text-blue-500 hover:underline ml-1 font-bold"
          target="_blank"
          rel="noopener noreferrer"
        >
          SANIA
        </a>
      </footer>
    </div>
  );
}
