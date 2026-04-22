import { useEffect, useMemo, useState } from "react";

import { useCreateUser, useUploadUserImage, useUsers } from "../hooks/useUsers";

const Home = () => {
  const { data: users, isLoading, isError, error } = useUsers();
  const { mutate: createUserMutate, isPending, isError: isCreateError, error: createError } =
    useCreateUser();
  const {
    mutateAsync: uploadImageMutateAsync,
    isPending: isUploadPending,
    isError: isUploadError,
    error: uploadError,
  } = useUploadUserImage();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [imageFile, setImageFile] = useState<File | null>(null);

  const previewUrl = useMemo(() => {
    if (!imageFile) return null;
    return URL.createObjectURL(imageFile);
  }, [imageFile]);

  useEffect(() => {
    if (!previewUrl) return;
    return () => URL.revokeObjectURL(previewUrl);
  }, [previewUrl]);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    let imageUrl: string | null = null;
    if (imageFile) {
      imageUrl = await uploadImageMutateAsync(imageFile);
    }

    createUserMutate(
      { name, email, image_url: imageUrl },
      {
        onSuccess: () => {
          setName("");
          setEmail("");
          setImageFile(null);
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
        <div className="space-y-2">
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setImageFile(e.target.files?.[0] ?? null)}
            className="w-full rounded border p-2"
          />
          {previewUrl && (
            <img
              src={previewUrl}
              alt="Selected preview"
              className="h-20 w-20 rounded object-cover"
            />
          )}
        </div>
        <button
          type="submit"
          disabled={isPending || isUploadPending}
          className="rounded bg-black px-4 py-2 text-white disabled:opacity-50"
        >
          {isUploadPending ? "Uploading..." : isPending ? "Creating..." : "Create User"}
        </button>
        {isUploadError && (
          <p className="text-sm text-red-600">
            Failed to upload image: {(uploadError as Error).message}
          </p>
        )}
        {isCreateError && (
          <p className="text-sm text-red-600">Failed to create user: {(createError as Error).message}</p>
        )}
      </form>

      <h2 className="mb-3 text-lg font-semibold">Users</h2>

      {users && users.length > 0 ? (
        <ul className="space-y-2">
          {users.map((user) => (
            <li key={user.id} className="rounded border p-3">
              <div className="flex items-center gap-3">
                {user.image_url ? (
                  <img
                    src={user.image_url}
                    alt={`${user.name} avatar`}
                    className="h-10 w-10 rounded-full object-cover"
                    loading="lazy"
                  />
                ) : (
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gray-200 text-sm font-semibold text-gray-700">
                    {user.name?.slice(0, 1)?.toUpperCase() ?? "?"}
                  </div>
                )}
                <div>
                  <p className="font-medium">{user.name}</p>
                  <p className="text-sm text-gray-600">{user.email}</p>
                </div>
              </div>
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
