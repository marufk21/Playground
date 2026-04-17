import { useState } from "react";

import { useCreateUser, useUsers } from "../hooks/useUsers";

const Home = () => {
  const { data: users, isLoading, isError, error } = useUsers();
  const { mutate: createUserMutate, isPending, isError: isCreateError, error: createError } =
    useCreateUser();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    createUserMutate(
      { name, email },
      {
        onSuccess: () => {
          setName("");
          setEmail("");
        },
      },
    );
  };

  if (isLoading) {
    return <p className="p-6">Loading users...</p>;
  }

  if (isError) {
    return (
      <p className="p-6 text-red-600">
        Failed to fetch users: {(error as Error).message}
      </p>
    );
  }

  return (
    <main className="mx-auto max-w-2xl p-6">
      <h1 className="mb-4 text-2xl font-bold">Home</h1>

      <form onSubmit={handleSubmit} className="mb-6 space-y-3 rounded border p-4">
        <h2 className="text-lg font-semibold">Create User</h2>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full rounded border p-2"
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full rounded border p-2"
          required
        />
        <button
          type="submit"
          disabled={isPending}
          className="rounded bg-black px-4 py-2 text-white disabled:opacity-50"
        >
          {isPending ? "Creating..." : "Create User"}
        </button>
        {isCreateError && (
          <p className="text-sm text-red-600">Failed to create user: {(createError as Error).message}</p>
        )}
      </form>

      <h2 className="mb-3 text-lg font-semibold">Users</h2>

      {users && users.length > 0 ? (
        <ul className="space-y-2">
          {users.map((user) => (
            <li key={user.id} className="rounded border p-3">
              <p className="font-medium">{user.name}</p>
              <p className="text-sm text-gray-600">{user.email}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No users found.</p>
      )}
    </main>
  );
};

export default Home;
