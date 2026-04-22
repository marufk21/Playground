import { api } from "./axios";

export type User = {
  id: number;
  name: string;
  email: string;
  image_url?: string | null;
};

export type CreateUserPayload = {
  name: string;
  email: string;
  image_url?: string | null;
};

export const getUsers = async (): Promise<User[]> => {
  const response = await api.get<User[]>("/users");
  const payload = response.data as User[] | { users?: User[] };

  if (Array.isArray(payload)) {
    return payload;
  }

  if (payload && Array.isArray(payload.users)) {
    return payload.users;
  }

  return [];
};

export const createUser = async (payload: CreateUserPayload): Promise<User> => {
  const response = await api.post<User>("/users", payload);
  return response.data;
};

export const uploadUserImage = async (file: File): Promise<string> => {
  const form = new FormData();
  form.append("file", file);

  const response = await api.post<{ url: string }>("/upload", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data.url;
};
