import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createUser, type CreateUserPayload, getUsers, uploadUserImage } from "../api/users";

export const useUsers = () =>
  useQuery({
    queryKey: ["users"],
    queryFn: getUsers,
  });

export const useCreateUser = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: CreateUserPayload) => createUser(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });
};

export const useUploadUserImage = () =>
  useMutation({
    mutationFn: (file: File) => uploadUserImage(file),
  });
