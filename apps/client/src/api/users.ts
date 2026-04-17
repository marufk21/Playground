import { api } from "./axios";

export type User = {
  id: number;
  name: string;
  email: string;
};

export type CreateUserPayload = {
  name: string;
  email: string;
};

export const getUsers = async (): Promise<User[]> => {
  const response = await api.get<User[]>("/users");
  return response.data;
};

export const createUser = async (payload: CreateUserPayload): Promise<User> => {
  const response = await api.post<User>("/users", payload);
  return response.data;
};
