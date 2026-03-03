"use client";

export default function Error({ error }: any) {
  return (
    <div className="p-10 text-center text-red-500">
      Something went wrong: {error.message}
    </div>
  );
}