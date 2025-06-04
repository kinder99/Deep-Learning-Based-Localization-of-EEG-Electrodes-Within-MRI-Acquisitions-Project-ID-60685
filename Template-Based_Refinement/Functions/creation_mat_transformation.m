function M = creation_mat_transformation(Rotation , Translation)

Translation = [Translation ; 1];
Rotation = [ Rotation ; 0 0 1];

M = [Rotation , Translation];
