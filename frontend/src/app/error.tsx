'use client'; // Error components must be Client Components

import { useEffect } from 'react';

export default function Error({ error, reset }: { error: Error & { digest?: string }; reset: () => void; }) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="text-center">
      <h2 className="font-poppins text-2xl font-bold mb-4">Something went wrong!</h2>
      <p className="mb-4">{error.message}</p>
      <button
        onClick={() => reset()}
        className="font-bold py-2 px-4 rounded-lg bg-gradient-to-r from-brand-primary to-brand-secondary text-white"
      >
        Try again
      </button>
    </div>
  );
}
